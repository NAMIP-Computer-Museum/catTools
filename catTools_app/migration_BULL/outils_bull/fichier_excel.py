import re
from datetime import datetime

from catTools_app import config
from catTools_app.outils_format import (
    RE_ANNEE_PROD,
    RE_USAGE,
    format_dimension,
    format_localisation,
)

from .. import constantes as const


def artefact(ligne):
    return {
        "id": id_artefact(ligne),
        "usage": usage_artefact(ligne),
        "famille": famille_artefact(ligne),
        "libelle": libelle_artefact(ligne),
        "modele": modele_artefact(ligne),
        "appartenance": appartenance_artefact(ligne),
        "num_serie": num_serie_artefact(ligne),
        "annee_prod": annee_prod_artefact(ligne),
        "quantite": quantite_artefact(ligne),
        "producteur": producteur_artefact(ligne),
        "etat": etat_artefact(ligne),
        "conditionnement": conditionnement_artefact(ligne),
        "localisation": localisation_artefact(ligne),
        "longueur": longueur_artefact(ligne),
        "largeur": largeur_artefact(ligne),
        "hauteur": hauteur_artefact(ligne),
        "poids": poids_artefact(ligne),
        "donateur": donateur_artefact(ligne),
        "liens": liens_artefact(ligne),
        "image": image_artefact(ligne),
        "date_entree": date_entree_artefact(ligne),
        "recolement": recolement_artefact(ligne),
        "commentaire": commentaire_artefact(ligne),
    }


"""
Les fonctions ci-dessous permettent de recuperer les details d'un artefact avec un ligne d'une worksheet passee en paramètre
Elles effectuent egalement les verifications concernant le format de ces different details
"""


def id_artefact(ligne):
    """Recupère l'identifiant de l'artefact lie à la ligne de la worksheet passee en paramètre et le renvoie sous le format BULL-identifiant"""
    id = ligne[const.ID].value
    return "BULL-" + str(id)


def usage_artefact(ligne):
    """
    Recupère l'usage de l'artefact lie à la ligne de la worksheet passee en paramètre
    Verifie que l'usage est au bon format (2 ou 3 lettre en majuscule) / Si pas mention dans le fichier de log
    Renvoie None si l'usage n'est pas encode et le signal dans le fichier de log
    """
    usage = ligne[const.USAGE].value
    if usage is None:
        config.message_avertissement(id_artefact(ligne), "L'usage est vide")
    else:
        usage = usage.upper()
        if RE_USAGE.match(usage):
            return usage
        else:
            config.message_avertissement(
                id_artefact(ligne), "L'usage n'a pas le bon format", usage
            )
            return None


def famille_artefact(ligne):
    """
    Recupère la famille de l'artefact lie à la ligne de la worksheet passee en paramètre
    Verifie que la famille est presente (si pas renvoie None et mention dans log)
    Formatte la famille pour qu'elle commence toujours par une majuscule
    """
    famille = ligne[const.FAMILLE].value
    if famille is None or famille == 0:
        config.message_avertissement(id_artefact(ligne), "La famille est vide")
    else:
        return famille.capitalize()


def libelle_artefact(ligne):
    """
    Recupère le libelle de l'artefact lie à la ligne de la worksheet passee en paramètre
    Verifie que le libelle est present (si pas renvoie None et mention dans log)
    """
    libelle = ligne[const.LIBELLE].value

    if libelle is None or libelle == 0:
        config.message_avertissement(id_artefact(ligne), "Le libelle est vide")
        return None
    else:
        libelle = re.sub("'", "''", libelle)
        return libelle


def modele_artefact(ligne):
    """
    Recupère le modèle de l'artefact lie à la ligne de la worksheet passee en paramètre
    Verifie que le modèle est present (si pas renvoie None et mention dans log)
    """
    modele = ligne[const.MODELE].value
    if modele is None or modele == 0 or not modele:
        config.message_avertissement(id_artefact(ligne), "Le modèle est vide")
        return None
    else:
        modele = str(modele)
        modele = modele.rstrip().lstrip()
        if not modele:
            config.message_avertissement(id_artefact(ligne), "Le modèle est vide")
            return None
        modele = re.sub("'", "''", str(modele))
        return modele


def appartenance_artefact(ligne):
    """
    Recupère l'appartenance de l'artefact lie à la ligne de la worksheet passee en paramètre
    Verifie que l'appartenance est present (si pas renvoie None et mention dans log)
    """
    appart = ligne[const.APPARTENANCE].value
    if appart is None or appart == 0:
        config.message_avertissement(id_artefact(ligne), "L'appartenance est vide")
        return None
    else:
        appart = str(appart).lstrip().rstrip()
        if appart == "" or appart == "?":
            config.message_avertissement(id_artefact(ligne), "L'appartenance est vide")
            return None
        return appart


def num_serie_artefact(ligne):
    """
    Recupère le numero de serie de l'artefact lie à la ligne de la worksheet passee en paramètre
    Verifie que le numero de serie est present (si pas renvoie None et mention dans log)
    """
    num_serie = ligne[const.NUMERO_SERIE].value
    if num_serie is None or num_serie == 0:
        config.message_avertissement(id_artefact(ligne), "Le numero de serie est vide")
        return None
    else:
        return num_serie


def annee_prod_artefact(ligne):
    """
    Recupère l'annee de production de l'artefact lie à la ligne de la worksheet passee en paramètre
    Verifie que l'annee de production est present (si pas renvoie None et mention dans log)
    Verifie egalement qu'elle est correct (Mention dans les logs)
    """
    annee_prod = str(ligne[const.ANNEE_PRODUCTION].value)
    if annee_prod is None or annee_prod == 0 or annee_prod in ("None", "none"):
        config.message_avertissement(
            id_artefact(ligne), "L'annee de production est vide"
        )
        return None
    elif not RE_ANNEE_PROD.match(annee_prod):
        config.message_avertissement(
            id_artefact(ligne),
            "L'annee de production n'a pas le bon format",
            annee_prod,
        )
        return None
    elif int(annee_prod) < 1500:
        config.message_avertissement(
            id_artefact(ligne), "L'annee de production est inferieur à 1500", annee_prod
        )
        return None
    elif int(annee_prod) > int(datetime.today().year):
        config.message_avertissement(
            id_artefact(ligne),
            "L'annee de production est superieur à aujourd'hui",
            annee_prod,
        )
        return None
    else:
        return annee_prod


def producteur_artefact(ligne):
    """
    Recupère le producteur de l'artefact lie à la ligne de la worksheet passee en paramètre
    Verifie que le producteur est present (si pas renvoie None et mention dans log)
    Format le producteur pour qu'il commence par une majuscule
    """
    producteur = ligne[const.PRODUCTEUR].value
    if producteur is None or producteur == 0:
        config.message_avertissement(id_artefact(ligne), "Le producteur est vide")
        return None
    else:
        producteur = re.sub("'", "''", str(producteur))
        return str(producteur).capitalize()


def quantite_artefact(ligne):
    """
    Recupère la quantite de l'artefact lie à la ligne de la worksheet passee en paramètre
    Verifie que la quantite est present (si pas renvoie None et mention dans log)
    """
    qte = ligne[const.QUANTITE].value
    if qte is None:
        config.message_avertissement(id_artefact(ligne), "La quantite est vide")
        return None
    else:
        return qte


def etat_artefact(ligne):
    """
    Recupère l'etat de l'artefact lie à la ligne de la worksheet passee en paramètre
    Verifie que l'etat est present (si pas renvoie None et mention dans log)
    Renvoie l'etat en majuscule
    """
    etat = ligne[const.ETAT].value
    if etat is None or etat == 0:
        config.message_avertissement(id_artefact(ligne), "L'etat est vide")
        return None
    else:
        return str(etat).upper()


def conditionnement_artefact(ligne):
    """
    Recupère le conditionnement de l'artefact lie à la ligne de la worksheet passee en paramètre
    Verifie que le conditionnement est present
    Renvoie le conditionnement qui commence toujours par une majuscule
    """
    cond = ligne[const.CONDITIONNEMENT].value

    if cond is None or cond == 0:
        return None
    return re.sub("'", "''", str(cond).capitalize())


def localisation_artefact(ligne):
    """
    Recupère la localisation de l'artefact lie à la ligne de la worksheet passee en paramètre
    Verifie que la localisation est present et qu'elle est au bon format (mention dans le log), Renvoie NONE dans le cas contraire
    """
    local = ligne[const.LOCALISATION].value
    if local is None or local == 0:
        config.message_avertissement(id_artefact(ligne), "La localisation est vide")
        return None
    else:
        local, bon_format = format_localisation(local, id_artefact(ligne))
        if bon_format:
            return local
        else:
            config.message_avertissement(
                id_artefact(ligne), "La localisation n'a pas le bon format", str(local)
            )
            return None


def longueur_artefact(ligne):
    """
    Recupère la longueur de l'artefact lie à la ligne de la worksheet passee en paramètre
    Verifie que la longueur est present et qu'elle est au bon format (mention dans le log), Renvoie NONE dans le cas contraire
    """
    longueur = str(ligne[const.LONGUEUR].value).lower()
    if longueur is None:
        config.message_avertissement(id_artefact(ligne), "La longueur est vide")
        return None
    else:
        longueur, bon_format = format_dimension(
            longueur, "longueur", id_artefact(ligne)
        )
        if bon_format:
            return longueur
        else:
            return None


def largeur_artefact(ligne):
    """
    Recupère la largeur de l'artefact lie à la ligne de la worksheet passee en paramètre
    Verifie que la largeur est present et qu'elle est au bon format (mention dans le log), Renvoie NONE dans le cas contraire
    """
    largeur = str(ligne[const.LARGEUR].value).lower()
    if largeur is None:
        config.message_avertissement(id_artefact(ligne), "La largeur est vide")
        return None
    else:
        largeur, bon_format = format_dimension(largeur, "largeur", id_artefact(ligne))
        if bon_format:
            return largeur
        else:
            return None


def hauteur_artefact(ligne):
    """
    Recupère la hauteur de l'artefact lie à la ligne de la worksheet passee en paramètre
    Verifie que la hauteur est present et qu'elle est au bon format (mention dans le log), Renvoie NONE dans le cas contraire
    """
    hauteur = str(ligne[const.HAUTEUR].value).lower()
    if hauteur is None:
        config.message_avertissement(id_artefact(ligne), "La hauteur est vide")
        return None
    else:
        hauteur, bon_format = format_dimension(hauteur, "hauteur", id_artefact(ligne))
        if bon_format:
            return hauteur
        else:
            return None


def poids_artefact(ligne):
    """
    Recupère le poids de l'artefact lie à la ligne de la worksheet passee en paramètre
    Verifie que le poids est present et qu'elle est au bon format (mention dans le log), Renvoie NONE dans le cas contraire
    """
    poids = str(ligne[const.POIDS].value).lower()
    if poids is None:
        config.message_avertissement(id_artefact(ligne), "Le poids est vide")
        return None
    else:
        poids, bon_format = format_dimension(poids, "poids", id_artefact(ligne))
        if bon_format:
            return poids
        else:
            return None


def donateur_artefact(ligne):
    """Recupère le donateur de l'artefact lie à la ligne de la worksheet passee en paramètre"""
    donateur = ligne[const.DONATEUR].value
    if donateur is None or donateur == 0:
        config.message_avertissement(id_artefact(ligne), "Pas de donateur")
        return None
    return donateur


def liens_artefact(ligne):
    """Recupère les liens de l'artefact lie à la ligne de la worksheet passee en paramètre"""
    return ligne[const.LIENS[0]], ligne[const.LIENS[1]]


def commentaire_artefact(ligne):
    """Recupère le commentaire de l'artefact lie à la ligne de la worksheet passee en paramètre"""
    comment = ligne[const.COMMENTAIRE].value
    if comment is None or comment == 0:
        comment = None
        config.message_avertissement(id_artefact(ligne), "Pas de commentaire")
    else:
        comment = re.sub("'", "''", str(comment))

    return comment


def image_artefact(ligne):
    """Recupère l'image de l'artefact lie à la ligne de la worksheet passee en paramètre"""
    image = ligne[const.IMAGE].value
    if image is None or image == 0:
        image = None
    else:
        image = re.sub("'", "''", image)

    return image


def date_entree_artefact(ligne):
    """
    Recupère la date d'entree de l'artefact lie à la ligne de la worksheet passee en paramètre
    Renvoie None si la date est inexistant ou incorrect (Log)
    Renvoie la date au format dd-mm-aaaa
    """
    date_entree = ligne[const.DATE_ENTREE].value
    if date_entree is None or date_entree == "":
        config.message_avertissement(id_artefact(ligne), "La date d'entree est vide")
        return None
    elif str(date_entree) > str(datetime.today()):
        config.message_avertissement(
            id_artefact(ligne),
            "La date d'entree est posterieur à aujourd'hui",
            date_entree,
        )
        return None
    elif str(date_entree) < str(datetime(1990, 1, 1)):
        config.message_avertissement(
            id_artefact(ligne),
            "La date d'entree est anterieur au 01/01/1990",
            date_entree,
        )
        return None
    else:
        if type(date_entree) is str:
            date_entree = re.sub("/", "-", date_entree)
            try:
                split = date_entree.split("-")
                datetime(year=int(split[0]), month=int(split[1]), day=int(split[2]))
                return date_entree
            except ValueError as e:
                config.message_avertissement(
                    id_artefact(ligne), "La date d'entree est incorrect", date_entree
                )
        else:
            return date_entree.strftime("%Y-%m-%d")


def recolement_artefact(ligne):
    """
    Recupère la date de recolement de l'artefact lie à la ligne de la worksheet passee en paramètre
    Renvoie None si la date est inexistant (Log)
    Renvoie la date au format dd-mm-aaaa
    """
    recolement = ligne[const.RECOLEMENT].value
    if recolement is None or recolement == "" or recolement == 0:
        config.message_avertissement(
            id_artefact(ligne), "La date de recolement est vide"
        )
        return None
    else:
        return recolement.strftime("%d-%m-%Y")
