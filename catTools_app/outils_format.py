import re

from . import config

RE_LOCAL_PHYSIQUE = re.compile("^(A|B|C|R|E)(\d*)-[A-Z](\d+)\.\d*$")
RE_LOCAL_NUM = re.compile("^(HDD/)(.*)/.*$")
RE_ANNEE_PROD = re.compile("[0-9]{4}$")
RE_USAGE = re.compile("^[A-Z]{2,3}$")


def format_localisation(localisation, id_artefact):
    """Renvoie la localisation qui respect le bon format si possible, et un booleen precisant si la transformation a ete realisee"""
    avant_transformation = localisation
    if localisation is not None:
        localisation = str(localisation)
        if (
            RE_LOCAL_NUM.match(localisation)
            or RE_LOCAL_PHYSIQUE.match(localisation)
            or str(localisation).lower() == "musée b"
        ):
            return localisation, True
        else:
            localisation = localisation.lstrip()
            localisation = re.sub("(\[.*\]$)", "", localisation).rstrip()
            localisation = re.sub("\[.*", "", localisation).rstrip()
            localisation = re.sub("([A-Z]\d*)(-|,|;|--)(\d)$", "\\1.\\3", localisation)
            localisation = re.sub("^(Ate|A|B|C|R|E)(\.|,|;|-|_)", "\\1-", localisation)
            if RE_LOCAL_PHYSIQUE.match(localisation) or RE_LOCAL_NUM.match(
                localisation
            ):
                config.message_info(
                    "La localisation a été corrigée automatiquement",
                    id_artefact,
                    localisation,
                    avant_transformation,
                )
                return localisation, True

    return avant_transformation, False


def format_dimension(valeur, type_dimension, id_artefact):
    """
    Transforme la dimension passee en paramètre (valeur) pour qu'elle correspondent au format souhaite
    Si la dimension est correct renvoie la dimension au bon format
    Si la dimension n'a pas pu être corrige, renvoie la valeur de dimensions d'origine
    Renvoie egalement un booleen qui permet de savoir si la transformation à eu lieu
    Les paramètres type et id_artefact permette d'ecrire les details dans les fichiers de log
    type = "largeur", "longueur", ...
    """
    bon_format = re.compile("^\d+\.?(\d*)$")
    re1 = re.compile("^\d+((\s*)|,)\d*\s*cm$")
    re2 = re.compile("^\d+((\s*)|,)\d*\s*mm$")
    re3 = re.compile("^\d+((\s*)|,)\d*\s*kg$")
    re4 = re.compile("^\d+((\s*)|,)\d*\s*gr$")
    valeur = str(valeur)
    valeur_init = valeur
    if bon_format.match(valeur):
        return valeur, True
    elif type_dimension in ("largeur", "hauteur", "longueur") and re1.match(valeur):
        split = valeur.split("c")
        valeur = split[0]
        valeur = re.sub(",", ".", valeur).lstrip().rstrip()
        config.message_info(
            "La " + type_dimension + " a été corrigée automatiquement",
            id_artefact,
            valeur,
            valeur_init,
        )
        return valeur, True
    elif type_dimension in ("largeur", "hauteur", "longueur") and re2.match(valeur):
        split = valeur.split("m")
        valeur = float(re.sub(",", ".", split[0]))
        valeur = valeur / 10
        config.message_info(
            "Transformation de la " + type_dimension + " en cm",
            id_artefact,
            valeur,
            valeur_init,
        )
        return valeur, True
    elif type_dimension in ("poids") and re3.match(valeur):
        split = valeur.split("k")
        valeur = split[0]
        valeur = re.sub(",", ".", valeur).lstrip().rstrip()
        config.message_info(
            "Le " + type_dimension + " a été corrigé automatiquement",
            id_artefact,
            valeur,
            valeur_init,
        )
        return valeur, True
    elif type_dimension in ("poids") and re4.match(valeur):
        split = valeur.split("g")
        valeur = float(re.sub(",", ".", split[0]))
        valeur = valeur / 1000
        config.message_info(
            "Transformation du " + type_dimension + " en kg",
            id_artefact,
            valeur,
            valeur_init,
        )
        return valeur, True
    else:
        if valeur is not None and valeur not in ("None", "none"):
            determinant = "le" if type_dimension == "poids" else "la"
            config.message_avertissement(
                id_artefact,
                "Mauvais en encodage pour %s %s" % (determinant, type_dimension),
                valeur,
            )
        return valeur, False
