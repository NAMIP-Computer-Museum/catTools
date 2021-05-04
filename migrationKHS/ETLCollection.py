def ETLCollection(root, cursor):
    id = None
    collection = root.find("ISBD/Z8/NXP")
    if collection is not None:
     # verification si la collection est en DB
     sql = "SELECT id_donateur FROM donateurs WHERE donateur =\'" + str(collection.text) + "\'"
     cursor.execute(sql)
     res = cursor.fetchall()
     for resultat in res:
        id = resultat[0]
     if id is None:
      sql1 = "INSERT INTO donateurs (donateur) VALUES(\'"+str(collection.text)+"\')"
      cursor.execute(sql1)
