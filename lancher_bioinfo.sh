clear #On commence par effacer la console

if [ $1 == --help ] || [ $1 == -h ]; then  #option help, détaille le fonctionnement du script.
       echo -e " The Bash script will copy the pyhton script at the destination of the .sam file. Then ... "
       exit 1
fi

if [ $1 == --output ] || [ $1 == -o ]; then  #option help, détaille le fonctionnement du script.
       echo -e " The Bash script will copy the pyhton script at the destination of the .sam file. Then ... "
       exit 1
fi

if [ $1 == --input ] || [ $1 == -i ]; then  #option help, détaille le fonctionnement du script.
       echo -e " The Bash script will copy the pyhton script at the destination of the .sam file. Then ... "
       exit 1
fi

cp analyse_sam.py "$1"analyse_sam2.py # Le script .py se situe dans le même fichier que le script actuel. On copie le script .py dans dans le dossier où se situe le fichier sam. Le script est copié sous un autre nom si le fichier sam se trouve dans le même dossier pour éviter de supprimer le fichier .py d'origine.
cd "$1" #On déplace ensuite l'endroit d'exécution des actions dans le dossier contenant le fichier .sam. Ainsi on pourra exploiter le fichier avec le script .py.

error="" #On initialise une variable vide afin de contenir les différents messages d'erreurs.
last-extension="${2##*.}" #On stock la dernière extension du nom du fichier dans la variable last-extension


if [ -z "$2" ] || [ ! -e "$2" ] || [ ! -f "$2" ] || [[ ! -s "$2" ]] || [ $last-extension != sam ]; then #On vérifie s'il n'y a pas d'érreur du à: un argument manquant, un fichier absent, un argument ne correspondant pas à un fichier régulier, un fichier vide ou n'ayant pas l'extension .sam.
        [ -z "$2" ]   &&  error+="Error: nom de fichier manquant.\n"  # && Et un opérateur permettant de lancer une commande que si la commande précédante s'exécute
        [ ! -e "$2" ] &&  error+="Error: $2 n'est pas présent dans le dossier.\n"
        [ ! -f "$2" ] &&  error+="Error: $2 n'est pas un fichier régulier.\n"
        [ ! -s "$2" ] &&  error+="Error: $2 est vide.\n"
        [[ $last-extension != sam ]] && error+="Error: $2 n'est pas un fichier sam."
        echo -e "$error" #On affiche les différents erreurs liées à l'exécution de la commande.
        exit 1 #Si il y a une erreur alors le programme s'arrête
else
        echo "Les vérifications sont terminées" #Sinon on averti l'utilisateur que l'on va pouvoir travailler sur le fichier.
fi


#read = lire.clavier
echo "=== Analyseur de Fichiers SAM ===
1) Analyse COMPLÈTE
2) Analyse CIGAR
3) Analyse MAPPING
4) Extraction FASTA
Choisissez une option [1-4] : 1

Analyse en cours... (exp_1/mon_alignement.sam)
✓ Analyse terminée avec succès
Fichiers générés : summary.txt, unmapped.fasta, partiallyMapped.fasta"
read answer 

if [ $all == "1" ] || [ 
then
          python3 script2.py $2
else
          param=""
          echo "You want to work on: 'mapped-reads', 'partially-mapped-reads', 'unmapped-reads', 'all'? "
          read mapped
          if [[ $mapped == "mapped-reads" ]] || [[ $mapped == "partially-mapped-reads" ]] || [[ $mapped == "unmapped-reads" ]] || [[ $mapped ==  "all" ]]
          then
            param+="$mapped"
          else
            echo "Error: you didn't write well parameters"
            exit 1
          fi
          echo " You want to work on: 'reads-number' or 'percentage'? "
          read type
          if [[ $type == "reads-number" ]] || [[ $type == percentage ]]
          then
            param+="$mapped"
          else
            echo "Error: you didn't write well parameters"
            exit 1
          fi
          echo "$param"

fi


rm script2.py
