# -*- coding: utf8 -*-
import openpyxl
from catTools import config
import mysql.connector
"""
fonction qui va recuperer toutes les familles  du fichiers
atttention certaines appartenances ne sont pas ecrite de la même façon
"""


def recup_famille():
    wb = openpyxl.load_workbook(filename='c:\\Users\\jazzt\\desktop\\NAM-IP\\bull.xlsm')
    ws = wb['Inventaire']

    familleliste = []
    for row in ws.iter_rows(min_row=config.min_row, max_col=config.max_column, max_row=config.max_row):
        usage = row[1].value
        famille = row[2].value
        if famille is None:
            continue
        elif famille in familleliste:
            continue
        else:
            familleliste.append(famille)
            try:
             conn = mysql.connector.connect(host=config.host, user=config.user, password=config.passwd, database=config.database)
             cursor = conn.cursor()
             sql1 = "SELECT id_usage FROM usages WHERE libelleUsage = \'"+usage+"\'"
             cursor.execute(sql1)
             res = cursor.fetchall()
             for resultat in res:
                 id = resultat[0]
             sql2 = "INSERT INTO `familles`(`famille`,`usage_key`) VALUES (\'"+str(famille)+"\',"+str(id)+")"
             cursor.execute(sql2)
             conn.commit()
            except mysql.connector.errors as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
            finally:
                if conn:
                    conn.close()
    return familleliste

recup_famille()