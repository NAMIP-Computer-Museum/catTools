# -*- coding: utf8 -*-
import openpyxl
from catTools import config
import mysql.connector
"""
fonction qui va recuperer tout les usages du fichiers
mettre constante ou fichier de config 
"""


def recup_usage():
    wb = openpyxl.load_workbook(filename='c:\\Users\\jazzt\\desktop\\NAM-IP\\bull.xlsm')
    ws = wb['Inventaire']

    usageliste = []
    for row in ws.iter_rows(min_row=config.min_row, max_col=config.max_column, max_row=config.max_row):
        usage = row[1].value
        if usage is None:
            continue
        elif usage in usageliste:
            continue
        else:
            usageliste.append(usage)
            try:
             conn = mysql.connector.connect(host=config.host, user=config.user, password=config.passwd, database=config.database)
             cursor = conn.cursor()
             sql = "INSERT INTO `usages`(`libelleUsage`) VALUES (\'"+usage+"\')"
             cursor.execute(sql)
             conn.commit()
            except mysql.connector.errors as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
            finally:
              if conn:
               conn.close()
    return usageliste

recup_usage()
