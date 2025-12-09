Fichier README 

Nom du projet : Projet Snake / Analyse de fichiers SAM 

Autheur: Charlotte Pariente et Théo Morlevat 
mettre les mails

Description :  

Le projet Snake à pour objectif de permettre l’analyse d’un fichier SAM(Séquences Alignées Mappées) et d’obtenir les résultats en un résumé. Il permet d’obtenir différentes informations mais aussi d’extraire les séquences qui seraient mal alignées. Ces informations peuvent portent sur différents indicateurs du fichier SAM (FLAG, CIGAR, RNAME...), les fréquences des reads selon certains indicateurs et l’obtention de tableaux résumant les données. 

Prérequis : 

- bash   

- Python 3.x 

 

Installation : 

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
