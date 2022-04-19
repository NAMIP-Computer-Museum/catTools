import mysql.connector

from catTools_app import config
from catTools_app.init_db import init_db
from catTools_app.migration_KHS import proto_khs
from catTools_app.migration_BULL import proto_bull

if __name__ == "__main__":
    sql_loc_format_incorrect = "INSERT INTO localisations (id_local, localisation) VALUES (-1, 'Localisation pas au bon format dans le fichier source')"
    sql_loc_inconnue = (
        "INSERT INTO localisations (id_local, localisation) VALUES (1, 'Inconnue')"
    )
    try:
        connexion = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.passwd,
            database=config.database,
        )
        cursor = connexion.cursor()
        init_db(cursor)
        cursor.execute(sql_loc_format_incorrect)
        cursor.execute(sql_loc_inconnue)
        proto_khs.migration_khs(connexion, cursor)
        proto_bull.migration(connexion, cursor)

    except mysql.connector.errors.DatabaseError as e:
        config.logging.error("Erreur %d, %s" % (e.args[0], e.args[1]))
    finally:
        connexion.close()
