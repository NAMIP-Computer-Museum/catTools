from catTools import config


def idArtefact(root):
    return root.find("INVID").text

def nomArtefact(root):
    libelle = ""
    id = root.find("INVID").text
    isbd = root.find("ISBD")
    if isbd is not None:
     titi = isbd.find("Z1/TITI")
     for child in titi:
        if child.text is not None:
            libelle = str(libelle) + str(child.text)
     libelle = config.re.sub('\'', ' ', libelle)
     return libelle
    else:
        config.logging.warning("Artefact:"+str(id)+";pas de libelle")
        return None

def dateInArtefact(root):
     date = "-01-01"
     id = root.find("INVID").text
     if root.find("ISBD/Z0/INV") is not None:
      year = root.find("ISBD/Z0/INV").text
      date =str(year)+date
      return date
     else:
         config.logging.warning("Artefact:"+str(id)+";pas de date d'entrée")
         return None

def modeleArtefact(root):
    if root.find("ISBD/Z2/SXP") is not None:
        return root.find("ISBD/Z2/SXP").text


def dateProdArtefact(root):
    annee = root.find("ISBD/Z4/DT")
    id = root.find("INVID").text
    if (annee is None) or (str(annee.text) == "s.d."):
        config.logging.warning("Artefact:"+str(id)+";pas de date")
        return None
    else:
        return annee.text


def dimensionArtefact(root, artefact):
 try:
    dim = ""
    z5 = root.findall("ISBD/Z5/")
    id = root.find("INVID").text
    for child in z5:
        if child.text is not None:
            dim = str(dim) + str(child.text)
    ref = str(dim).split()
    if len(ref) < 2:
          t = root.findall("ISBD/Z5/T/")
          if len(t) == 4:
           l = config.re.sub(',', '.', t[0].text)
           artefact.setLongueur(l)
           larg = config.re.sub(',', '.', t[1].text)
           artefact.setLargeur(larg)
           haut = config.re.sub(',', '.', t[2].text)
           artefact.setHauteur(haut)
           poids = config.re.sub(',', '.', t[3].text)
           artefact.setPoids(poids)
          elif len(t) == 3:
              l = config.re.sub(',', '.', t[0].text)
              artefact.setLongueur(l)
              larg = config.re.sub(',', '.', t[1].text)
              artefact.setLargeur(larg)
              haut = config.re.sub(',', '.', t[2].text)
              artefact.setHauteur(haut)
              artefact.setPoids = None

    elif str(ref[0]) == "L":
         artefact.setLongueur(float(ref[1]))

         if str(ref[3]) == "l":
            artefact.setLargeur(float(ref[4]))

         if (len(ref) > 6):
            if (str(ref[6]) == "H"):
                artefact.setHauteur(float(ref[7]))
         elif (len(ref) > 6):
            if (config.re.match("^[0-9]*$", str(ref[6]))):
                artefact.setHauteur(float(ref[6]))
         else:
            artefact.setHauteur(None)

         if (len(ref) > 10):
            if (config.re.match("^[0-9]*$", str(ref[8]))):
                 artefact.setPoids(float(ref[8]))
         elif (len(ref) > 10):
            if (config.re.match("^[0-9]*$", str(ref[9]))):
                artefact.setPoids(float(ref[9]))
         else:
            artefact.setPoids(None)

    elif config.re.match("^[0-9]*$", str(ref[0])):
        artefact.setPoids(float(ref[0]))
        artefact.setLongueur(None)
        artefact.setLargeur(None)
        artefact.setHauteur(None)
 except BaseException as e:
     config.logging.warning("artefact:"+str(id)+";pas de dimension")

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
    if root.find("ISBD/Z0/LIEU") is not None:
     loc = root.find("ISBD/Z0/LIEU").text
     sql = "SELECT id_local FROM localisations WHERE localisation = \'" + str(loc) + "\'"
     cursor.execute(sql)
     res = cursor.fetchall()
     for resultat in res:
        id = resultat[0]
     return id
    else :
        config.logging.warning("artefact:"+str(id)+";pas de localisation")
        return None


def recupProducteur(root, cursor):
    id = None
    producteur = root.findall("ISBD/Z4/NXP")
    if len(producteur) == 0:
        prod = "NULL"
        config.logging.warning("artefact:" + str(id) + ";pas de producteur")
    elif len(producteur) == 1:
        prod = producteur[0].text
        if str(prod).__contains__("'"):
         prod = config.re.sub("'", ' ', prod)
    elif len(producteur) == 3:
        prod = producteur[2].text
        if str(prod).__contains__("'"):
         prod = config.re.sub("'", ' ', prod)
    else:
        prod = producteur[1].text
        if str(prod).__contains__("'"):
         prod = config.re.sub("'", ' ', prod)
    sql = "SELECT id_producteur FROM producteurs WHERE producteur =\'" + str(prod) + "\'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for resultat in res:
        id = resultat[0]
    return id


def recupEtat(root, cursor):
    id = None
    if root.find("ISBD/Z7/T") is not None:
     etat = root.find("ISBD/Z7/T").text
     if str(etat).__contains__("'"):
         etat = config.re.sub("'"," ",etat)
     sql = "SELECT id_etat FROM etats WHERE etat =\'" + str(etat) + "\'"
     cursor.execute(sql)
     res = cursor.fetchall()
     for resultat in res:
        id = resultat[0]
     return id
    else:
        config.logging.warning("artefact:"+str(id)+";pas d'etat")
        return None


def recupCollection(root, cursor):
    id = None
    if root.find("ISBD/Z7/T") is not None:
      collection = root.find("ISBD/Z8/NXP").text
      sql = "SELECT id_donateur FROM donateurs WHERE donateur =\'" + str(collection) + "\'"
      cursor.execute(sql)
      res = cursor.fetchall()
      for resultat in res:
        id = resultat[0]
      return id
    else :
        config.logging.warning("artefact:"+str(id)+";pas de collection")
        return None

def recupDescription(root):
  desc = ""
  ref = root.findall("P/T")
  for child in ref:
      desc = desc + str(child.text)
  desc = config.re.sub('●', '-', desc)
  desc = config.re.sub('\'',' ',desc)
  return desc