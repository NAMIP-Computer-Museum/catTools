GET_PRODUCTEURS = ("SELECT distinct producteur, pays, ville FROM producteurs" +
    "LEFT JOIN artefacts ON producteurs.id_producteur = artefacts.prod_key" +
    "LEFT JOIN categorie ON artefacts.cat_key = categorie.id_categorie" +
    "LEFT JOIN familles ON familles.id_famille = artefacts.famille_key " +
    "LEFT JOIN usages ON usages.id_usage = familles.usage_key " +
    "WHERE usages.libelleUsage = 'MA' OR categorie.libelle = 'Machines")
GET_LIEUX = (
    "SELECT pays, ville FROM producteurs WHERE NOT (pays IS NULL AND ville IS NULL)"
)
GET_DONATEURS = "SELECT donateur FROM donateurs"
GET_LOCALISATON = (
    "SELECT localisation FROM localisations WHERE id_local != -1 AND id_local != 1"
)
GET_MACHINES = ("SELECT artefacts.id_artefact, artefacts.libelle, artefacts.modele, artefacts.numSerie, artefacts.anProd, artefacts.quantite," +
    "artefacts.dateIn, artefacts.longueur, artefacts.largeur, artefacts.hauteur, artefacts.poids, artefacts.description, artefacts.commentaire, localisations.localisation," +
    "donateurs.donateur, producteurs.producteur FROM artefacts " +
    "LEFT JOIN categorie ON categorie.id_categorie = artefacts.cat_key LEFT JOIN familles ON familles.id_famille = artefacts.famille_key " +
    "LEFT JOIN usages ON usages.id_usage = familles.usage_key LEFT JOIN donateurs ON donateurs.id_donateur = artefacts.donateur_key " +
    "LEFT JOIN localisations ON localisations.id_local = artefacts.localisation_key " +
    "LEFT JOIN producteurs ON producteurs.id_producteur = artefacts.prod_key WHERE usages.libelleUsage = 'MA' OR categorie.libelle = 'Machines'")
