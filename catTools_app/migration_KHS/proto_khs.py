import re
import xml.etree.ElementTree as ET
from os import listdir

import mysql.connector

from catTools_app import config, requetes_sql
from catTools_app.migration_KHS.Artefact import Artefact

from . import outils_khs

from tqdm import tqdm


"""
Ce fichier permet de migrer les données de KHS vers la base de données en utilisant les fonctions définies dans le fichier outils_khs.py 
"""


def migration_khs(connexion, cursor):
    fichier = ""
    try:
        for fichier in tqdm(listdir(config.pathkhs), total=len(listdir(config.pathkhs)), desc="Migration KHS"):
            if re.match("V[0-9]*.xml", fichier):
                tree = ET.parse(config.pathkhs + "\\" + str(fichier))
                root = tree.getroot()
                outils_khs.ajouter_lieu_stockage(root, cursor)
                outils_khs.ajouter_producteur(root, cursor)
                outils_khs.ajouter_etat(root, cursor)
                outils_khs.ajouter_collection(root, cursor)
                ajouter_artefact(cursor, root, fichier)

        connexion.commit()

    except mysql.connector.errors.DatabaseError as e:
        config.logging.error(
            "Fichier " + str(fichier) + " ; Erreur %d, %s" % (e.args[0], e.args[1])
        )


def ajouter_artefact(cursor, root, fichier):
    id = outils_khs.id_artefact(root)
    artefact = Artefact(id, fichier)
    artefact.nom = outils_khs.nom_artefact(root)
    artefact.date_entree = outils_khs.date_entree_artefact(root)
    artefact.modele = outils_khs.modele_artefact(root)
    artefact.date_production = outils_khs.date_prod_artefact(root)
    outils_khs.dimensions_artefact(root, artefact)
    artefact.images = outils_khs.images_artefact(root)
    artefact.description = outils_khs.description_artefact(root)
    artefact.stock = outils_khs.identifiant_localisation(root, cursor)
    artefact.producteur = outils_khs.identifiant_producteur(root, cursor)
    artefact.etat = outils_khs.identifiant_etat(root, cursor)
    artefact.collection = outils_khs.identifiant_collection(root, cursor)

    try:
        cursor.execute(requetes_sql.ajouter_artefact_khs(artefact))
        for image in artefact.images:
            cursor.execute(requetes_sql.ajouter_image(image, artefact.id))
    except mysql.connector.errors.DatabaseError as e:
        config.logging.error(
            "Fichier " + str(fichier) + " ; Erreur %d, %s" % (e.args[0], e.args[1])
        )
