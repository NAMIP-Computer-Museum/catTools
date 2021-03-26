import configKhs
def idArtefact(root):
    return root.find("INVID").text

def nomArtefact(root):
    libelle =""
    isbd = root.find("ISBD")
    titi = isbd.find("Z1/TITI")
    for child in titi:
        if child.text is not None:
            libelle = str(libelle) + str(child.text)
    return libelle

def dateInArtefact(root):
    return root.find("ISBD/Z0/INV").text

def modeleArtefact(root):
    if root.find("ISBD/Z2/SXP") is not None:
        return root.find("ISBD/Z2/SXP").text

def dateProdArtefact(root):
    if root.find("ISBD/Z4/DT") is not None:
        return root.find("ISBD/Z4/DT").text

def dimensionArtefact(root, artefact):
     dim = ""
     z5 = root.findall("ISBD/Z5/")
     for child in z5:
         if child.text is not None:
             dim = str(dim) + str(child.text)
     ref = str(dim).split()
     if str(ref[0]) == "L":
         artefact.longueur = ref[1]

         if str(ref[3]) == "l":
                artefact.largeur = ref[4]

         if len(ref) > 6:
             if str(ref[6]) == "H":
              artefact.hauteur = ref[7]
         elif len(ref) > 6:
             if configKhs.re.match("^[0-9]*$", str(ref[6])):
                print(ref[6])
                artefact.hauteur = ref[6]
         else:
             artefact.hauteur = None

         if len(ref) > 10:
            if configKhs.re.match("^[0-9]*$", str(ref[8])):
             artefact.poids = ref[8]
         elif len(ref) > 10:
             if configKhs.re.match("^[0-9]*$", str(ref[9])):
                artefact.poids = ref[9]
         else:
             artefact.poids = None

     elif configKhs.re.match("^[0-9]*$", str(ref[0])):
         artefact.poids = ref[0]
         artefact.longeur = None
         artefact.largeur = None
         artefact.hauteur = None

def imageArtefact(root):
    list = []
    img = root.findall("P/AI")
    for i in img:
        image = i.attrib
        ref = str(image).split("'")
        ref = ref[3].split("$")
        ref = ref[0].split("/")
        list.append(ref[1])
    return list

def recupLocalisation(root, cursor):
    id = None
    loc = root.find("ISBD/Z0/LIEU").text
    sql="SELECT id_local FROM localisations WHERE localisation = \'" + str(loc) + "\'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for resultat in res:
        id = resultat[0]
    return id
def recupProducteur(root, cursor):
    id = None
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
def recupEtat(root, cursor):
    id = None
    etat = root.find("ISBD/Z7/T").text
    sql = "SELECT id_etat FROM etats WHERE etat =\'" + str(etat) + "\'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for resultat in res:
        id = resultat[0]
    return id
def recupCollection(root, cursor):
    id = None
    collection = root.find("ISBD/Z8/NXP").text
    sql = "SELECT id_donateur FROM donateurs WHERE donateur =\'" + str(collection) + "\'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for resultat in res:
        id = resultat[0]
    return id