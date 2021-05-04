from catTools import config
def addArtefact(artefact, cursor):
    p1 = "INSERT INTO artefacts (`id_artefact`,`sourceFile`, `libelle`, `modele`,`anProd`,`dateIn`, `longueur`,"
    p2 = "`largeur`, `hauteur`, `poids`,`description`, `donateur_key`, `prod_key`, `etat_key`, `localisation_key`"
    p3 = ") VALUES(\'" + str(artefact.getId()) + "\',\'"+str(artefact.getFile())+"\',\'" + str(artefact.getNom()) + "\',\'" + str(artefact.getModele()) + "\'," + str(artefact.getDateProd())
    if artefact.getDateIn() is not None:
     p4 = ",\'" + str(artefact.getDateIn()) + "\'," + str(artefact.getLongueur()) + "," + str(artefact.getLargeur()) + ","+ str(artefact.getHauteur()) + "," + str(artefact.getPoids())
    else:
     p4 = "," + str(artefact.getDateIn()) + "," + str(artefact.getLongueur()) + "," + str(artefact.getLargeur()) + "," + str(artefact.getHauteur()) + "," + str(artefact.getPoids())

    p5 = ",\'"+str(artefact.getDescription())+"\'," + str(artefact.getCollection()) + "," + str(artefact.getProducteur()) + "," + str(artefact.getEtat()) + "," + str(artefact.getStock())+")"
    sql = p1 + p2 + p3 + p4 + p5
    sql = config.re.sub('None', 'NULL', sql)
    try:
     cursor.execute(sql)
    except config.mysql.connector.errors.DatabaseError as e:
        config.logging.error("artefact:" + str(artefact.getFile()) + ";Error %d; %s" % (e.args[0], e.args[1]))
        config.logging.error("requete artefact;" + str(sql) + "\n")

def addImage(artefact,cursor):
    for image in artefact.image:
     sql="INSERT INTO images(image,artefact_key) VALUES (\'"+str(image)+"\',\'"+str(artefact.id)+"\')"
     try:
      cursor.execute(sql)
     except config.mysql.connector.errors.DatabaseError as e:
        config.logging.error("artefact:" + str(artefact.getFile()) + ";Error %d; %s" % (e.args[0], e.args[1]))
        config.logging.error("requete artefact;" + str(sql) + "\n")
