import re
import traceback
from xml.etree.ElementTree import ParseError

import mysql.connector

from catTools_app import config
from catTools_app import requetes_sql as sql
from catTools_app.outils_format import format_localisation


"""
Les fonctions ci-dessus se charge d'aller recuperer les informations souhaitees dans la base de donnees
"""


def nom_artefact(root):
    """ "Renvoie le nom de l'artefact ou None dans le cas où il n'y aurait pas de libelle"""
    libelle = ""
    isbd = root.find("ISBD")
    if isbd is not None:
        titi = isbd.find("Z1/TITI")
        if titi is not None:
            for child in titi:
                if child.text is not None:
                    libelle += str(child.text)
                    for little_child in child:
                        libelle += str(little_child.text) + str(little_child.tail)

        libelle = re.sub("'", "''", libelle)
        if libelle == "":
            config.message_avertissement(id_artefact(root), "Le libelle est vide")
            return None
        
        return libelle.lstrip()
    else:
        config.message_avertissement(id_artefact(root), "Le libelle est vide")
        return None


def id_artefact(root):
    return root.find("INVID").text


def date_entree_artefact(root):
    """Renvoie la date d'entree de l'artefact ou None"""
    date = "-01-01"
    if root.find("ISBN/Z0/INV") is not None:
        annee = root.find("ISBD/Z0/INV").text
        date = str(annee) + date
        return date
    else:
        config.message_avertissement(
            id_artefact(root), "La date d'entree est vide"
        )
        return None


def modele_artefact(root):
    """Renvoie le modèle de l'artefact ou None"""
    if root.find("ISBD/Z2/SXP") is not None:
        return root.find("ISBD/Z2/SXP").text
    else:
        config.message_avertissement(id_artefact(root), "Le modèle est vide")
        return None


def date_prod_artefact(root):
    """Renvoie la date de production de l'artefact ou None"""
    annee = root.find("ISBD/Z4/DT")

    if annee is None or str(annee.text) == "s.d.":
        config.message_avertissement(
            id_artefact(root), "La date de production est vide"
        )
        return None

    annee_prod_existe = False
    for annee in root.findall("ISBD/Z4/DT"):
        annee_prod_existe = "D" in annee.attrib
        if annee_prod_existe:
            break

    if annee_prod_existe:
        annee_prod = annee.attrib["D"]
        if re.match("^\d{8}$", annee_prod):
            annee_prod = annee_prod[4:]
            return annee_prod
    else:
        config.message_avertissement(
            id_artefact(root), "La date de production est vide"
        )
        return None


def images_artefact(root):
    """Renvoie une liste contenant les noms de fichiers des images liees à l'artefact"""
    images = []
    for image in root.findall("P/AI"):
        ref = image.attrib["R"]
        ref = ref.split("$")
        ref = ref[0].split("/")
        images.append(ref[1])
    return images


def identifiant_localisation(root, cursor):
    """Renvoie l'identifiant de la localisation de l'artefact ou 1 si la localisation n'est pas connue ou -1 si ne respecte pas le bon format"""
    if root.find("ISBD/Z0/LIEU") is not None:
        localisation = root.find("ISBD/Z0/LIEU").text
        localisation, bon_format = format_localisation(localisation, id_artefact(root))

        if bon_format:
            try:
                cursor.execute(sql.id_localisation(localisation))
                resultat = cursor.fetchall()
                if len(resultat) == 0:
                    return 1
                return resultat[0][0]
            except mysql.connector.errors.DatabaseError as e:
                config.message_erreur(e, id_artefact(root))
        elif localisation is not None or localisation not in ("None", "none"):
            config.message_avertissement(id_artefact(root), "La localisation ne respecte pas le bon format d'ecriture", localisation)
            return -1
    else:
        config.message_avertissement(
            id_artefact(root), "La localisation est vide"
        )
        return 1


def identifiant_producteur(root, cursor):
    """Renvoie l'identifiant du procducteur lie à l'artefact ou None"""
    producteur = root.findall("ISBD/Z4/NXP")
    if producteur is not None and len(producteur) != 0:
        if len(producteur) == 1:
            producteur = re.sub("'", "''", str(producteur[0].text))
        elif len(producteur) == 3:
            producteur = re.sub("'", "''", str(producteur[2].text))
        else:
            producteur = re.sub("'", "''", str(producteur[1].text))
        try:
            cursor.execute(sql.id_producteur(producteur))
            resultat = cursor.fetchall()
            if len(resultat) == 0:
                config.message_avertissement(
                    id_artefact(root),
                    "le producteur n'a pas ete trouve dans la base de donnees",
                )
                return None
            return resultat[0][0]
        except mysql.connector.errors.DatabaseError as e:
            config.message_avertissement(id_artefact(root), e)

    else:
        config.message_avertissement(
            id_artefact(root), "le producteur est vide"
        )
        return None


def identifiant_etat(root, cursor):
    """Renvoie l'identifiant de l'etat correspondant à l'artefact ou None"""
    if root.find("ISBD/Z7/T") is not None:
        etat = re.sub("'", "''", str(root.find("ISBD/Z7/T").text))
        cursor.execute(sql.id_etat(etat))
        resultat = cursor.fetchall()
        if len(resultat) == 0:
            config.message_avertissement(
                id_artefact(root), "l'etat n'a pas ete trouve dans la base de donnees"
            )
            return None
        return resultat[0][0]
    else:
        config.message_avertissement(id_artefact(root), "L'etat est vide")
        return None


def identifiant_collection(root, cursor):
    """Renvoie l'identifiant de la collection correspondante à l'artefact ou None"""
    if root.find("ISBD/Z8/T") is not None:
        collection = str(root.find("ISBD/Z8/NXP").text)
        cursor.execute(sql.id_donateur(collection))
        resultat = cursor.fetchall()
        if len(resultat) == 0:
            config.message_avertissement(
                id_artefact(root),
                "la collection n'a pas ete trouvee dans la base de donnees",
            )
            return None
        return resultat[0][0]
    else:
        config.message_avertissement(
            id_artefact(root), "la collection est vide"
        )
        return None


def description_artefact(root):
    """Renvoie la description de l'artefact"""
    description = ""
    ref = root.findall("P/")
    for child in ref:
        if child.tag in ("NXP", "T", "DT", "B", "AV", "DSN"):
            if child.text is not None:
                description += " " + str(child.text).lstrip().rstrip()
            for little_child in child:
                if little_child.text is not None:
                    description += " " + str(little_child.text).lstrip().rstrip()

    description = re.sub("●", "-", description)
    description = re.sub("'", "''", description)

    return description.lstrip().rstrip()


"""
Les fonctions ci-dessous permetre d'ajouter des informations dans la base de donnees à partir d'information recuperer dans l4arbre XML dont la racine a ete passee en paramètres
"""


def ajouter_collection(root, cursor):
    """Permet d'ajouter une collection à la base de donnees à partir d'un fichier si elle n'y est pas encore presente"""
    collection = root.find("ISBD/Z8/NXP")

    if collection is not None and collection.text is not None:
        try:
            # Verifier si la collection est dejà presente dans la base de donnees
            cursor.execute(sql.id_donateur(str(collection.text)))
            if len(cursor.fetchall()) == 0:
                # Inserer la nouvelle collection dans la base de donnees
                cursor.execute(sql.ajouter_donateur(str(collection.text)))
        except mysql.connector.errors.DatabaseError as e:
            config.message_erreur(e, id_artefact(root))


def ajouter_producteur(root, cursor):
    """Permet d'ajouter un producteur à la base de donnees à partir d'un fichier s'il n'y est pas encore present"""
    try:
        producteur = root.findall("ISBD/Z4/NXP")
        if len(producteur) != 0:
            if len(producteur) == 1:
                producteur = str(producteur[0].text)

                producteur = re.sub("'", "''", str(producteur))

                if not producteur_existe(root, producteur, cursor):
                    try:
                        cursor.execute(sql.ajouter_producteur(producteur))
                    except mysql.connector.errors.DatabaseError as e:
                        config.message_erreur(e, id_artefact(root))
            elif len(producteur) == 3:
                pays = str(producteur[0].text)
                ville = str(producteur[1].text)
                producteur = str(producteur[2].text)

                producteur = re.sub("'", "''", producteur)

                if not producteur_existe(root, producteur, cursor):
                    pays = re.sub("'", "''", pays)
                    ville = re.sub("'", "''", ville)
                    try:
                        cursor.execute(
                            sql.ajouter_producteur(producteur, pays=pays, ville=ville)
                        )
                    except mysql.connector.errors.DatabaseError as e:
                        config.message_erreur(e, id_artefact(root))
            else:
                pays = str(producteur[0].text)
                producteur = str(producteur[1].text)

                producteur = re.sub("'", "''", producteur)

                if producteur != "s.n.":
                    if not producteur_existe(root, producteur, cursor):
                        pays = re.sub("'", "''", pays)
                        try:
                            cursor.execute(
                                sql.ajouter_producteur(producteur, pays=pays)
                            )
                        except mysql.connector.errors.DatabaseError as e:
                            config.message_erreur(e, id_artefact(root))
    except ParseError as e:
        config.message_erreur(e, id_artefact(root))
        traceback.print_exc()


def ajouter_etat(root, cursor):
    """Permet d'ajouter un etat à la base de donnees à partir d'un fichier s'il n'y est pas encore present"""
    etat = root.find("ISBD/Z7/T")
    if etat is not None:
        etat = str(etat.text)
        etat = re.sub("'", "''", etat)
        # Verifier si l'etat est dejà present dans la base de donnees
        try:
            cursor.execute(sql.id_etat(etat))

            if len(cursor.fetchall()) == 0:
                cursor.execute(sql.ajouter_etat(etat))

        except mysql.connector.errors.DatabaseError as e:
            config.message_erreur(e, id_artefact(root))


def ajouter_lieu_stockage(root, cursor):
    """Permet d'ajouter le lieu de stockage à la base de donnees s'il n'y est pas encore present et s'il respecte le bon format"""
    loc = root.find("ISBD/Z0/LIEU")

    if loc is not None:
        loc = str(loc.text)
        loc, bon_format = format_localisation(loc, id_artefact(root))
        if bon_format:
            try:
                # Verifier que le lieu de stockage est dejà present en DB
                cursor.execute(sql.id_localisation(loc))
                if len(cursor.fetchall()) == 0:
                    cursor.execute(sql.ajouter_localisation(loc))
            except mysql.connector.errors.DatabaseError as e:
                config.message_erreur(e, id_artefact(root))


"""
Les fonctiones ci-dessous sont des outils supplementaires
"""


def producteur_existe(root, producteur, cursor):
    """Verifie si le producteur est dejà present dans la base de donnees"""
    try:
        cursor.execute(sql.id_producteur(producteur))
        return len(cursor.fetchall()) != 0
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e, id_artefact(root))


def dimensions_artefact(root, artefact):
    """Ajoute les dimensions à l'artefact passe en paramètre tout en les formattant dans le bon format"""
    try:
        dim = ""
        for child in root.findall("ISBD/Z5/"):
            if child.text is not None:
                dim += str(child.text)
            for little_child in child:
                if little_child.text is not None:
                    dim += little_child.text
                if little_child.tail is not None:
                    dim += little_child.tail
        dimensions = re.findall("((L|l|H) \d*,?(\d*)?)", dim)
        poids = re.findall("(\d*,?(\d*)? kg)", dim)
        if len(dimensions) == 3:
            artefact.longueur = re.sub(
                "L", "", (re.sub(",", ".", dimensions[0][0]))
            ).lstrip()
            artefact.largeur = re.sub(
                "l", "", (re.sub(",", ".", dimensions[1][0]))
            ).lstrip()
            artefact.hauteur = re.sub(
                "H", "", (re.sub(",", ".", dimensions[2][0]))
            ).lstrip()
        elif len(dimensions) > 3:
            config.message_avertissement(
                id_artefact(root), "Plusieurs artefact dans le fichier"
            )
        else:
            config.message_avertissement(
                id_artefact(root), "Pas de dimensions pour l'artefact"
            )

        if len(poids) == 1:
            artefact.poids = re.sub("kg", "", (re.sub(",", ".", poids[0][0]))).rstrip()
        elif len(poids) > 1:
            config.message_avertissement(
                id_artefact(root), "Plusieurs artefact dans le fichier"
            )
        else:
            config.message_avertissement(
                id_artefact(root), "Pas de poids pour l'artefact"
            )
    except BaseException as e:
        config.logging.error(
            "dimensions_artefact (" + id_artefact(root) + ") " + str(e)
        )
