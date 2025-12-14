# Fichier README 

Nom du projet : Projet Snake / Analyseur automatisé de fichiers SAM 

## Auteurs et contexte académique

**Développeurs** : Marie-Charlotte PARIENTE & Théo MORLEVAT<br/>
**Cadre académique** : Projet Système Bio-Info - 2025-2026 - HAI724I  
**Établissement** : Faculté des Sciences - Université de Montpellier  
**Spécialisation** : Analyse de données de séquençage paired-end

## Contact par:
- theom1907@gmail.com
- charlotte.pariente@gmail.com 

---

## Vue d'ensemble :  

Le projet Snake à pour objectif de permettre l’analyse d’un fichier SAM(Séquences Alignées Mappées) et d’obtenir les résultats en un résumé, dans un environnement de laboratoire. Il a été pensé de sorte à pouvoir travailler sur les dossiers biologiques (fichier SAM) à distance. Cela permet de stocker les scripts dans un dossier séparé des données évitant de polluer les données. Ce script se veut utilisable et compréhensible pour des biologistes.

### Caractéristiques
- **Analyse complète** :        Statistiques globales, qualité de l'alignement, analyse des paires de lectures
- **Parsing robuste** :         Décodage des champs CIGAR et FLAG conformes aux spécifications SAM officielles
- **Extraction de séquences** : Génération automatique de fichiers FASTA pour les reads non mappés et partiellement alignés
- **Architecture modulaire** :  Séparation stricte entre code source et données expérimentales
- **interactif** :              Interface conviviale adaptée aux biologistes non informaticiens 

---

## Architecture du système

Le système repose sur deux scripts, un script bash et un script python, situés dans un **dossier centralisé** :

| Composant            | Type     | Rôle                                                                                 |
|----------------------|----------|--------------------------------------------------------------------------------------|
| `analyse_sam.py`     | Python 3 | Moteur d'analyse : calculs statistiques, parsing CIGAR/FLAG, génération des rapports |
| `lanceur_bioinfo.sh` | Bash     | Interface utilisateur : interaction, gestion des permissions, exécution sécurisée    |

### Arborescence type

/racine/<br/>
├── bio-info/                      # Dossier des scripts (Admin)<br/>
│   ├── analyse_sam.py<br/>
│   ├── lanceur_bioinfo.sh<br/>
│   └── README.md<br/>
│<br/>
└── home/user/data/                # Dossier du biologiste (Utilisateur)<br/>
    ├── experience_1.sam<br/>
    └── (Fichiers de sortie générés ici)<br/>

**Principe fondamental** : Les scripts restent dans `bio-info/` et ne sont jamais copiés de façon permanente dans les dossiers de données. Une copie temporaire du script python est créée pendant l'exécution dans le fichier contenant le fichier sam. La localisation d'exécution des commandes est déplacé dans le même fichier afin de lancer le script python copié sur les données, puis il supprimée à la fin de l'exécution.

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
- **Format** : Attend un format SAM standard (avec en-têtes @HD, @SQ recommandés)

---

## Installation

### Téléchargement des scripts
Télécharger le fichier Python analyse_sam.py et le fichier lanceur_bioinfo.sh à partir de git. 

[Lien htpps du git ](https://github.com/theo-morlevat/projet-snake.git)

Il est recommandé de placer ces scripts dans un dossier (exemple : bio-info) dont vous connaissez le chemin.

#### Rendre le script Bash exécutable

```bash
chmod +x lanceur_bioinfo.sh
```

**Note** : Le script Python n'a pas besoin d'être exécutable, il est appelé via `python3` par le script Bash.

---

## Guide d'utilisation

### Syntaxe

```bash
/chemin/vers/bio-info/lanceur_bioinfo.sh <DOSSIER_DONNEES> <FICHIER_SAM>
```
### Arguments

| Argument            | Type           | Description                                                               |
|---------------------|----------------|---------------------------------------------------------------------------|
| `<DOSSIER_DONNEES>` | Chemin         | Répertoire contenant vos fichiers de données (chemin absolu ou relatif)   |
| `<FICHIER_SAM>`     | Nom de fichier | Nom du fichier `.sam` à analyser (doit être situé dans `DOSSIER_DONNEES`) |

Faite attention le fichier sam `FICHIER_SAM` ne doit pas avoir de ligne vide, cela peut entraîner une erreur.

### Exemples concrets

- En partant du principe que vous vous trouvez dans votre session ~

```bash
~/bio-info/lanceur_bioinfo.sh ~/mes_experiences/exp_1 mon_alignement.sam
```
- À partir du moment que vous connaissez les chemins des scripts et du fichier sam à analyser, vous pouvez exécuter cette commande n'importe où.
- Les résultats seront générés dans ~/mes_experiences/exp_1

### Paramètres en argument de lanceur_bioinfo.sh

-h ou –-help : paramètre expliquant commant utiliser le script et les paramètres possibles.

-i ou –-input : paramètre explicitant quel données d'entrées il faut saisir et un exemple.

-o ou --output : paramètre donnant les sortie attendues à la fin du script.

 ---

## Menu interactif

Une fois le script lancé, vous serez invité à choisir le type d'analyse via un menu numéroté :

### Options disponibles

**1. Analyse COMPLÈTE**
- Rapport synthétique complet (`summary.txt`)
- Calcul du pourcentage GC global
- Analyse des paires de lectures (R1/R2)
- Génération de fichiers FASTA pour les reads non mappés
- Statistiques par chromosome/contig
- **Durée** : Modérée (proportionnelle à la taille du fichier)

**2. Analyse CIGAR**
- Extraction et décodage des chaînes CIGAR
- Pourcentages d'insertions, délétions et clipping
- **Durée** : Rapide
- **Cas d'usage** : Évaluation rapide de la qualité des alignements

**3. Analyse MAPPING**
- Qualité de l'alignement (MAPQ)
- Couverture par chromosome
- Contenu GC des reads mappés
- Distribution des longueurs de reads
- **Durée** : Rapide

**4. Extraction FASTA**
- Génération des fichiers `.fasta` uniquement
- Reads non mappés (FLAG = 4)
- Reads partiellement alignés (avec indels ou clipping)
- Reads parfaitement alignés (optionnel)
- **Durée** : Très rapide

### Exemple d'interaction

```
=== Analyseur de Fichiers SAM ===
1) Analyse COMPLÈTE
2) Analyse CIGAR
3) Analyse MAPPING
4) Extraction FASTA
Choisissez une option [1-4] : 1

Analyse en cours... (exp_1/mon_alignement.sam)
✓ Analyse terminée avec succès
Fichiers générés : summary.txt, unmapped.fasta, partiallyMapped.fasta
```

 ---

## Fichiers de sortie

Tous les résultats sont générés **directement dans le dossier de données** fourni en argument.
Ce script  la possibilité de créer 4 fichiers différents.

| Fichier                 | Type  | Généré par                         | Description                                                                  |
|-------------------------|-------|------------------------------------|------------------------------------------------------------------------------|
| `summary.txt`           | Texte | Analyse COMPLÈTE                   | Rapport synthétique contenant : statistiques globales, qualité d'alignement, |
|                         |       |                                    |  analyse des paires, distribution par chromosome, contenu GC.                |
| `unmapped.fasta`        | FASTA | Analyse COMPLÈTE, Extraction FASTA | Séquences ADN des reads n'ayant pas pu être alignés (FLAG 4)                 |
| `partiallyMapped.fasta` | FASTA | Analyse COMPLÈTE, Extraction FASTA | Séquences alignées mais présentant des indels, clipping ou cigar complexe    |
| `mapped.fasta`          | FASTA | Extraction FASTA (optionnel)       | Séquences parfaitement alignées (sans mutations apparentes)                  |

### Format du fichier `summary.txt`

```
=== SAM Analysis Report ===
File: mon_alignement.sam
Timestamp: 2025-12-13 18:45:23

--- Global Statistics ---
Total reads: 1,234,567
Mapped reads: 1,210,345 (98.15%)
Unmapped reads: 24,222 (1.85%)

--- Alignment Quality ---
Mean MAPQ: 42.3
Median MAPQ: 45
...

--- Pairwise Analysis ---
Properly paired: 1,195,234 (96.82%)
Singleton: 15,111 (1.22%)
...

--- Per-Chromosome Coverage ---
chr1: 45,234 reads (3.89%)
chr2: 41,567 reads (3.57%)
...
```

---
 
## Fonctionnement du script
## ⚙️ Fonctionnement technique

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

- **Parsing SAM** : Lecture ligne par ligne des alignements, extraction des champs obligatoires
- **Décodage CIGAR** : Interprétation des opérations de cigar (M, I, D, S, H, etc.)
- **Décodage FLAG** : Analyse binaire des FLAGs SAM pour classifier les reads
- **Statistiques** : Agrégation par chromosome, calcul des moyennes et percentiles
- **Génération FASTA** : Extraction des séquences (champ 10) en fonction de la classification

---

**Dernière mise à jour** : Décembre 2025  
**Version du README** : 1.0
