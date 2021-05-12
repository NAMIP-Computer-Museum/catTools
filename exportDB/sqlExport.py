sqlAr ="Select a.id_artefact,a.sourceFile,"\
       +"a.libelle,a.modele,"\
       +"a.anProd,a.dateIn,"\
       +"a.longueur,a.largeur,a.hauteur,a.poids,"\
       +"a.donateur_key,a.prod_key,a.etat_key,a.localisation_key"\
       +" from artefacts a"

sqlD = "SELECT d.donateur FROM donateurs d WHERE d.id_donateur = "

sqlP = "SELECT p.producteur FROM producteurs p WHERE p.id_producteur = "

sqlE = "SELECT e.etat FROM etats e WHERE e.id_etat = "

sqlLocal = "SELECT l.localisation FROM localisations l WHERE l.id_local = "