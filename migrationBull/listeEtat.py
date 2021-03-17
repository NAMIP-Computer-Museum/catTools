# -*- coding: utf8 -*-

import openpyxl
from catTools import config
import mysql.connector
"""
fonction permettant de repucerer tout les etats du fichier
"""


def recup_etat():
    wb = openpyxl.load_workbook(filename='c:\\Users\\jazzt\\desktop\\NAM-IP\\bull.xlsm')
    ws = wb['Inventaire']

    etatliste = []
    for row in ws.iter_rows(min_row=config.min_row, max_col=config.max_column, max_row=config.max_row):
        etat = row[11].value
        if etat is None:
            continue
        elif etat in etatliste:
            continue
        elif etat is int:
            continue
        else:
            etatliste.append(etat)
            try:
             conn = mysql.connector.connect(host=config.host, user=config.user, password=config.passwd, database=config.database)
             cursor = conn.cursor()
             sql = "INSERT INTO `etats`(`etat`) VALUES (\'"+str(etat)+"\')"
             cursor.execute(sql)
             conn.commit()
            except mysql.connector.errors as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
            finally:
                if conn:
                    conn.close
recup_etat()