# -*- coding: utf8 -*-
import configKhs
import utilitaireKhs
import ETLEtat
import ETLCollection
import ETLProducteur
import ETLStock
import xml.etree.ElementTree as ET
import sql
try:
    # ouverture du socket de communication avec la DB
    conn = configKhs.mysql.connector.connect(host=configKhs.host, user=configKhs.user, password=configKhs.passwd, database=configKhs.database)
    cursor = conn.cursor()
    # boucle pour charger les ETL en DB
    for file in configKhs.os.listdir(configKhs.path):
        if configKhs.re.match('V[0-9]*.xml', file):
            tree = ET.parse("data\\"+str(file))
            root = tree.getroot()
            ETLStock.ETLStock(root, cursor)
            ETLProducteur.ETLProducteur(root, cursor)
            ETLEtat.ETLEtat(root, cursor)
            ETLCollection.ETLCollection(root, cursor)
            conn.commit
    # ouverture de la boucle de lecture des fichiers xml
    for file in configKhs.os.listdir(configKhs.path):
        if configKhs.re.match('V[0-9]*.xml', file):
              tree = ET.parse("data\\"+str(file))
              root = tree.getroot()
            # recherche des données de l'artefact du fichier xml en cours
              id = utilitaireKhs.idArtefact(root)
              artefact = configKhs.Artefact.Artefact(id)
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
except configKhs.mysql.connector.errors.DatabaseError as e:
    print("Error %d: %s" % (e.args[0], e.args[1]))
finally:
    # fermeture de la connection
    conn.close

