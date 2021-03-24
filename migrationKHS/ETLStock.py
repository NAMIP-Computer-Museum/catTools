import xml.etree.ElementTree as ET
def ETLStock(file, cursor):
    id = None
    tree = ET.parse("data\\" + str(file))
    root = tree.getroot()
    loc = root.find("ISBD/Z0/LIEU").text
    #verification si la localisation est en DB
    sql="SELECT id_local FROM localisations WHERE localisation = \'" + str(loc) + "\'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for resultat in res:
        id = resultat[0]
    if id:
        """"rien ne se passe"""
    else:
      sql1 ="INSERT INTO localisations (localisation) VALUES(\'"+str(loc)+"\')"
      cursor.execute(sql1)