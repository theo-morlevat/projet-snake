## README FILE

Project name : Snake Project / Automatised analyser of SAM file

## Autors and academic context

**Developers** : Marie-Charlotte PARIENTE & Théo MORLEVAT  
**Academic framework** : System project Bio-Info - 2025-2026 - HAI724I  
**Establishment** : Faculté des Sciences - Université de Montpellier  
**Specialization** : Paired-end sequencing data analysis

## Contacts :
- theo.morlevat@etu.umontpellier.fr
- marie-charlotte.pariente@etu.umontpellier.fr

---

## Global view :

The Snake project aims to facilitate sequence alignment file analysis and generate a summary of the results usable in the laboratory. It was designed to allow the processing of long-range **SAM (Sequence Alignment/Map)** files, thus offering the possibility of separating computer tools from biological data and to ensure that no scripts pollute the experimental files. These scripts were designed to remain accessible and understandable to biologists, without requiring advanced programming skills.

### Features
- **Complete analysis** : Overall statistics, alignment quality, reading pair analysis.
- **Robust parsing** : Decoding of CIGAR and FLAG fields in accordance with official SAM specifications.
- **Sequence extraction** : Automatic generation of files in FASTA format (separation of mapped, unmapped and partially aligned reads).
- **Modular architecture** : Strict separation between source code and experimental data.
- **User interaction** : Interactive options suitable for biologists without advanced computer skills.

**Note** : The authors chose to comment their code extensively in French to make it accessible to French-speaking biologists. In addition, the scripts use explicit variable names and docstrings (Python) in English, thus facilitating understanding and use by the international scientific community.

---

## Architecture du système

Le système repose sur deux scripts, un script bash et un script python, situés dans un **dossier centralisé** :

| Composant            | Type     | Rôle                                                                                 |
|----------------------|----------|--------------------------------------------------------------------------------------|
| `analyse_sam.py`     | Python 3 | Moteur d'analyse : calculs statistiques, parsing CIGAR/FLAG, génération des rapports |
| `launcher_bioinfo.sh` | Bash     | Interface utilisateur : interaction, gestion des permissions, exécution sécurisée    |

### Arborescence type
```
/racine/
├── bio-info/                      # Dossier des scripts (Admin)
│   ├── analyse_sam.py
│   ├── launcher_bioinfo.sh
│   ├── LISEZ-MOI.md
│   └── README.md
│
└── home/user/data/                # Dossier du biologiste (Utilisateur)
    ├── experience_1.sam
    └── (Fichiers de sortie générés ici)
```
**Principe fondamental** : Les scripts restent dans `bio-info/` et ne sont jamais copiés de façon permanente dans les dossiers de données.
Lors de l’exécution, une copie temporaire du script Python est créée dans le même répertoire que le fichier SAM à analyser. Les commandes sont alors exécutées dans ce répertoire, garantissant que le script agit directement sur les données locales. Une fois l’exécution terminée, la copie temporaire du script est automatiquement supprimée.

---

## Spécifications techniques

### Prérequis système

| Composant | Minimum | Recommandé |
|-----------|---------|------------|
| Python    | 3.0     | 3.6+       |
| Bash      | 4.0     | 5.1+       |

### Dépendances Python

```
# Bibliothèques standard uniquement
- re (expressions régulières)
- sys (arguments système)
- math (fonctions mathématiques)
```

**Avantage** : Aucune installation de librairie externe requise. Fonctionne avec une installation Python standard.

### Limitations connues

- **Taille de fichier** : Optimisé pour SAM < 2 GB (adaptation recommandée pour les fichiers plus volumineux)
- **Encodage** : Suppose un encodage UTF-8 des fichiers SAM
- **Format** : Attend un format SAM standard (avec en-têtes @HD, @SQ recommandés, sans lignes vides)

---

## Installation

### Téléchargement des scripts
Télécharger le fichier Python analyse_sam.py et le fichier launcher_bioinfo.sh à partir de git.

```
https://github.com/theo-morlevat/projet-snake.git
```

Il est recommandé de placer ces scripts dans un dossier (exemple : bio-info) dont vous connaissez le chemin.

#### Rendre le script Bash exécutable

```bash
chmod +x launcher_bioinfo.sh
```

**Note** : Le script Python n'a pas besoin d'être exécutable, il est appelé via `python3` par le script Bash.

---

## Guide d'utilisation

### Syntaxe

```bash
/chemin/vers/bio-info/launcher_bioinfo.sh <DOSSIER_DONNEES> <FICHIER_SAM>
```
### Arguments

| Argument            | Type           | Description                                                               |
|---------------------|----------------|---------------------------------------------------------------------------|
| `<DOSSIER_DONNEES>` | Chemin         | Répertoire contenant vos fichiers de données (chemin absolu ou relatif)   |
| `<FICHIER_SAM>`     | Nom de fichier | Nom du fichier `.sam` à analyser (doit être situé dans `DOSSIER_DONNEES`) |

### Exemples concrets

- En partant du principe que vous vous trouvez dans votre session ~

```bash
~/bio-info/launcher_bioinfo.sh ~/mes_experiences/exp_1 mon_alignement.sam
```
- À partir du moment où vous connaissez les chemins des scripts et du fichier sam à analyser, vous pouvez exécuter cette commande n'importe où.
- Les résultats seront générés dans ~/mes_experiences/exp_1

### Paramètres en argument de launcher_bioinfo.sh

```
-h ou –-help : paramètre expliquant commant utiliser le script et les paramètres possibles.

-i ou –-input : paramètre explicitant quel données d'entrées il faut saisir et un exemple.

-o ou --output : paramètre donnant les sortie attendues à la fin du script.
```

 ---

## Menu interactif

Une fois le script lancé, vous serez invité à choisir le type d'analyse :

### Options disponibles

**1. Analyse COMPLÈTE**
- Rapport synthétique complet (`summary.txt`)
- Calcul du pourcentage GC global
- Analyse des paires de lectures (R1/R2), FLAG, CIGAR, distribution chromosomique et MAPQ
- Génération de fichier(s) `.fasta` en fonction des besoins de l'utilisateur
- **Durée** : Modérée

**2. Analyse CIGAR**
- Extraction et décodage des chaînes CIGAR
- Affichage directe des résultats dans le terminal (aucun fichier de sortie)
- **Durée** : Rapide

**3. Analyse MAPPING**
- Qualité de l'alignement (MAPQ), contenu %GC et couverture par chromosome
- Affichage directe des résultats dans le terminal (aucun fichier de sortie)
- **Durée** : Rapide

**4. Extraction FASTA**
- Génération de fichier(s) `.fasta` en fonction des besoins de l'utilisateur
- 'unmapped' : Reads non mappés (FLAG = 4)
- 'partiallyMapped' : Reads partiellement alignés (avec indels ou clipping)
- 'mapped' : Reads parfaitement alignés
- 'all' : Génération des 3 fichiers cités ci-dessus
- **Durée** : Rapide à modérée

**Note** : Les durées d'exécutions sont proportionnelles à la taille du fichier d'entrée

### Exemple d'interaction

```
Verifications completed
This script could work on all data or on specifics needs. You want to work on : 'full', 'cigar', 'mapping', 'fasta'
full (donnée entrée dans la console)
You want to work on : 'mapped', 'partiallyMapped', 'unmapped', 'all'?
all (donnée entrée dans la console)
Analysis in progress...
--- Analysis begins (Mode: full) ---
Reading SAM file...
Analyzing CIGAR...
Mapping Analysis (Quality, GC content, Chromosomes)...
FASTA file generation for : ['all'] ...
Writing the complete report...
Success! Check 'summary.txt'
ദി(˵•̀ᴗ-˵)✧
Analysis successfully completed
```
 ---
Tous les résultats sont générés **directement dans le dossier de données** fourni en argument.
Ce script  la possibilité de créer 4 fichiers différents.

| Fichier                 | Type  | Généré par                         | Description                                                                  |
|-------------------------|-------|------------------------------------|------------------------------------------------------------------------------|
| `summary.txt`           | Texte | Analyse COMPLÈTE                   | Rapport synthétique contenant : statistiques globales, qualité d'alignement, analyse des paires, distribution par chromosome, contenu GC.|
| `unmapped.fasta`        | FASTA | Analyse COMPLÈTE, Extraction FASTA | Séquences ADN des reads n'ayant pas pu être alignés (FLAG 4)                 |
| `partiallyMapped.fasta` | FASTA | Analyse COMPLÈTE, Extraction FASTA | Séquences alignées mais présentant des indels, clipping ou cigar complexe    |
| `mapped.fasta`          | FASTA | Analyse COMPLÈTE, Extraction FASTA | Séquences parfaitement alignées (sans mutations apparentes)                  |

### Format du fichier `summary.txt`

```
=== SAM ANALYSIS REPORT ===

Total reads analyzed: 2256936
Global GC Content: 22.43%

--- Paired-End Analysis ---
Pairs with 1 Full Mapped & 1 Unmapped: 9
Pairs with 1 Full Mapped & 1 Partial:  156
Pairs fully mapped (Both Perfect):     439

--- Reads per category ---
Number of reads mapped : 119220 (5.28%)
Number of reads partiallyMapped : 87494 (3.88%)
Number of reads unmapped : 2137716 (94.72%)

--- FLAG statistics ---
Number of reads per FLAG value:
FLAG 65 : 166 reads (0.01%)
FLAG 69 : 154 reads (0.01%)
FLAG 73 : 3098 reads (0.14%)
FLAG 77 : 1066875 reads (47.27%)
...

--- Global CIGAR operations ---
Match (M): 37.91%
Insertion (I): 0.0%
Deletion (D): 0.0%
Skipped region (N): 0.0%
Soft clipping (S): 41.22%
Hard clipping (H): 20.85%
Padding (P): 0.0%
Sequence match (=): 0.0%
Sequence mismatch (X): 0.0%

--- Chromosome Distribution ---
Chromosome NC_045512.2 : 119220 reads

--- Position statistics per chromosome ---
Chromosome NC_045512.2 : positions min=7 max=29885 mean=16409.33 sd=9881.18

--- Mapping Quality (MAPQ) ---
Average MAPQ score: 3.14
Distribution:
  0 (Ambiguous/Unmapped): 2138292 (94.74%)
  1-29 (Low Confidence): 389 (0.02%)
  30+ (High Confidence): 118255 (5.24%)
```
---

## Fonctionnement du script

### Flux d'exécution du script Bash

Pour garantir une séparation stricte entre code source et données, le script Bash suit cette logique :

1. **Vérification des arguments** : Contrôle de la présence de 2 arguments
2. **Validation des fichiers** : Vérification de l'existence du dossier et du fichier SAM
3. **Déplacement sécurisé** : Changement du répertoire courant vers le dossier de données (`cd`)
4. **Copie temporaire** : Copie du script Python dans le dossier de données
5. **Exécution** : Lancement du script Python avec les paramètres choisis
6. **Nettoyage** : Suppression immédiate de la copie du script Python
7. **Rapport** : Affichage du statut final et des fichiers générés

### Architecture du script Python

- **read_sam** : Analyse le fichier SAM et organise les lectures par leur nom de requête (QNAME).
- **flag_decoding** : Décode les FLAGs bit à bit en un dictionnaire de booléens
- **analyze_cigar** : Analyse les CIGAR, comptabilise les bases par type d’opération et produit des statistiques globales sur l’ensemble des lectures alignées
- **categorize_reads** : Classe les reads en catégories (alignées, non alignées, partiellement alignées)
- **Génération FASTA** : Extraction du QNAME et des séquences en fonction des options choisies
- **analyze_mapping** : Analyse la distribution des reads cartographiées sur les chromosomes de référence
- **analyze_mapq** : Classe les reads en trois catégories, évalue les scores de qualité de mapping des lectures
- **analyze_pairs** : Analyse les reads "paired-end" pour identifier les configurations de mapping spécifiques
- **calculate_GC** : Calcule le pourcentage global de contenu GC sur l'ensemble des séquences lues
- **write_summary** : Rédige un rapport d'analyse complet dans un fichier texte

---

## Licence

Ce projet est distribué sous licence **libre de droit copyleft**. Vous êtes autorisé à :

- Utiliser le code à des fins académiques et de recherche
- Modifier le code pour adapter à vos besoins
- Redistribuer le code modifié, à condition de mentionner les modifications

**Obligations** : Toute redistribution doit inclure cette mention de licence et le nom du ou des auteurs originels.

---

**Dernière mise à jour** : Décembre 2025  
**Version du LISEZ-MOI** : 1.0
