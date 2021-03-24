import xml.etree.ElementTree as ET
import configKhs
def idArtefact(file):
    tree = ET.parse("data\\" + str(file))
    root = tree.getroot()
    return root.find("INVID").text

def nomArtefact(file):
    libelle =""
    tree = ET.parse("data\\" + str(file))
    root = tree.getroot()
    isbd = root.find("ISBD")
    titi = isbd.find("Z1/TITI")
    for child in titi:
        if child.text is not None:
            libelle = str(libelle) + str(child.text)
    return libelle

def dateInArtefact(file):
    tree = ET.parse("data\\" + str(file))
    root = tree.getroot()
    return root.find("ISBD/Z0/INV").text

def modeleArtefact(file):
    tree = ET.parse("data\\" + str(file))
    root = tree.getroot()
    if root.find("ISBD/Z2/SXP") is not None:
        return root.find("ISBD/Z2/SXP").text

def dateProdArtefact(file):
    tree = ET.parse("data\\" + str(file))
    root = tree.getroot()
    if root.find("ISBD/Z4/DT") is not None:
        return root.find("ISBD/Z4/DT").text

def dimensionArtefact(file, artefact):
    list = []
    tree = ET.parse("data\\" + str(file))
    root = tree.getroot()
    isbd = root.find("ISBD")
    z5 = isbd.find("Z5/T")
    if z5 is not None:
        z5 = isbd.find("Z5/T")
        sp = str(z5.text).split()
        for item in sp:
            if configKhs.re.match("^[0-9]*$", item):
                list.append(item)
    nb = z5.findall("NB")
    if len(nb) != 0:
        for child in nb:
            dim = child.text
            list.append(dim)
    return list

def imageArtefact(file):
    list = []
    tree = ET.parse("data\\" + str(file))
    root = tree.getroot()
    img = root.findall("P/AI")
    for i in img:
        image = i.attrib
        ref = str(image).split("'")
        ref = ref[3].split("$")
        ref = ref[0].split("/")
        list.append(ref[1])
    return list

def recupLocalisation(file, cursor):
    id = None
    tree = ET.parse("data\\" + str(file))
    root = tree.getroot()
    loc = root.find("ISBD/Z0/LIEU").text
    sql="SELECT id_local FROM localisations WHERE localisation = \'" + str(loc) + "\'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for resultat in res:
        id = resultat[0]
    return id
def recupProducteur(file, cursor):
    id = None
    tree = ET.parse("data\\" + str(file))
    root = tree.getroot()
    producteur = root.findall("ISBD/Z4/NXP")
    if len(producteur) == 1:
        prod = producteur[0].text
    else:
        prod = producteur[2].text
    sql = "SELECT id_producteur FROM producteurs WHERE producteur =\'" + str(prod) + "\'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for resultat in res:
        id = resultat[0]
    return id
def recupEtat(file, cursor):
    id = None
    tree = ET.parse("data\\" + str(file))
    root = tree.getroot()
    etat = root.find("ISBD/Z7/T").text
    sql = "SELECT id_etat FROM etats WHERE etat =\'" + str(etat) + "\'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for resultat in res:
        id = resultat[0]
    return id
def recupCollection(file, cursor):
    id = None
    tree = ET.parse("data\\" + str(file))
    root = tree.getroot()
    collection = root.find("ISBD/Z8/NXP").text
    sql = "SELECT id_donateur FROM donateurs WHERE donateur =\'" + str(collection) + "\'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for resultat in res:
        id = resultat[0]
    return id