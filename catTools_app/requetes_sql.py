import re


def ajouter_artefact_khs(artefact):
    p1 = "INSERT INTO artefacts (`id_artefact`,`sourceFile`, `libelle`, `modele`,`anProd`,`dateIn`, `longueur`,"
    p2 = "`largeur`, `hauteur`, `poids`,`description`, `donateur_key`, `prod_key`, `etat_key`, `localisation_key`)"

    if artefact.modele is not None:
        p3 = (
            " VALUES('"
            + str(artefact.id)
            + "','"
            + str(artefact.fichier_source)
            + "','"
            + str(artefact.nom)
            + "','"
            + str(artefact.modele)
            + "',"
            + str(artefact.date_production)
            + ","
        )
    else:
        p3 = (
            " VALUES('"
            + str(artefact.id)
            + "','"
            + str(artefact.fichier_source)
            + "','"
            + str(artefact.nom)
            + "',NULL,"
            + str(artefact.date_production)
            + ","
        )

    if artefact.date_entree is not None:
        p4 = (
            "'"
            + str(artefact.date_entree)
            + "',"
            + str(artefact.longueur)
            + ","
            + str(artefact.largeur)
            + ","
            + str(artefact.hauteur)
            + ","
            + str(artefact.poids)
        )
    else:
        p4 = (
            str(artefact.date_entree)
            + ","
            + str(artefact.longueur)
            + ","
            + str(artefact.largeur)
            + ","
            + str(artefact.hauteur)
            + ","
            + str(artefact.poids)
        )

    p5 = (
        ",'"
        + str(artefact.description)
        + "',"
        + str(artefact.collection)
        + ","
        + str(artefact.producteur)
        + ","
        + str(artefact.etat)
        + ","
        + str(artefact.stock)
        + ")"
    )
    sql = p1 + p2 + p3 + p4 + p5
    sql = re.sub("None", "NULL", sql)

    return sql


def ajouter_etat(etat):
    return "INSERT INTO etats (etat) VALUES ('" + str(etat) + "')"


def ajouter_image(image, id_artefact):
    return "INSERT INTO images(image, artefact_key) VALUES ('%s', '%s')" % (
        str(image),
        str(id_artefact),
    )


def ajouter_producteur(producteur, ville=None, pays=None):
    return (
        "INSERT INTO producteurs (producteur, ville, pays) VALUES ('%s', '%s', '%s')"
        % (str(producteur), str(ville), str(pays))
    )


def ajouter_localisation(localisation):
    return (
        "INSERT INTO localisations (localisation) VALUES ('" + str(localisation) + "')"
    )


def id_localisation(localisation):
    return (
        "SELECT id_local FROM localisations WHERE localisation = '"
        + str(localisation)
        + "'"
    )


def id_producteur(producteur):
    return (
        "SELECT id_producteur FROM producteurs WHERE producteur = '"
        + str(producteur)
        + "'"
    )


def id_appartenance(appartenance):
    return (
        "SELECT id_appart FROM appartenances WHERE appartenance ='"
        + str(appartenance)
        + "'"
    )


def id_conditionnement(conditionnement):
    return (
        "SELECT id_cond FROM conditionnements WHERE conditionnement = '"
        + str(conditionnement)
        + "'"
    )


def ajouter_conditionnement(conditionnement):
    return "INSERT INTO conditionnements(conditionnement) VALUES ('%s')" % (
        str(conditionnement)
    )


def ajouter_appartenance(appartenance):
    return (
        "INSERT INTO appartenances (appartenance) VALUES('"
        + str(appartenance).capitalize()
        + "')"
    )


def ajouter_recolement(recolement, id_artefact):
    return "INSERT INTO recolements (recolement) VALUES ('%s', '%s')" % (
        str(recolement),
        str(id_artefact),
    )


def id_famille(famille):
    return "SELECT id_famille FROM familles WHERE famille ='" + str(famille) + "'"


def ajouter_famille(famille, usage_key):
    return "INSERT INTO familles (famille, usage_key) VALUES('%s', '%s')" % (
        famille,
        usage_key,
    )


def ajouter_usage(usage):
    return "INSERT INTO usages (libelleUsage) VALUES ('" + str(usage) + "')"


def id_etat(etat):
    return "SELECT id_etat FROM etats WHERE etat = '" + str(etat) + "'"


def id_donateur(donateur):
    return "SELECT id_donateur FROM donateurs WHERE donateur = '" + str(donateur) + "'"


def ajouter_donateur(donateur):
    return "INSERT INTO donateurs (donateur) VALUES ('" + str(donateur) + "')"


def id_usage(usage):
    return "SELECT id_usage FROM usages WHERE libelleUsage ='" + str(usage) + "'"


def supprimer_tables():
    return "DROP TABLE IF EXISTS etats, producteurs, donateurs, appartenances, localisations, conditionnements, usages, familles, artefacts, recolements, images, liens"


def creer_table_etats():
    return "CREATE TABLE IF NOT EXISTS etats(id_etat int(10) NOT NULL AUTO_INCREMENT, etat varchar(255) NOT NULL, PRIMARY KEY(id_etat))"


def creer_table_producteurs():
    return (
        "CREATE TABLE IF NOT EXISTS producteurs(id_producteur int(10) NOT NULL AUTO_INCREMENT, producteur varchar(255) NOT NULL,"
        + "pays varchar(255) NULL, ville varchar(255) NULL, PRIMARY KEY(id_producteur))"
    )


def creer_table_donateurs():
    return "CREATE TABLE IF NOT EXISTS donateurs(id_donateur int(10) NOT NULL AUTO_INCREMENT, donateur varchar(255) NOT NULL, PRIMARY KEY(id_donateur))"


def creer_table_appartenances():
    return "CREATE TABLE IF NOT EXISTS appartenances(id_appart int(10) NOT NULL AUTO_INCREMENT, appartenance varchar(255) NOT NULL, PRIMARY KEY(id_appart))"


def creer_table_localisations():
    return "CREATE TABLE IF NOT EXISTS localisations(id_local int(10) NOT NULL AUTO_INCREMENT, localisation varchar(255) NOT NULL, PRIMARY KEY(id_local))"


def creer_table_conditionnements():
    return "CREATE TABLE IF NOT EXISTS conditionnements(id_cond int(10) NOT NULL AUTO_INCREMENT, conditionnement varchar(255) NOT NULL, PRIMARY KEY(id_cond))"


def creer_table_usages():
    return "CREATE TABLE IF NOT EXISTS usages(id_usage int(10) NOT NULL AUTO_INCREMENT, libelleUsage varchar(255) NOT NULL, PRIMARY KEY(id_usage));"


def creer_table_familles():
    return (
        "CREATE TABLE IF NOT EXISTS familles(id_famille int(10) NOT NULL AUTO_INCREMENT, famille varchar(255) NOT NULL, usage_key int NOT NULL,"
        + "PRIMARY KEY(id_famille), FOREIGN KEY (usage_key) REFERENCES usages(id_usage))"
    )


def creer_table_artefacts():
    return (
        "CREATE TABLE IF NOT EXISTS artefacts (id_artefact varchar(255) NOT NULL, sourceFile varchar(255) DEFAULT NULL,"
        + "libelle varchar(600) DEFAULT NULL, modele varchar(255) DEFAULT NULL, numSerie varchar(255) DEFAULT NULL, anProd int(4) DEFAULT NULL,"
        + "quantite int(5) DEFAULT NULL, dateIn date DEFAULT NULL, longueur double(10,3) DEFAULT NULL, largeur double(10,3) DEFAULT NULL,"
        + "hauteur double(10,3) DEFAULT NULL, poids double(10,3) DEFAULT NULL, description longtext DEFAULT NULL, commentaire varchar(255) DEFAULT NULL,"
        + "donateur_key int NULL, cond_key int NULL, prod_key int NULL, etat_key int NULL, localisation_key int NULL, appart_key int NULL,"
        + "famille_key int NULL, PRIMARY KEY(id_artefact), FOREIGN KEY (donateur_key)  REFERENCES donateurs(id_donateur),"
        + "FOREIGN KEY (cond_key) REFERENCES conditionnements (id_cond), FOREIGN KEY (prod_key) REFERENCES producteurs(id_producteur), "
        + "FOREIGN KEY (etat_key) REFERENCES etats(id_etat), FOREIGN KEY (localisation_key)  REFERENCES localisations(id_local),"
        + "FOREIGN KEY (appart_key) REFERENCES appartenances(id_appart), FOREIGN KEY (famille_key) REFERENCES familles(id_famille))"
    )


def creer_table_recolements():
    return (
        "CREATE TABLE IF NOT EXISTS recolements(id_recol int(10) NOT NULL AUTO_INCREMENT, recolement date NOT NULL,"
        + "artefact_key varchar(255) NOT NULL, PRIMARY KEY(id_recol), FOREIGN KEY (artefact_key) REFERENCES artefacts(id_artefact))"
    )


def creer_table_images():
    return (
        "CREATE TABLE IF NOT EXISTS images(id_image int(10) NOT NULL AUTO_INCREMENT, image varchar(255) NOT NULL,"
        + "artefact_key varchar(255) NOT NULL, PRIMARY KEY(id_image), FOREIGN KEY (artefact_key) REFERENCES artefacts(id_artefact))"
    )
