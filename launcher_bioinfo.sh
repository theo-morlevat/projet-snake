clear #On commence par effacer la console

if [ $1 == --help ] || [ $1 == -h ]; then  #option help, détaille le fonctionnement du script.
       echo -e "Usage: /path/lancher_bioinfo.sh [path/directory] [SAM_FILE]\nAnalyse a sam file to produce fasta file with specifics reads and/ or a summary\n \nListe of options\n -i, --input give informations about input\n -o, --output  give names and types of outputs"
       exit 1 # arrete l'execution du programme
fi

if [ $1 == --input ] || [ $1 == -i ]; then  #option input, détaille le fonctionnement du script.
       echo -e "This command need a first argument, a path wich lead to the directory which contain the sam file.\nThe second argument is the name of your sam file.\nAn exemple: ~/bio-info/lancher_bioinfo.sh ~/my_experiments/exp_1 my_alignement.sam"
       exit 1
fi

if [ $1 == --output ] || [ $1 == -o ]; then  #option output, donne une explication des données d'entrée et un exemple.
       echo -e "This programme can output 4 differents files:\nsummary.txt : synthetic rapport\nunmapped.fasta : sequencies of unmapped reads\npartiallyMapped.fasta : sequencies of partially mapped reads\nmapped.fasta : sequencies of corrected mapped reads"
       exit 1
fi

cp analyze_sam.py "$1"analyze_sam2.py #Le script .py se situe dans le même fichier que le script actuel. On copie le script .py dans dans le dossier où se situe le fichier sam. Le script est copié sous un autre nom si le fichier sam se trouve dans le même dossier pour éviter de supprimer le fichier .py d'origine.
cd "$1" #On déplace ensuite l'endroit d'exécution des actions dans le dossier contenant le fichier .sam. Ainsi on pourra exploiter le fichier avec le script .py.


error="" #On initialise une variable vide afin de contenir les différents messages d'erreurs.
lastextension="${2##*.}" #On stock la dernière extension du nom du fichier dans la variable last-extension


if [ -z "$2" ] || [ ! -e "$2" ] || [ ! -f "$2" ] || [[ ! -s "$2" ]] || [ $lastextension != sam ]; then #On vérifie s'il n'y a pas d'érreur du à: un argument manquant, un fichier absent, un argument ne correspondant pas à un fichier régulier, un fichier vide ou n'ayant pas l'extension .sam.
        [ -z "$2" ]   &&  error+="Error: nom de fichier manquant.\n"  # && Et un opérateur permettant de lancer une commande que si la commande précédante s'exécute
        [ ! -e "$2" ] &&  error+="Error: $2 n'est pas présent dans le dossier.\n" #on affiche alors un message en lien avec l'erreur
        [ ! -f "$2" ] &&  error+="Error: $2 n'est pas un fichier régulier.\n"
        [ ! -s "$2" ] &&  error+="Error: $2 est vide.\n"
        [[ $lastextension != sam ]] && error+="Error: $2 n'est pas un fichier sam."
        echo -e "$error" #On affiche les différents erreurs liées à l'exécution de la commande.
        exit 1 #Si il y a une erreur alors le programme s'arrête
else
        echo "Verifications completed" #Sinon on averti l'utilisateur que l'on va pouvoir travailler sur le fichier.
fi


echo "This script could work on all data or on specifics needs. You want to work on : 'full', 'cigar', 'mapping', 'fasta'" # affiche un message demandant l'analyse a réaliser
read parameter # l'utilisateur entre la valeur dans la console, la valeur est stocké dans la variable param

if [[ $parameter == "full" ]] || [[ $parameter == "cigar" ]] || [[ $parameter == "mapping" ]] || [[ $parameter ==  "fasta" ]]; # on verifie que les données entrées sont correct
then
          if [[ $parameter == "cigar" ]] || [[ $parameter == "mapping" ]];
          then
            echo "Analysis in progress..."
            python3 analyze_sam2.py $2 $parameter
            echo -e "Analysis successfully completed"
          else
            echo "You want to work on : 'mapped', 'partiallyMapped', 'unmapped', 'all'? " # on demande sur quel type de reads on travaille
            read mapped # on stock la réponse dans mapped
            if [[ $mapped == "mapped" ]] || [[ $mapped == "partiallyMapped" ]] || [[ $mapped == "unmapped" ]] || [[ $mapped ==  "all" ]];# on verifie que les données entrées sont correct
            then
              parameter+="$mapped" # on ajoute l'information dans param
              echo "Analysis in progress..." # on affiche que l'analyse est en cours
              python3 analyze_sam2.py $2 $parameter
              echo -e "Analysis successfully completed" # Une fois l'analyse fini on affiche un message de validation
            else
              echo "Error: you didn't write well parameters" # sinon on affiche un message d'erreur
              exit 1
            fi
          fi
else
          echo "Error: you didn't write well parameters"
          exit 1
fi



rm analyze_sam2.py # On supprime le script du dossier contenant les données.
