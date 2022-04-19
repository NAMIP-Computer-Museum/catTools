from distutils.log import error

import mysql.connector

from catTools_app import config
from catTools_app import requetes_sql as sql


def init_db(cursor):
    try:
        cursor.execute(sql.supprimer_tables())
        cursor.execute(sql.creer_table_etats())
        cursor.execute(sql.creer_table_producteurs())
        cursor.execute(sql.creer_table_donateurs())
        cursor.execute(sql.creer_table_appartenances())
        cursor.execute(sql.creer_table_localisations())
        cursor.execute(sql.creer_table_conditionnements())
        cursor.execute(sql.creer_table_usages())
        cursor.execute(sql.creer_table_familles())
        cursor.execute(sql.creer_table_artefacts())
        cursor.execute(sql.creer_table_recolements())
        cursor.execute(sql.creer_table_images())
    except mysql.connector.errors.DatabaseError as e:
        config.logging.error(
            "Erreur lors de l'initialisation de la base de données : %d, %s"
            % (e.args[0], e.args[1])
        )
