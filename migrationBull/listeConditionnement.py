# -*- coding: utf8 -*-
import openpyxl
from catTools import config
import mysql.connector
import re
"""
fonction qui va recuperer tout les usages du fichiers
mettre constante ou fichier de config 
"""


def recup_conditionnement():
    wb = openpyxl.load_workbook(filename='c:\\Users\\jazzt\\desktop\\NAM-IP\\bull.xlsm')
    ws = wb['Inventaire']

    condliste = []
    for row in ws.iter_rows(min_row=config.min_row, max_col=config.max_column, max_row=config.max_row):
        local = row[18].value
        cond = row[17].value
        id = 0
        if cond is None:
            continue
        elif cond in condliste:
            continue
        elif cond == 0:
            continue
        else:
            condliste.append(cond)
            try:
             conn = mysql.connector.connect(host=config.host, user=config.user, password=config.passwd, database=config.database)
             cursor = conn.cursor()
             sql1 = "SELECT id_local FROM localisations WHERE localisation = \'"+str(local)+"\'"
             cursor.execute(sql1)
             res = cursor.fetchall()
             for resultat in res:
               id = resultat[0]
               cond = re.sub('[\'"]', '', cond)
               sql2 = "INSERT INTO `conditionnements`(`conditionnement`,localisation_key) VALUES (\'"+str(cond)+"\',"+str(id)+")"
               cursor.execute(sql2)
               conn.commit()
            except mysql.connector.errors.InterfaceError as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
            finally:
              if conn:
               conn.close()
    return condliste

recup_conditionnement()