import configKhs
def addArtefact(artefact, cursor):
    p1 = "INSERT INTO artefacts (`id_artefact`, `libelle`, `modele`,`anProd`,`dateIn`, `longueur`,"
    p2 = "`largeur`, `hauteur`, `poids`,`description`, `donateur_key`, `prod_key`, `etat_key`, `localisation_key`"
    p3 = ") VALUES(\'" + str(artefact.getId()) + "\',\'" + str(artefact.getNom()) + "\',\'" + str(artefact.getModele()) + "\'," + str(artefact.getDateProd())
    p4 = ",\'" + str(artefact.getDateIn()) + "\'," + str(artefact.getLongueur()) + "," + str(artefact.getLargeur()) + ","+ str(artefact.getHauteur()) + "," + str(artefact.getPoids())
    p5 = ",\'"+str(artefact.getDescription())+"\'," + str(artefact.getCollection()) + "," + str(artefact.getProducteur()) + "," + str(artefact.getEtat()) + "," + str(artefact.getStock())+")"
    sql = p1 + p2 + p3 + p4 + p5
    sql = configKhs.re.sub('None', 'NULL', sql)
    #print(sql)
    try:
     cursor.execute(sql)
    except configKhs.mysql.connector.errors.DatabaseError as e:
        configKhs.logging.error("artefact:" + str(artefact.getId()) + ";Error %d; %s" % (e.args[0], e.args[1]))
        configKhs.logging.error("requete artefact;" + str(sql) + "\n")

def addImage(artefact,cursor):
    for image in artefact.image:
     sql="INSERT INTO images(image,artefact_key) VALUES (\'"+str(image)+"\',\'"+str(artefact.id)+"\')"
     try:
      cursor.execute(sql)
     except configKhs.mysql.connector.errors.DatabaseError as e:
        configKhs.logging.error("artefact:" + str(artefact.getId()) + ";Error %d; %s" % (e.args[0], e.args[1]))
        configKhs.logging.error("requete artefact;" + str(sql) + "\n")
