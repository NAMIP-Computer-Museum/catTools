# -*- coding: utf8 -*-
from catTools import config
import utilitaireKhs
import ETLEtat
import ETLCollection
import ETLProducteur
import ETLStock
import Artefact
import xml.etree.ElementTree as ET
import sql
try:
    # ouverture du socket de communication avec la DB
    conn = config.mysql.connector.connect(host=config.host, user=config.user, password=config.passwd, database=config.database)
    cursor = conn.cursor()
    # boucle pour charger les ETL en DB
    for file in config.os.listdir(config.pathkhs):
        if config.re.match('V[0-9]*.xml', file):
            tree = ET.parse("C:\\Users\\jazzt\\PycharmProjects\\pythonProject\\catTools\\data\\khs\\"+str(file))
            root = tree.getroot()
            ETLStock.ETLStock(root, cursor)
            ETLProducteur.ETLProducteur(root, cursor)
            ETLEtat.ETLEtat(root, cursor)
            ETLCollection.ETLCollection(root, cursor)
            conn.commit
except config.mysql.connector.errors.DatabaseError as e:
    config.logging.error("File:"+str(file)+";Error %d;%s" % (e.args[0], e.args[1]))
try:
    # ouverture de la boucle de lecture des fichiers xml
    for file in config.os.listdir(config.pathkhs):
        if config.re.match('V[0-9]*.xml', file):
              tree = ET.parse("C:\\Users\\jazzt\\PycharmProjects\\pythonProject\\catTools\\data\\khs\\"+str(file))
              root = tree.getroot()
            # recherche des données de l'artefact du fichier xml en cours
              id = utilitaireKhs.idArtefact(root)
              artefact = Artefact.Artefact(id,file)
              artefact.setNom(utilitaireKhs.nomArtefact(root))
              artefact.setDateIn(utilitaireKhs.dateInArtefact(root))
              artefact.setModele(utilitaireKhs.modeleArtefact(root))
              artefact.setDateProd(utilitaireKhs.dateProdArtefact(root))
              utilitaireKhs.dimensionArtefact(root, artefact)
              artefact.image = utilitaireKhs.imageArtefact(root)
              artefact.setDescription(utilitaireKhs.recupDescription(root))
             # recherche des données deja en table
              artefact.setStock(utilitaireKhs.recupLocalisation(root, cursor))
              artefact.setProducteur(utilitaireKhs.recupProducteur(root, cursor))
              artefact.setEtat(utilitaireKhs.recupEtat(root, cursor))
              artefact.setCollection(utilitaireKhs.recupCollection(root, cursor))
             # insertion dans les tables
              sql.addArtefact(artefact, cursor)
              sql.addImage(artefact, cursor)
            # commit des modifications dans la DB
              conn.commit()
except config.mysql.connector.errors.DatabaseError as e:
    config.logging.error("File:"+str(file)+";Error %d;%s" % (e.args[0], e.args[1]))
finally:
    # fermeture de la connection
    conn.close

