from catTools_app import requetes_sql as sql
import mysql.connector
from catTools_app import config


def ajouter_artefact(cursor, artefact):
    try:
        cursor.execute(sql.id_conditionnement(artefact["cond"]))
        cond_id = cursor.fetchone()[0] if len(cursor.fecthone()) != 0 else None

        cursor.execute(sql.ajouter_localisation(artefact["cond"]))
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(artefact["id_artefact"], e)


def ajouter_localisation(cursor, localisation, id_artefact):
    try:
        cursor.execute(sql.id_localisation(localisation))
        resultat = cursor.fetchone()
        if not resultat:
            cursor.execute(sql.ajouter_localisation(localisation))
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e, id_artefact)


def ajouter_appartenance(cursor, appartenance, id_artefact):
    try:
        cursor.execute(sql.id_appartenance(appartenance))
        resultat = cursor.fetchone()
        if not resultat:
            cursor.execute(sql.ajouter_appartenance(appartenance))
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e, id_artefact)


def ajouter_usage(cursor, usage, id_artefact):
    try:
        cursor.execute(sql.id_usage(usage))
        resultat = cursor.fetchone()
        if not resultat:
            cursor.execute(sql.ajouter_usage(usage))
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e, id_artefact)


def ajouter_conditionnement(cursor, conditionnement, id_artefact):
    try:
        cursor.execute(sql.id_conditionnement(conditionnement))
        resultat = cursor.fetchone()
        if not resultat:
            cursor.execute(sql.ajouter_conditionnement(conditionnement))
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e, id_artefact)


def ajouter_etat(cursor, etat, id_artefact):
    try:
        cursor.execute(sql.id_etat(etat))
        resultat = cursor.fetchone()
        if not resultat:
            cursor.execute(sql.ajouter_etat(etat))
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e, id_artefact)


def ajouter_famille(cursor, famille, usage, id_artefact):
    try:
        cursor.execute(sql.id_usage(usage))
        usage_key = cursor.fetchone()[0]
        cursor.execute(sql.id_famille(famille))
        resultat = cursor.fetchone()
        if not resultat:
            cursor.execute(sql.ajouter_famille(famille, usage_key))
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e, id_artefact)


def ajouter_producteur(cursor, producteur, id_artefact):
    try:
        cursor.execute(sql.id_producteur(producteur))
        resultat = cursor.fetchone()
        if not resultat:
            cursor.execute(sql.ajouter_producteur(producteur))
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e, id_artefact)


def ajouter_donateur(cursor, donateur, id_artefact):
    try:
        cursor.execute(sql.id_donateur(donateur))
        resultat = cursor.fetchone()
        if not resultat:
            cursor.execute(sql.ajouter_donateur(donateur))
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e, id_artefact)


def id_conditionnement(conditionnement, cursor):
    try:
        cursor.execute(sql.id_conditionnement(conditionnement))
        resultat = cursor.fetchone()
        if resultat is not None:
            return resultat[0]
        return None
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e)


def id_famille(famille, cursor):
    try:
        cursor.execute(sql.id_famille(famille))
        resultat = cursor.fetchone()
        if resultat is not None:
            return resultat[0]
        return None
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e)


def id_usage(usage, cursor):
    try:
        cursor.execute(sql.id_usage(usage))
        resultat = cursor.fetchone()
        if resultat is not None:
            return resultat[0]
        return None
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e)


def id_producteur(producteur, cursor):
    try:
        cursor.execute(sql.id_producteur(producteur))
        resultat = cursor.fetchone()
        if resultat is not None:
            return resultat[0]
        return None
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e)


def id_appartenance(appartenance, cursor):
    try:
        cursor.execute(sql.id_appartenance(appartenance))
        resultat = cursor.fetchone()
        if resultat is not None:
            return resultat[0]
        return None
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e)


def id_etat(etat, cursor):
    try:
        cursor.execute(sql.id_etat(etat))
        resultat = cursor.fetchone()
        if resultat is not None:
            return resultat[0]
        return None
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e)


def id_donateur(donateur, cursor):
    try:
        cursor.execute(sql.id_donateur(donateur))
        resultat = cursor.fetchone()
        if resultat is not None:
            return resultat[0]
        return None
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e)


def id_localisation(localisation, cursor):
    try:
        cursor.execute(sql.id_localisation(localisation))
        resultat = cursor.fetchone()
        if resultat is not None:
            return resultat[0]
        return None
    except mysql.connector.errors.DatabaseError as e:
        config.message_erreur(e)
