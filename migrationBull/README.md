# MigrationBull
## ETL (Extract, Transform and Load)
- listeAppartenance.py :
Il s'agit de l'ETL qui récupère les différentes appartenances des artéfacts
  de l'inventaire de Bull.
    
- listeConditionnement.py : 
Il s'agit de l'ETL qui récupère les différents conditionnements des artéfacts
  de l'inventaire de Bull.
On a besoin de générer tout d'abord l'ETL des localisations avant de le lancer.
- listeEtat.py :
Il s'agit de l'ETL qui récupère les différents états des artéfacts
  de l'inventaire de Bull.
- listeFamille.py :
Il s'agit de l'ETL qui récupère les différentes familles des artéfacts
  de l'inventaire de Bull.
On a besoin de générer tout d'abord l'ETL des usages avant de le lancer.
- listeLocalisation.py :
Il s'agit de l'ETL qui récupère les différentes localisations des artéfacts
  de l'inventaire de Bull.
- listeProducteur.py :
Il s'agit de l'ETL qui récupère les différents producteurs des artéfacts
  de l'inventaire de Bull.
- listeUsage.py :
Il s'agit de l'ETL qui récupère les différents usages des artéfacts
  de l'inventaire de Bull.
## Prototype
-proto_bull.py :
Il s'agit du prototype d'insertion d'artefacts pour l'inventaire Bull.
Il a besoin que les ETL présentés ultérieurement soient lancer et qu'ils aient accomplis leur
tâches avant de le faire tourner.
Il va rechercher les informations que les ETL ont déjà mis en DB pour remplir celles des artéfacts
