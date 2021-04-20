# -*- coding: utf8 -*-
import openpyxl
from catTools import config
"""
fonction qui va recuperer tout les usages du fichiers
mettre constante ou fichier de config 
"""


def recup_usage(cursor):
    wb = openpyxl.load_workbook(filename='c:\\Users\\jazzt\\desktop\\NAM-IP\\bull.xlsm')
    ws = wb['Inventaire']

    for row in ws.iter_rows(min_row=config.min_row, max_col=config.max_column, max_row=config.max_row):
        usage = row[1].value
        idA = row[0].value
        id = None
        sql = "SELECT id_usage FROM usages WHERE libelleUsage =\'" + str(usage).upper() + "\'"
        cursor.execute(sql)
        res = cursor.fetchone()
        if res:
           """rien ne se passe"""
        else:
            if (usage is int) or (usage is None):
                config.logging.warning("artefact:"+str(idA)+"-usage n'est pas correct ou vide")
            else:
              sql1 ="INSERT INTO usages (libelleUsage) VALUES(\'"+str(usage).upper()+"\')"
              cursor.execute(sql1)

