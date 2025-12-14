# Importation des bibliothèques nécessaires à l'exécution du script python
import sys                                                      # Module sys, permet d’accéder aux paramètres donnés au script Python depuis le terminal
import re                                                       # Librairie Python pour utiliser les expressions régulières (analyser les CIGAR)
import math                                                     # Pour les calculs de moyenne, écart-type, min, max ...


# _____________________________________________________________________________________________________________________________________________________________________#
#                                                            1. EXTRACTION DES READS DEPUIS UN FICHIER SAM                                                             #
# _____________________________________________________________________________________________________________________________________________________________________#


def read_sam(sam_file):                                         # Lit un fichier SAM et renvoie un dictionnaire :
    """
    Parses a SAM file and organizes reads by their Query Name (QNAME).

    Args:
        sam_file (str): Path to the input SAM file.

    Returns:
        dict: A dictionary where keys are QNAMEs and values are lists of dictionaries,
              each representing a read (handling paired-end data).
    """
    dico_sam = {}                                               # Dictionnaire de listes de dictionnaires contenant les 10 premières colonnes du fichier SAM

    with open(sam_file, 'r') as file:                           # Ouverture (et fermeture) du fichier SAM
        for line in file:                                       # Boucle sur chaque ligne du fichier SAM
            if not line.startswith("@"):                        # Ignore les lignes d'en-tête
                list_column = line.rstrip("\n").split("\t")     # Découpe la ligne en cours et la stocke dans une liste
                QNAME = list_column[0]                          # Stocke la première valeur de la liste dans la variable QNAME
                dico_temp = {                                   # Création d'un dico temporaire
                    "FLAG": int(list_column[1]),                # Structure globale du dico temporaire :
                    "RNAME": list_column[2],                    # "KEY" : value (en fonction du n° de colonne du fichier SAM)
                    "POS": int(list_column[3]),                 # + transformation de String vers int pour les champs numériques
                    "MAPQ": int(list_column[4]),
                    "CIGAR": list_column[5],
                    "RNEXT": list_column[6],
                    "PNEXT": int(list_column[7]),
                    "TLEN": int(list_column[8]),
                    "SEQ": list_column[9]
                }

                if QNAME not in dico_sam:                       # Si le nom du read (QNAME) n’existe pas encore comme clé dans le dictionnaire dico_sam
                    dico_sam[QNAME] = []                        # On crée une liste vide associée à cette clé
                    # Cette liste permettra de stocker plusieurs entrées pour le même QNAME -> gestion des paires de reads (read1 et read2)
                dico_sam[QNAME].append(dico_temp)               # Ajoute dico_temp (contenant toutes les informations d'un read) à la liste correspondant à ce QNAME
                    # Chaque QNAME devient une clé pointant vers une liste de dictionnaires, chacun représentant un read du fichier SAM
    return dico_sam


# _____________________________________________________________________________________________________________________________________________________________________#
#                                                                          2. ANALYSE DU FLAG                                                                          #
# _____________________________________________________________________________________________________________________________________________________________________#


def flag_decoding(FLAG):                                        # Converti une valeur de FLAG (entier) en dictionnaire de booléens
    """
    Decodes the bitwise SAM FLAG integer into a dictionary of boolean statuses.

    Args:
        FLAG (int): The decimal FLAG value from the SAM file.

    Returns:
        dict: A dictionary mapping FLAG properties (e.g., 'is_paired', 'is_unmapped')
              to boolean values (True/False).
    """
    bit_list = [
        "is_paired",        # bit 0  (1)
        "is_proper_pair",   # bit 1  (2)
        "is_unmapped",      # bit 2  (4)
        "mate_unmapped",    # bit 3  (8)
        "is_reverse",       # bit 4  (16)
        "mate_reverse",     # bit 5  (32)
        "is_read1",         # bit 6  (64)
        "is_read2",         # bit 7  (128)
        "not_primary",      # bit 8  (256)
        "fails_qc",         # bit 9  (512)
        "is_duplicate",     # bit 10 (1024)
        "is_supplementary"  # bit 11 (2048)
    ]

    list_flagB = list(bin(FLAG)[2:])                            # Conversion en liste de caractère binaire et suppression de '0b'
    if len(list_flagB) < 12:                                    # Si la longueur du binaire < 12 bits, alors : compléter avec des '0' à gauche
        list_flagB = ['0']*(12 - len(list_flagB)) + list_flagB

    dico_flag_bool = {}
    for i in range(12):                                         # Boucle de 0 à 11 (les 12 bits)
        bit_temp = list_flagB[-(i+1)]                           # Récupère le i-ème bit en partant de la fin de la liste de bits
        dico_flag_bool[bit_list[i]] = (bit_temp == '1')         # Vérifie si le bit i du FLAG est actif, convertit en True/False et stocke

    return dico_flag_bool


# _____________________________________________________________________________________________________________________________________________________________________#
#                                                                         3. ANALYSE DU CIGAR                                                                          #
# _____________________________________________________________________________________________________________________________________________________________________#


def cigar_decoding(CIGAR):                                      # Prend une seule valeur de CIGAR et renvoie un dictionnaire
    """
    Parses a CIGAR string to count the number of bases associated with each operation.

    Args:
        CIGAR (str): The CIGAR string (e.g., "10M2I5M").

    Returns:
        dict: A dictionary with CIGAR operations as keys (e.g., 'M', 'I', 'D')
              and the total count of bases as values.
    """
    cigar_operations = ['M','I','D','S','H','N','P','X','=']    # Définit toutes les lettres possibles du CIGAR
    dico_1cigar = {op: 0 for op in cigar_operations}            # Dictionnaire du nombre de bases pour chaque lettre du CIGAR (initialisé à 0)
    list_tuples = re.findall(r'(\d+)([MIDNSHP=X])', CIGAR)      # Liste de tuples (nombre, opération) pour chaque segment du CIGAR
    for number_of_bases, letter in list_tuples:                 # Pour chaque tuple (number_of_bases, letter)
        dico_1cigar[letter] += int(number_of_bases)             # Ajout du nombre de bases à la clé correspondante dans dico_ops
    return dico_1cigar


def analyze_cigar(dico_sam):
    """
    Computes global statistics for CIGAR operations across all aligned reads.

    Args:
        dico_sam (dict): The main dictionary containing parsed SAM data.

    Returns:
        tuple: Contains:
            - dico_statsCigar (dict): Percentage of each operation globally.
            - total_reads (int): Total number of reads processed.
    """
    cigar_operations = ['M','I','D','S','H','N','P','X','=']    # Liste standard des opérations CIGAR
    dico_cigarPerRead = {}                                      # Contiendra pour chaque read, un sous-dictionnaire comptant les bases associées à chaque opération CIGAR
    dico_opCounter = {op: 0 for op in cigar_operations}         # Accumulateur global comptant toutes les opérations rencontrées sur tout l’échantillon
    dico_statsCigar = {}                                        # Dictionnaire des statistiques globales des opérations CIGAR (en pourcentage)
    total_bases = 0                                             # Somme des bases pour toutes les opérations, tous alignements confondus
    total_reads = 0                                             # Compteur du nombre total d'alignements analysés

    for QNAME, read_list in dico_sam.items():                   # Pour chaque read de chaque QNAME
        for read in read_list:
            total_reads += 1
            read_id = total_reads                               # Création d'un identifiant unique pour chaque read

            cigar_counts = cigar_decoding(read["CIGAR"])        # Appel de la fonction cigar_decoding
            dico_cigarPerRead[read_id] = cigar_counts           # Chaque alignement reçoit son propre résumé CIGAR

            for op in cigar_operations:                         # Mise à jour des compteurs
                dico_opCounter[op] += cigar_counts[op]          # On ajoute les valeurs pour chaque type d’opération
            total_bases += sum(cigar_counts.values())           # total_bases augmente du nombre total de bases de l’alignement


    for op in cigar_operations:                                 # Calcul des pourcentages globaux
        if total_bases > 0:                                     # nb de base de l'opération / total nb bases toutes opération x 100
            dico_statsCigar[op] = round(dico_opCounter[op] * 100.0 / total_bases, 2)
        else:
            dico_statsCigar[op] = 0.0                           # Evite le bug de la division par zéro

    return dico_cigarPerRead, dico_statsCigar, total_reads


# _____________________________________________________________________________________________________________________________________________________________________#
#                                                                         4. FICHIER DE SORTIE                                                                         #
# _____________________________________________________________________________________________________________________________________________________________________#


def write_summary (dico_nbReadInCat, total_reads, dico_statsCigar, dico_readsPerChr,
                  dico_posPerChr, dico_flagCount, mapq_counts, average_mapq,
                  gc_content, stats_pairs, summary_file="summary.txt"):
    """
    Writes a comprehensive analysis report to a text file.

    Args:
        dico_nbReadInCat (dict): Counts of reads per category (mapped/unmapped).
        total_reads (int): Total number of reads analyzed.
        dico_statsCigar (dict): Global percentages of CIGAR operations.
        dico_readsPerChr (dict): Read counts per chromosome.
        dico_posPerChr (dict): Alignment positions per chromosome.
        dico_flagCount (dict): Counts of each FLAG value encountered.
        mapq_counts (dict): Counts of reads per MAPQ category.
        average_mapq (float): The average MAPQ score.
        gc_content (float): The global GC percentage.
        stats_pairs (dict): Statistics on paired-end read configurations.
        summary_file (str): Output filename (default: "summary.txt").
    """

    with open(summary_file, "w") as summary:
        summary.write("=== SAM ANALYSIS REPORT ===\n\n")
        summary.write("Total reads analyzed: {}\n".format(total_reads))
        summary.write("Global GC Content: {:.2f}%\n\n".format(gc_content))

        summary.write("--- Paired-End Analysis ---\n")
        summary.write("Pairs with 1 Full Mapped & 1 Unmapped: {}\n".format(stats_pairs["OneMapped_OneUnmapped"]))
        summary.write("Pairs with 1 Full Mapped & 1 Partial:  {}\n".format(stats_pairs["OneMapped_OnePartial"]))
        summary.write("Pairs fully mapped (Both Perfect):     {}\n\n".format(stats_pairs["Properly_Paired_BothMapped"]))

        summary.write("--- Reads per category ---\n")
        for cat in ['mapped', 'partiallyMapped', 'unmapped']:
            count = dico_nbReadInCat.get(cat, 0)
            percent = count * 100.0 / total_reads if total_reads > 0 else 0.0
            summary.write("Number of reads {} : {} ({}%)\n".format(cat, count, round(percent, 2)))

        summary.write("\n--- FLAG statistics ---\n")
        summary.write("Number of reads per FLAG value:\n")
        for flag_value in sorted(dico_flagCount.keys()):            # Tri des flags par ordre croissant
            count = dico_flagCount[flag_value]
            percent = count * 100.0 / total_reads if total_reads > 0 else 0.0
            summary.write("FLAG {} : {} reads ({}%)\n".format(flag_value, count, round(percent, 2)))

        summary.write("\n--- Global CIGAR operations ---\n")
        summary.write("Match (M): {}%\n".format(dico_statsCigar.get('M', 0)))
        summary.write("Insertion (I): {}%\n".format(dico_statsCigar.get('I', 0)))
        summary.write("Deletion (D): {}%\n".format(dico_statsCigar.get('D', 0)))
        summary.write("Skipped region (N): {}%\n".format(dico_statsCigar.get('N', 0)))
        summary.write("Soft clipping (S): {}%\n".format(dico_statsCigar.get('S', 0)))
        summary.write("Hard clipping (H): {}%\n".format(dico_statsCigar.get('H', 0)))
        summary.write("Padding (P): {}%\n".format(dico_statsCigar.get('P', 0)))
        summary.write("Sequence match (=): {}%\n".format(dico_statsCigar.get('=', 0)))
        summary.write("Sequence mismatch (X): {}%\n".format(dico_statsCigar.get('X', 0)))

        summary.write("\n--- Chromosome Distribution ---\n")
        for chrom in dico_readsPerChr:
            count = dico_readsPerChr[chrom]
            summary.write("Chromosome {} : {} reads\n".format(chrom, count))

        summary.write("\n--- Position statistics per chromosome ---\n")
        for chrom, positions in dico_posPerChr.items():
            if positions:
                min_pos = min(positions)
                max_pos = max(positions)
                mean_pos = sum(positions) / len(positions)
                variance = sum((pos - mean_pos) ** 2 for pos in positions) / len(positions)
                sd_pos = math.sqrt(variance)
                summary.write("Chromosome {} : positions min={} max={} mean={:.2f} sd={:.2f}\n".format(chrom, min_pos, max_pos, mean_pos, sd_pos))
            else:
                summary.write("Chromosome {} : no mapped reads\n".format(chrom))

        summary.write("\n--- Mapping Quality (MAPQ) ---\n")
        summary.write("Average MAPQ score: {:.2f}\n".format(mapq_avg))
        summary.write("Distribution:\n")
        mapq_order = ["0 (Ambiguous/Unmapped)", "1-29 (Low Confidence)", "30+ (High Confidence)"]
        for label in mapq_order:
            count = mapq_counts.get(label, 0)
            perc = (count * 100.0 / total_reads) if total_reads > 0 else 0.0
            summary.write("  {}: {} ({:.2f}%)\n".format(label, count, perc))


# _____________________________________________________________________________________________________________________________________________________________________#
#           5. QUESTION 1 et 2 : Comment et combien de reads sont mappés ? # compter le nombre de reads en fonction du flag (colonne #2) et pour chaque flag           #
# _____________________________________________________________________________________________________________________________________________________________________#


def categorize_reads(dico_sam, categories=['all']):                     # Catégorise les reads en mappés, non mappés et partiellement mappés
    """
    Classifies reads into categories (mapped, unmapped, partially mapped) and writes them to FASTA files.

    Args:
        dico_sam (dict): The main dictionary containing parsed SAM data.
        categories (list): List of categories to process (default: ['all']).

    Returns:
        tuple: Contains:
            - dico_nbReadInCat (dict): Number of reads in each category.
            - dico_flagCount (dict): Number of occurrences for each FLAG value.
    """
    all_cats = ['mapped', 'partiallyMapped', 'unmapped']                # Toutes les catégories possibles
    if 'all' in categories:
        categories = all_cats[:]

    dico_nbReadInCat = {}                                               # Dictionnaire pour compter le nombre de reads dans chaque catégorie
    dico_fasta = {}                                                     # Dictionnaire pour stocker le nom du fichier FASTA associé à chaque catégorie
    dico_fasta_names = {}
    dico_flagCount = {}                                                 # Comptage des flags rencontrés

    for cat in categories:
        dico_nbReadInCat[cat] = 0
        fasta_name = "{}.fasta".format(cat)
        dico_fasta_names[cat] = fasta_name
        dico_fasta[cat] = open(fasta_name, "w")                         # Définit le nom du fichier FASTA correspondant [exemple : 'mapped.fasta' pour la catégorie 'mapped']

    for QNAME, read_list in dico_sam.items():                           # Parcourt chaque read du dictionnaire SAM
        for read in read_list:

            flag_info = flag_decoding(read["FLAG"])                     # Appelle la fonction flag_decoding pour décoder le FLAG SAM en un dictionnaire de booléens
            cigar_counts = cigar_decoding(read["CIGAR"])                # Comptage des bases par opération
            flag_value = read["FLAG"]
            if flag_value not in dico_flagCount:
                dico_flagCount[flag_value] = 0
            dico_flagCount[flag_value] += 1

            if 'unmapped' in categories and flag_info["is_unmapped"]:   # Vérifie si la catégorie 'unmapped' est activée et si le read n’est pas aligné (is_unmapped=True)
                dico_nbReadInCat['unmapped'] += 1                       # Incrémente le compteur 'unmapped'
                dico_fasta['unmapped'].write(">{}\n".format(QNAME))     # Ajoute le read dans le fichier FASTA correspondant
                dico_fasta['unmapped'].write("{}\n".format(read['SEQ']))
                continue

            if 'mapped' in categories and not flag_info["is_unmapped"]: # Vérifie si la catégorie 'mapped' est activée et si le read est aligné (is_unmapped=False)
                dico_nbReadInCat['mapped'] += 1
                dico_fasta['mapped'].write(">{}\n".format(QNAME))
                dico_fasta['mapped'].write("{}\n".format(read['SEQ']))

            if ('partiallyMapped' in categories and not flag_info["is_unmapped"]
                and (cigar_counts['I'] > 0 or cigar_counts['D'] > 0 or cigar_counts['S'] > 0)):
                dico_nbReadInCat['partiallyMapped'] += 1
                dico_fasta['partiallyMapped'].write(">{}\n".format(QNAME))
                dico_fasta['partiallyMapped'].write("{}\n".format(read['SEQ']))

    for cat in dico_fasta:
        dico_fasta[cat].close()

    return dico_nbReadInCat, dico_flagCount


# _____________________________________________________________________________________________________________________________________________________________________#
#     6. QUESTION 3 : Où les reads sont-ils mappés ? L'alignement est-il homogène le long de la séquence de référence ? # compter le nombre de reads par chromosome    #
# _____________________________________________________________________________________________________________________________________________________________________#


def analyze_mapping(dico_sam):
    """
    Analyzes the distribution of mapped reads across reference chromosomes.

    Args:
        dico_sam (dict): The main dictionary containing parsed SAM data.

    Returns:
        tuple: Contains:
            - dico_readsPerChr (dict): Count of reads mapped to each chromosome.
            - dico_posPerChr (dict): List of mapping start positions for each chromosome.
    """
    dico_readsPerChr = {}                                       # Compte le nombre de reads par chromosome
    dico_posPerChr = {}                                         # Liste des positions pour vérifier l'homogénéité des alignements

    for QNAME, read_list in dico_sam.items():
        for read in read_list:
            flag_info = flag_decoding(read["FLAG"])
            if flag_info["is_unmapped"]:
                continue                                        # Ignore les reads non mappés

            chrom = read["RNAME"]                               # Nom du chromosome
            POS = read["POS"]                                   # Position de début de l'alignement

            if chrom not in dico_readsPerChr:                   # Mise à jour du compteur de reads par chromosome
                dico_readsPerChr[chrom] = 0
                dico_posPerChr[chrom] = []
            dico_readsPerChr[chrom] += 1
            dico_posPerChr[chrom].append(POS)

    return dico_readsPerChr, dico_posPerChr


# _____________________________________________________________________________________________________________________________________________________________________#
#  7. QUESTION 4 : Avec quelle qualité les reads sont-ils mappés ? # compter le nb de reads pour chaque valeur de qualité ou par tranche de valeurs (score de mapping) #
# _____________________________________________________________________________________________________________________________________________________________________#


def analyze_mapq(dico_sam):
    """
    Evaluates the Mapping Quality (MAPQ) scores of the reads.

    Args:
        dico_sam (dict): The main dictionary containing parsed SAM data.

    Returns:
        tuple: Contains:
            - mapq_counts (dict): Counts of reads in defined quality tiers (Low/High).
            - mapq_avg (float): The global average MAPQ score.
    """
    mapq_counts = {
        "0 (Ambiguous/Unmapped)": 0,
        "1-29 (Low Confidence)": 0,
        "30+ (High Confidence)": 0
    }

    total_mapq = 0
    total_reads = 0

    for QNAME, read_list in dico_sam.items():
        for read in read_list:
            MAPQ = read["MAPQ"]
            total_reads += 1
            total_mapq += MAPQ

            # Catégorisation simplifiée
            if MAPQ == 0:
                mapq_counts["0 (Ambiguous/Unmapped)"] += 1
            elif MAPQ < 30:
                mapq_counts["1-29 (Low Confidence)"] += 1
            else:
                mapq_counts["30+ (High Confidence)"] += 1

    if total_reads > 0:
        mapq_avg = total_mapq / total_reads
    else:
        mapq_avg = 0.0

    return mapq_counts, mapq_avg


# _____________________________________________________________________________________________________________________________________________________________________#
#                                                                              9. Extraction des reads ”mal mappés”                                                                              #
# _____________________________________________________________________________________________________________________________________________________________________#


def analyze_pairs(dico_sam):
    """
    Analyzes paired-end reads to identify specific mapping configurations.

    Identifies pairs where:
    - One read is fully mapped and the other is unmapped.
    - One read is fully mapped and the other is partially mapped.

    Args:
        dico_sam (dict): The main dictionary containing parsed SAM data.

    Returns:
        dict: Counts for specific paired-end configurations (e.g., 'OneMapped_OneUnmapped').
    """
    stats_pairs = {
        "OneMapped_OneUnmapped": 0,
        "OneMapped_OnePartial": 0,
        "Properly_Paired_BothMapped": 0
    }

    for QNAME, read_list in dico_sam.items():

        if len(read_list) != 2:                                                 # Ignore la commande si il n'y a qu'un read/2
            continue

        r1 = read_list[0]
        r2 = read_list[1]
        flag1 = flag_decoding(r1["FLAG"])                                       # Décoder les infos pour les deux reads
        flag2 = flag_decoding(r2["FLAG"])
        cigar1 = cigar_decoding(r1["CIGAR"])
        cigar2 = cigar_decoding(r2["CIGAR"])

        is_partial1 = (cigar1['I'] > 0 or cigar1['D'] > 0 or cigar1['S'] > 0)   # Définition "Partiellement mappé" (Indels ou Clipping)
        is_partial2 = (cigar2['I'] > 0 or cigar2['D'] > 0 or cigar2['S'] > 0)

        is_full1 = (not flag1["is_unmapped"]) and (not is_partial1)             # Définition "Entièrement mappé" (Mappé ET NON Partiel)
        is_full2 = (not flag2["is_unmapped"]) and (not is_partial2)

        # --- CASE 1: One fully mapped, the other unmapped  ---
        # (R1 Full ET R2 Unmapped) OR (R1 Unmapped ET R2 Full)
        if (is_full1 and flag2["is_unmapped"]) or (flag1["is_unmapped"] and is_full2):
            stats_pairs["OneMapped_OneUnmapped"] += 1

        # --- CASE 2: One fully mapped, the other partially mapped  ---
        # (R1 Full ET R2 Partial) OR (R1 Partial ET R2 Full)
        elif (is_full1 and is_partial2 and not flag2["is_unmapped"]) or (is_partial1 and not flag1["is_unmapped"] and is_full2):
            stats_pairs["OneMapped_OnePartial"] += 1

        # --- CASE 3: Both are correctly mapped (for comparison) ---
        elif is_full1 and is_full2:
            stats_pairs["Properly_Paired_BothMapped"] += 1

    return stats_pairs


# _____________________________________________________________________________________________________________________________________________________________________#
#                                                                              10. BONUS :                                                                              #
# _____________________________________________________________________________________________________________________________________________________________________#


def calculate_GC(dico_sam):
    """
    Calculates the global GC content percentage across all read sequences.

    Args:
        dico_sam (dict): The main dictionary containing parsed SAM data.

    Returns:
        float: The percentage of G and C bases in the total sequenced bases.
    """
    nb_gc = 0
    total_bases = 0

    for QNAME, read_list in dico_sam.items():
        for read in read_list:
            sequence = read["SEQ"]
            nb_gc += sequence.count('G') + sequence.count('C')
            total_bases += len(sequence)

    if total_bases > 0:
        gc_percent = (nb_gc / total_bases) * 100.0
    else:
        gc_percent = 0.0

    return gc_percent


# _____________________________________________________________________________________________________________________________________________________________________#
#                                                                              11. MAIN :                                                                              #
# _____________________________________________________________________________________________________________________________________________________________________#


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Error: Missing SAM file.")
        sys.exit(1)

    sam_file = sys.argv[1]

    mode = sys.argv[2] if len(sys.argv) > 2 else "full"         # Argument 2 : full, cigar, mapping, fasta (full par défaut)

    if len(sys.argv) > 3:                                       # Argument 3 : Choix des catégories FASTA (ex: "unmapped,partiallyMapped,mapped")
        cats_arg = sys.argv[3]
        fasta_categories = cats_arg.split(",")                  # Transformation de la chaîne "mapped,unmapped" en liste ['mapped', 'unmapped']
    else:
        fasta_categories = ['all']

    print("--- Analysis begins (Mode: {}) ---".format(mode))

    print("Reading SAM file...")
    dico_sam = read_sam(sam_file)
    total_reads = sum(len(read_list) for read_list in dico_sam.values())

    dico_statsCigar = {}                                        # Initialisation des variables pour limiter les erreurs
    stats_pairs = {"OneMapped_OneUnmapped": 0, "OneMapped_OnePartial": 0, "Properly_Paired_BothMapped": 0}
    dico_nbReadInCat = {}
    dico_readsPerChr = {}
    dico_posPerChr = {}
    dico_flagCount = {}
    mapq_counts = {}
    mapq_avg = 0
    gc_global = 0

    # --- CIGAR ---
    if mode in ["cigar", "full"]:
        print("Analyzing CIGAR...")
        dico_statsCigar, _ = analyze_cigar(dico_sam)
        if mode == "cigar":
            print("\nCIGAR results :")
            for letter, number in dico_statsCigar.items():
                print("  {}: {}%".format(letter, number))

    # --- MAPPING ---
    if mode in ["mapping", "full"]:
        print("Mapping Analysis (Quality, GC content, Chromosomes)...")
        mapq_counts, mapq_avg = analyze_mapq(dico_sam)
        dico_readsPerChr, dico_posPerChr = analyze_mapping(dico_sam)
        gc_global = calculate_GC(dico_sam)
        if mode == "mapping":
            print("\nGC Content: {:.2f}%".format(gc_global))
            print("Average MAPQ: {:.2f}".format(mapq_avg))

    # --- FASTA & PAIRES ---
    if mode in ["fasta", "full"]:
        print("FASTA file generation for : {} ...".format(fasta_categories))
        dico_nbReadInCat, dico_flagCount = categorize_reads(dico_sam, categories=fasta_categories)
        stats_pairs = analyze_pairs(dico_sam)
        if mode == "fasta":
            print("Done! FASTA file(s) generated.")

    # --- RAPPORT ---
    if mode == "full":
        print("Writing the complete report 'summary.txt'...")
        write_summary(dico_nbReadInCat, total_reads, dico_statsCigar, dico_readsPerChr, dico_posPerChr, dico_flagCount, mapq_counts, mapq_avg, gc_global, stats_pairs)
        print("Success! Check 'summary.txt")
        print("ദി(˵•̀ᴗ-˵)✧")
