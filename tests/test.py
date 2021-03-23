import xml.etree.ElementTree as ET
import Artefact
import re
def extract(file):
 tree = ET.parse("data\\"+str(file))
 root = tree.getroot()
 artefact1 = Artefact.Artefact()
 artefact1.clearList()

 """
 recup id
 if (A) et (B)
 """
 artefact1.id = root.find("INVID").text
 """
 recup images 
 """
 img = root.findall("P/AI")
 for i in img:
    image = i.attrib
    ref = str(image).split("'")
    ref = ref[3].split("$")
    ref = ref[0].split("/")
    artefact1.addImage(ref[1])
    "enfant de la balise AI"
    child = i.find("IMG")
    ichild = child.attrib
    ref = str(ichild).split("'")
    ref = ref[3].split("$")
    ref = ref[2].split("/")
    artefact1.addRef(ref[1])


 """
 recup stock et date in dans l'inventaire
 """
 artefact1.stock = root.find("ISBD/Z0/LIEU").text

 artefact1.dateIn = root.find("ISBD/Z0/INV").text
 """
 recup du nom 
 """
 isbd = root.find("ISBD")
 titi = isbd.find("Z1/TITI")
 for child in titi:
    if child.text is not None :
     libelle = str(libelle)+str(child.text)
 artefact1.nom = libelle
 """
 recup du modele, num série ou édition
 """
 if root.find("ISBD/Z2/SXP") is not None:
   artefact1.modele = root.find("ISBD/Z2/SXP").text
 """
 recup producteur + date production
 """
 producteur =root.findall("ISBD/Z4/NXP")
 if len(producteur) == 1:
   artefact1.producteur = producteur[0].text
 else:
     artefact1.producteur = producteur[2].text

 if root.find("ISBD/Z4/DT") is not None:
  artefact1.dateProd = root.find("ISBD/Z4/DT").text

 """
 recup des dimensions
 """
 isbd = root.find("ISBD")
 z5 = isbd.find("Z5/T")
 if z5 is not None:
     z5 = isbd.find("Z5/T")
     sp = str(z5.text).split()
     for item in sp:
      if re.match("^[0-9]*$", item):
          artefact1.addDim(item)
 nb = z5.findall("NB")
 if len(nb) != 0:
  for child in nb:
      dim = child.text
      artefact1.addDim(dim)
 """
 recup de l'état
 """
 artefact1.etat = root.find("ISBD/Z7/T").text

 """
 recup de la collection
 """
 artefact1.collection = root.find("ISBD/Z8/NXP").text

 artefact1.toString()
