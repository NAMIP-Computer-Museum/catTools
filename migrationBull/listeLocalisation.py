# -*- coding: utf8 -*-
import openpyxl
from catTools import config
import mysql.connector
"""
fonction qui va recuperer tout les usages du fichiers
mettre constante ou fichier de config 
"""


def recup_localisation():
    wb = openpyxl.load_workbook(filename='c:\\Users\\jazzt\\desktop\\NAM-IP\\bull.xlsm')
    ws = wb['Inventaire']

    localliste = []
    for row in ws.iter_rows(min_row=config.min_row, max_col=config.max_column, max_row=config.max_row):
        local = row[18].value
        if local is None:
            continue
        elif local == 0:
            continue
        elif local in localliste:
            continue
        elif local is int:
            continue
        else:
            localliste.append(local)
            try:
             conn = mysql.connector.connect(host=config.host, user=config.user, password=config.passwd, database=config.database)
             cursor = conn.cursor()
             sql = "INSERT INTO `localisations`(`localisation`) VALUES (\'"+local+"\')"
             cursor.execute(sql)
             conn.commit()
            except mysql.connector.errors as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
            finally:
                if conn:
                    conn.close
    return localliste

recup_localisation()