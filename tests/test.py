import xml.etree.ElementTree as ET
tree = ET.parse('c:\\Users\\jazzt\\PycharmProjects\\pythonProject\\catTools\\data\\KHS\\xml1.xml')
root = tree.getroot()
libelle = ""
"""
recup id
"""
id = root.find("INVID").text
print(id)
"""
recup images 
garder le nom de l'image 
"""
img = root.findall("P/AI")
for i in img:
    image = i.attrib
    ref = str(image).split("'")
    image = ref[3].split("$")
    print(image[0])
    "enfant de la balise AI"
    child = i.find("IMG")
    ichild = child.attrib
    ref =str(ichild).split("'")
    ichild = ref[3].split("$")
    print(ichild[2])
"""
recup stock et date in dans l'inventaire
"""
stock = root.find("ISBD/Z0/LIEU").text
print(stock)
dateIn = root.find("ISBD/Z0/INV").text
print(dateIn)
"""
recup du nom 
"""
isbd = root.find("ISBD")
titi = isbd.find("Z1/TITI")
for child in titi:
    libelle = str(libelle)+str(child.text)
print(libelle)
"""
recup du modele, num série ou édition
"""
modele = root.find("ISBD/Z2/SXP").text
print(modele)
"""
recup producteur + date production
"""
producteur = root.find("ISBD/Z4")[5].text
print(producteur)
dateProd = root.find("ISBD/Z4")[7].text
print(dateProd)
"""
recup des dimensions
"""
isbd = root.find("ISBD")
z5 = isbd.find("Z5/T")
nb = z5.findall("NB")
for child in nb:
     dim = child.text
     print(dim)

"""
recup de l'état
"""
etat = root.find("ISBD/Z7/T").text
print(etat)
"""
recup de la collection
"""
collection = root.find("ISBD/Z8/NXP").text
print(collection)
ref = root.find("ISBD/Z8/REF").text
print(ref)