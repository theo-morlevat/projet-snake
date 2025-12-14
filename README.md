#Fichier README 

Nom du projet : Projet Snake / Analyseur automatisé de fichiers SAM 

Autheur: Charlotte Pariente et Théo Morlevat 
theom1907@gmail.com
charlotte.pariente@gmail.com 

## Vue d'ensemble :  

Le projet Snake à pour objectif de permettre l’analyse d’un fichier SAM(Séquences Alignées Mappées) et d’obtenir les résultats en un résumé, dans un environnement de laboratoire. Il a été pensé de sorte à pouvoir travailler sur les dossiers biologiques (fichier SAM) à distance. Cela permet de stocker les scripts dans un dossier séparé des données évitant de polluer les données. Ce script se veut utilisable et compréhensible pour des biologistes.

### caractéristiques
- **Analyse complète** :        Statistiques globales, qualité de l'alignement, analyse des paires de lectures
- **Parsing robuste** :         Décodage des champs CIGAR et FLAG conformes aux spécifications SAM officielles
- **Extraction de séquences** : Génération automatique de fichiers FASTA pour les reads non mappés et partiellement alignés
- **Architecture modulaire** :  Séparation stricte entre code source et données expérimentales
- **interactif** :              Interface conviviale adaptée aux biologistes non informaticiens 

## Architecture du système

Le système repose sur deux scripts, un script bash et un script python, situés dans un **dossier centralisé** :

| Composant            | Type     | Rôle                                                                                 |
|----------------------|----------|--------------------------------------------------------------------------------------|
| `analyse_sam.py`     | Python 3 | Moteur d'analyse : calculs statistiques, parsing CIGAR/FLAG, génération des rapports |
| `lanceur_bioinfo.sh` | Bash     | Interface utilisateur : interaction, gestion des permissions, exécution sécurisée    |

### Arborescence type

/racine/
├── bio-info/                      # Dossier des scripts (Admin)
│   ├── analyse_sam.py
│   ├── lanceur_bioinfo.sh
│   └── README.md
│
└── home/user/data/                # Dossier du biologiste (Utilisateur)
    ├── experience_1.sam
    └── (Fichiers de sortie générés ici)

**Principe fondamental** : Les scripts restent dans `bio-info/` et ne sont jamais copiés de façon permanente dans les dossiers de données. Une copie temporaire du script python est créée pendant l'exécution dans le fichier contenant le fichier sam. La localisation d'exécution des commandes est déplacé dans le même fichier afin de lancer le script python copié sur les données, puis il supprimée à la fin de l'exécution.

## Prérequis

- bash   

- Python 3.x 

 
## Installation

Télécharger le fichier Python script.py et le fichier script.sh à partir de git. 

Lien htpps du git 

Le script utilise les packages 

-os 

-re 

... 

 

Utiliser le script : 

Donnée d’entrée : 

-un fichier sam, qui ne doit pas avoir de ligne vide et qui doit être coté pour éviter les problèmes des espaces 

-le chemin menant au fichier sam 

./script.sh chemin/menant/au/fichier.sam “nomdufichier.sam” 

Paramètres “basiques”: 

-h ou –-help 

-i ou –-input 

-o ou --output 

 

Les paramètres spécifiques à l’analyse des données seront directements demandé dans le terminal via une saisie au clavier. 

Penser à autoriser le droit d’exécution des fichiers avec chmod 

 

Fonctionnement du script : 

Le script bash vérifie la présence d’un fichier sam conforme et lance le fichier python. Le script python permet d’analyser un fichier SAM. Pour cela il filtre les reads selon le FLAG et la qualité (MAPQ), et produit des statistiques, sur les reads mappés, de distribution par chromosome et de qualité de mapping. 

Le script bash lancera lui-même le script python 

Paramètres : demandé directement dans le terminal 

Sorties : 

- only_unmapped.fasta contient les séquences des reads non mappés 

- summary_unmapped.txt donne le nombre de reads non mappés 

-partiallymapped 

 - flags_distribution.csv : répartition des flags 

 - chrom_distribution.csv : répartition par chromosome 

 - mapq_distribution.csv : distribution des scores MAPQ 

 

Script Python 

Inclure le script complet, bien commenté. 

Vérifier que tous les chemins sont relatifs ou paramétrables, pour faciliter l’utilisation par un autre utilisateur. 

Ajouter éventuellement des options en ligne de commande (via argparse) pour rendre le script flexible. 
