# MigrationKHS

##Portotype
-proto_KHS:
permet la migration des données venant de la base de données de know how sphere qui sont des fichiers en 
xml
pour cela il a besoin des ETL pour charger différentes données redondantes
Et va rechercher les données nécessaires pour ajouter les artefacts en DB 

##ETL
-ETLCollection: ETL qui permet de mettre en base de données tout les collections contenues dans les 
fichier de KHS

-ETLEtat: ETL qui permet de migrer les differents etats des fichiers de KHS

-ETLProducteur: ETL qui permet de migrer tout les producteur avec si il y a les données sur le lieu de 
production comme la ville et le pays

-ETLStock: ETL qui permet de migrer les differentes localisations des fichiers KHS