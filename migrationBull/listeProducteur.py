# -*- coding: utf8 -*-
import openpyxl
from catTools import config
import mysql.connector
"""
fonction permettant de repucerer tout les producteur du fichier
"""


def recup_producteur():
    wb = openpyxl.load_workbook(filename='c:\\Users\\jazzt\\desktop\\NAM-IP\\bull.xlsm')
    ws = wb['Inventaire']

    prodliste = []
    for row in ws.iter_rows(min_row=config.min_row, max_col=config.max_column, max_row=config.max_row):
        prod = row[8].value
        if prod is None:
            continue
        elif prod in prodliste:
            continue
        elif str(prod).capitalize() is int:
            continue
        else:
            prodliste.append(prod)
            try:
             conn = mysql.connector.connect(host=config.host, user=config.user, password=config.passwd, database=config.database)
             cursor = conn.cursor()
             sql = "INSERT INTO `producteurs`(`producteur`) VALUES (\""+str(prod)+"\")"
             cursor.execute(sql)
             conn.commit()
            except mysql.connector.errors as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
            finally:
                if conn:
                    conn.close

recup_producteur()