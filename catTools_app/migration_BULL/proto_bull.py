from catTools_app.migration_BULL.outils_bull.fichier_excel import (
    artefact,
    conditionnement_artefact,
)
from catTools_app import config
import openpyxl as pyxl
import mysql.connector
from catTools_app import requetes_sql as sql
from .outils_bull import db, fichier_excel

"""
Ce fichier contient le code principale de la migration des données de bull
"""


def migration(connexion, cursor):
    wb = pyxl.load_workbook(filename=config.pathbull)
    ws = wb["Inventaire"]
    nb_artefact = 0
    for ligne in ws.iter_rows(
        min_row=config.ligne_min,
        max_row=config.ligne_max,
        min_col=config.colonne_min,
        max_col=config.colonne_max,
    ):
        artefact = fichier_excel.artefact(ligne)
        remplir_tables_externe(artefact, cursor)
        ajouter_artefact(artefact, cursor)

    connexion.commit()
    
def artefact_request(artefact, id_cond, id_famille, id_appart, id_donateur, id_etat, id_producteur, id_localisation):
    sql = "INSERT INTO artefacts (`id_artefact`, `libelle`, `modele`, `numSerie`,`anProd`,`dateIn`, `longueur`, `largeur`, `hauteur`,"
    sql += "`poids`, `commentaire`, `donateur_key`, `prod_key`, `etat_key`, `localisation_key`, `cond_key`, `famille_key`, `appart_key`) VALUES("
    sql += "'" + str(artefact["id"]) + "',"
    sql += "'" + str(artefact["libelle"]) + "'," if artefact["libelle"] is not None else "NULL,"
    sql += "'" + str(artefact["modele"]) + "'," if artefact["modele"] is not None else "NULL,"
    sql += "'" + str(artefact["num_serie"]) + "'," if artefact["num_serie"] is not None else "NULL,"
    sql += ("'" + str(artefact["annee_prod"]) + "',") if artefact["annee_prod"] is not None else "NULL,"
    sql += ("'" + str(artefact["date_entree"]) + "',") if artefact["date_entree"] is not None else "NULL,"
    sql += ("'" + str(artefact["longueur"]) + "',") if artefact["longueur"] is not None else "NULL,"
    sql += ("'" + str(artefact["largeur"]) + "',") if artefact["largeur"] is not None else "NULL,"
    sql += ("'" + str(artefact["hauteur"]) + "',") if artefact["hauteur"] is not None else "NULL,"
    sql += ("'" + str(artefact["poids"]) + "',") if artefact["poids"] is not None else "NULL,"
    sql += ("'" + str(artefact["commentaire"]) + "',") if artefact["commentaire"] is not None else "NULL,"
    sql += ("'" + str(id_donateur) + "',") if id_donateur is not None else "NULL,"
    sql += ("'" + str(id_producteur) + "',") if id_producteur is not None else "NULL,"
    sql += ("'" + str(id_etat) + "',") if id_etat is not None else "NULL,"
    sql += ("'" + str(id_localisation) + "',") if id_localisation is not None else "NULL,"
    sql += ("'" + str(id_cond) + "',") if id_cond is not None else "NULL,"
    sql += ("'" + str(id_famille) + "',") if id_famille is not None else "NULL,"
    sql += ("'" + str(id_appart) + "'") if id_appart is not None else "NULL"    
    sql += ")"
    
    return sql

def ajouter_artefact(artefact, cursor):
    id_cond = db.id_conditionnement(artefact["conditionnement"], cursor)
    id_famille = db.id_famille(artefact["famille"], cursor)
    id_appart = db.id_appartenance(artefact["appartenance"], cursor)
    id_donateur = db.id_donateur(artefact["donateur"], cursor)
    id_etat = db.id_etat(artefact["etat"], cursor)
    id_producteur = db.id_producteur(artefact["producteur"], cursor)
    id_localisation = db.id_localisation(artefact["localisation"], cursor)
    
    try:
        cursor.execute(artefact_request(artefact, id_cond, id_famille, id_appart, id_donateur, id_etat, id_producteur, id_localisation))
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e, artefact['id'])
        
    
    
    

def remplir_tables_externe(artefact, cursor):
    if artefact["localisation"] is not None:
        db.ajouter_localisation(cursor, artefact["localisation"], artefact["id"])
    if artefact["appartenance"] is not None:
        db.ajouter_appartenance(cursor, artefact["appartenance"], artefact["id"])
    if artefact["usage"] is not None:
        db.ajouter_usage(cursor, artefact["usage"], artefact["id"])
    if artefact["conditionnement"] is not None:
        db.ajouter_conditionnement(cursor, artefact["conditionnement"], artefact["id"])
    if artefact["etat"] is not None:
        db.ajouter_etat(cursor, artefact["etat"], artefact["id"])
    if artefact["famille"] is not None:
        db.ajouter_famille(
            cursor, artefact["famille"], artefact["usage"], artefact["id"]
        )
    if artefact["producteur"] is not None:
        db.ajouter_producteur(cursor, artefact["producteur"], artefact["id"])
    if artefact["donateur"] is not None:
        db.ajouter_donateur(cursor, artefact["donateur"], artefact["id"])
