import xml.etree.ElementTree as ET

def ETLCollection(file, cursor):
    id = None
    tree = ET.parse("data\\" + str(file))
    root = tree.getroot()
    collection = root.find("ISBD/Z8/NXP").text
    # verification si la collection est en DB
    sql = "SELECT id_donateur FROM donateurs WHERE donateur =\'" + str(collection) + "\'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for resultat in res:
        id = resultat[0]
    if id is None:
     sql1 = "INSERT INTO donateurs (donateur) VALUES(\'"+str(collection)+"\')"
     cursor.execute(sql1)
