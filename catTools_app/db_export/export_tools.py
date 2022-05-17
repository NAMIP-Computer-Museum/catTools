import re
from distutils.command.config import config

import mysql.connector
import pandas as pd
from tqdm import tqdm

from catTools_app import config

from . import requetes_sql as sql

OUTPUTS_FOLDER = "catTools_app\db_export\outputs\\"


def export(cursor):
    export_lieux(cursor)
    export_producteurs(cursor)
    export_donateurs(cursor)
    export_localisations(cursor)
    export_machines(cursor)


def export_lieux(cursor):
    try:
        cursor.execute(sql.GET_LIEUX)

        lieux = cursor.fetchall()

        lieux = [{"Pays": x, "Ville": y} for x, y in lieux]
        df = pd.DataFrame(lieux)
        df.to_excel(OUTPUTS_FOLDER + "lieux.xlsx", index=False)
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e)


def export_producteurs(cursor):
    try:
        cursor.execute(sql.GET_PRODUCTEURS)

        producteurs = cursor.fetchall()

        producteurs = [
            {"Producteurs": x, "Pays": y, "Ville": z} for x, y, z in producteurs
        ]
        df = pd.DataFrame(producteurs)
        df.to_excel(OUTPUTS_FOLDER + "producteurs.xlsx")
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e)


def export_donateurs(cursor):
    try:
        cursor.execute(sql.GET_DONATEURS)

        donateurs = cursor.fetchall()

        donateurs = [{"Donateurs": x[0]} for x in donateurs]
        df = pd.DataFrame(donateurs)
        df.to_excel(OUTPUTS_FOLDER + "donateurs.xlsx")
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e)

def export_machines(cursor):
    try:
        cursor.execute(sql.GET_MACHINES)

        machines = cursor.fetchall()

        machines = [
            {
                "id": id,
                "libelle": libelle,
                "modele": modele,
                "numSerie": numSerie,
                "anProd": anProd,
                "quantite": quantite,
                "dateIn": dateIn,
                "longueur": longueur,
                "largeur": largeur,
                "hauteur": hauteur,
                "poids": poids,
                "description": description,
                "commentaire": commentaire,
                "localisation": localisation,
                "donateur": donateur,
                "producteur": producteur,
            } for id, libelle, modele, numSerie, anProd, quantite, dateIn, longueur, largeur, hauteur, poids, description, commentaire, localisation, donateur, producteur in machines
        ]
        df = pd.DataFrame(machines)
        df.to_excel(OUTPUTS_FOLDER + "machines.xlsx")
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e)

def export_localisations(cursor):
    try:
        cursor.execute(sql.GET_LOCALISATON)

        localisations = cursor.fetchall()
        dict_locs = []
        i = 1

        for loc in tqdm(localisations, total=len(localisations)):
            loc = str(loc[0])
            if loc.lower() not in ("musée b") and not re.match("^(HDD/)(.*)/.*$", loc):
                libelle_lieu = ""
                lieu = str(re.search("(^[A-Z]\d*)", loc)[0])
                armoire = str(re.search("(?<=-)[A-Z]", loc)[0])
                colonne = str(re.search("(?<=[A-Z])\d+", loc)[0])
                planche = str(re.search("\d+$", loc)[0])
                
                if lieu == "A":
                    libelle_lieu = "Archives"
                elif lieu == "B":
                    libelle_lieu = "Bibliothèque"
                elif lieu == "R":
                    libelle_lieu = "Réserve le long du mur"
                elif lieu.__contains__("C"):
                    libelle_lieu = "Conteneur " + re.sub("[^0-9]", "", lieu)
                else:
                    libelle_lieu = "Autres"
                
                dict_locs.append(
                    {
                        "lieu": lieu,
                        "libelle_lieu": libelle_lieu,
                        "armoire": armoire,
                        "colonne": colonne,
                        "planche": planche,
                    }
                )
            i += 1

        df = pd.DataFrame(dict_locs)
        df.to_excel(OUTPUTS_FOLDER + "localisation_musée.xlsx", index=False)
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e)
