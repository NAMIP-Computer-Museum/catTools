# -*- coding: utf8 -*-
import logging
import re
import os
import mysql.connector
import datetime
import openpyxl
"""
initialisation de l'ecriture dans un file du logging
"""
logging.basicConfig(filename="errorlog.txt",filemode="w",format = "%(levelname)s;%(message)s")
"""
initialisation variable de la boucle du fichier
"""
min_row = 7
# nombre maximum de ligne dans le fichier de test: 678
#nombre maximum dans le vrai fichier: ?
max_row = 678
max_column = 34
min_column = 0
# dossier ou se trouve les différents fichiers xml
pathkhs = 'C:\\Users\\jazzt\\PycharmProjects\\pythonProject\\catTools\\data\\khs'
pathBull = 'C:\\Users\\jazzt\\PycharmProjects\\pythonProject\\catTools\\data\\Bull\\extractBull.xlsm'
"""
initalisation parametres connection DB locale
"""
#"""
host = "localhost"
user = "root"
passwd = ""
database = "nam_ip"
#"""

"""
initialisation parametres connection DB distante
"""
"""
host = "cl1-sql11.phpnet.org"
database = "durnal6"
user = "durnal6"
passwd = "z56p1AEmh4Ry"
#"""

"""
initinalisation parametres connection DB locale KHS
"""
"""
host = "localhost"
user = "root"
passwd = ""
database = "Khs"
#"""

"""
config export en excel
"""
filename = "exportDB"+str(datetime.date.today())+".xlsx"
wrap = openpyxl.styles.Alignment(wrap_text=True)
font = openpyxl.styles.Font(size=12,
                            bold=True)