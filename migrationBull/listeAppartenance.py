# -*- coding: utf8 -*-
import openpyxl
from catTools import config
import mysql.connector
"""
fonction permettant de repucerer toutes les appartenances du fichier
atttention certaines appartenances ne sont pas ecrite de la même façon
"""


def recup_appartenance():
    wb = openpyxl.load_workbook(filename='c:\\Users\\jazzt\\desktop\\NAM-IP\\bull.xlsm')
    ws = wb['Inventaire']

    appartliste = []
    for row in ws.iter_rows(min_row=config.min_row, max_col=config.max_column, max_row=config.max_row):
        appart = row[5].value
        if appart is None:
            continue
        elif appart == 0:
            continue
        elif appart in appartliste:
            continue
        else:
            appartliste.append(appart)
            try:
             conn = mysql.connector.connect(host=config.host, user=config.user, password=config.passwd, database=config.database)
             cursor = conn.cursor()
             sql = "INSERT INTO `appartenances`(`appartenance`) VALUES (\'"+str(appart)+"\')"
             cursor.execute(sql)
             conn.commit()
            except mysql.connector.errors as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
            finally:
                if conn:
                    conn.close
recup_appartenance()