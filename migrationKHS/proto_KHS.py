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
            tree = ET.parse(str(file))
            root = tree.getroot()
            ETLStock.ETLStock(root, cursor)
            ETLProducteur.ETLProducteur(root, cursor)
            ETLEtat.ETLEtat(root, cursor)
            ETLCollection.ETLCollection(root, cursor)
            conn.commit
    # ouverture de la boucle de lecture des fichiers xml

    for file in configKhs.os.listdir(configKhs.path):
        if configKhs.re.match('V[0-9]*.xml', file):
             tree = ET.parse(str(file))
             root = tree.getroot()
            # creation d'une instance de la classe artefact
             artefact = configKhs.Artefact.Artefact()
             artefact.clearList()
            # recherche des données de l'artefact du fichier xml en cours
             artefact.id = utilitaireKhs.idArtefact(file)
             artefact.libelle = utilitaireKhs.nomArtefact(file)
             artefact.dateIn = utilitaireKhs.dateInArtefact(file)
             artefact.modele = utilitaireKhs.modeleArtefact(file)
             artefact.dateProd = utilitaireKhs.dateProdArtefact(file)
             artefact.dimension = utilitaireKhs.dimensionArtefact(file)
             artefact.image = utilitaireKhs.imageArtefact(file)
             # recherche des données deja en table
             artefact.stock = utilitaireKhs.recupLocalisation(file, cursor)
             artefact.producteur = utilitaireKhs.recupProducteur(file, cursor)
             artefact.etat = utilitaireKhs.recupEtat(file, cursor)
             artefact.collection = utilitaireKhs.recupCollection(file, cursor)
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
"""
     recuperation des id des tables extérieures au artéfacts
     insert dans la table artefacts
     insert dans la table images

except:
  log => fichier de log     
"""

