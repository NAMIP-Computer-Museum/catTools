import config
import utilitaireKhs
import xml.etree.ElementTree as ET
from khs import ETLStock, ETLProducteur, ETLEtat, ETLCollection, sql

file = "V0000333.xml"
libelle = ""
idref = ""
i = 1
tree = ET.parse(str(configTest.path)+"\\"+file)
root = tree.getroot()
conn = configTest.mysql.connector.connect(host=configTest.host, user=configTest.user, password=configTest.passwd,database=configTest.database)
cursor = conn.cursor()
ETLStock.ETLStock(root, cursor)
ETLProducteur.ETLProducteur(root, cursor)
ETLEtat.ETLEtat(root, cursor)
ETLCollection.ETLCollection(root, cursor)
conn.commit

tabArtefact = []
        #recherche id
idref = root.find("INVID").text

        #recherche du libelle
isbd = root.find("ISBD")

if isbd is not None:
 titi = isbd.find("Z1/TITI")
for child in titi:
   if child.text is not None:
     libelle = str(libelle) + str(child.text)
     libelle = configTest.re.sub('\'', ' ', libelle)

if libelle.find(")")!=-1:
    libelle = str(libelle).split(")")
    for ar in libelle:
        id = str(idref)+"."+str(i)
        artefact = configTest.Artefact.Artefact(id,file)
        artefact.setNom(ar)
        tabArtefact.append(artefact)
        i = i+1
dim = ""
z5 = root.findall("ISBD/Z5/")
id = root.find("INVID").text
for child in z5:
    if child.text is not None:
        dim = str(dim) + str(child.text)
    ref = str(dim).split()
    if len(ref) < 2:
        "len apres avoir les child nb = 8"
        t = root.findall("ISBD/Z5/T/")
        i = 0
        for ar in tabArtefact:
            if i < len(t)-1:
             L = configTest.re.sub(',', '.', t[i].text)
             ar.setLongueur(L)
             i = i+1
             l = configTest.re.sub(',', '.', t[i].text)
             ar.setLargeur(l)
             i = i+1
             h = configTest.re.sub(',', '.', t[i].text)
             ar.setHauteur(h)
             i = i+1
             p = configTest.re.sub(',', '.', t[i].text)
             ar.setPoids(p)
             i =i+1
for ar in tabArtefact:
    print(ar.getId(), ar.getNom(),ar.getLongueur(),ar.largeur,ar.getHauteur(),ar.getPoids())
dateIn = utilitaireKhs.dateInArtefact(root)
numSerie = utilitaireKhs.modeleArtefact(root)
anprod = utilitaireKhs.dateProdArtefact(root)
image = utilitaireKhs.imageArtefact(root)
description = utilitaireKhs.recupDescription(root)
local =utilitaireKhs.recupLocalisation(root, cursor)
prod = utilitaireKhs.recupProducteur(root, cursor)
etat =utilitaireKhs.recupEtat(root, cursor)
collection =utilitaireKhs.recupCollection(root, cursor)
for ar in tabArtefact:
    ar.setModele(numSerie)
    ar.setDateIn(dateIn)
    ar.setDateProd(anprod)
    ar.image = image
    ar.setDescription(description)
    ar.setStock(local)
    ar.setProducteur(prod)
    ar.setEtat(etat)
    ar.setCollection(collection)
try :
  for ar in tabArtefact:
     print(ar.getId())
     sql.addArtefact(ar, cursor)
     sql.addImage(ar, cursor)
except configTest.mysql.connector.errors.DatabaseError as e:
    configTest.logging.error("File:"+str(file)+";Error %d;%s" % (e.args[0], e.args[1]))
finally:
    # fermeture de la connection
    conn.close
conn.commit()

