import configKhs
#a travailler car doit etre tres modulable
def addArtefact(artefact,cursor):
    p1 = "INSERT INTO artefacts (`id_artefact`, `libelle`, `modele`,`anProd`,`dateIn`, `longueur`,"
    p2 = "`largeur`, `hauteur`, `poids`, `donateur_key`, `prod_key`, `etat_key`, `localisation_key`,"
    p3 = ") VALUES(\'" + str(artefact.id) + "\',\'" + str(artefact.nom) + "\',\'" + str(artefact.modele) + "\'," + str(artefact.dateProd)
    p4 = "," + str(artefact.dateIn) + "," + str(artefact.) + "," + str(l) + ","+ str(h) + "," + str(k) + ","
    p5 = ""+ str(artefact.collection) + "," + str(artefact.producteur) + "," + str(artefact.etat) + "," + str(artefact.stock)+")"
    sql = p1 + p2 + p3 + p4 + p5
    sql = configKhs.re.sub('None', 'NULL', sql)
    cursor.execute(sql)

def addImage(artefact,cursor):
    for image in artefact.image:
     sql="INSERT INTO images(image,artefact_key) VALUES (\'"+str(image)+"\',\'"+str(artefact.id)+"\')"
     cursor.execute(sql)



