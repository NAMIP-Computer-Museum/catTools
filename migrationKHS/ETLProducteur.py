def ETLProducteur(root, cursor):
    id = None
    producteur = root.findall("ISBD/Z4/NXP")
    if len(producteur) == 1:
        prod = producteur[0].text
        #verification existance producteur en DB
        sql = "SELECT id_producteur FROM producteurs WHERE producteur =\'" + str(prod) + "\'"
        cursor.execute(sql)
        res = cursor.fetchall()
        for resultat in res:
          id = resultat[0]
        if id:
          """rien ne se passe"""
        else:
          sql1 ="INSERT INTO producteurs (producteur) VALUES (\'"+str(prod)+"\')"
          cursor.execute(sql1)
    else:
         pays = producteur[0].text
         ville = producteur[1].text
         prod = producteur[2].text
         sql = "SELECT id_producteur FROM producteurs WHERE producteur =\'" + str(prod) + "\'"
         cursor.execute(sql)
         res = cursor.fetchall()
         for resultat in res:
             id = resultat[0]
         if id:
            """rien ne se passe"""
         else:
           sql1 ="INSERT INTO producteurs (producteur,pays,ville) VALUES(\'"+str(prod)+"\',\'"+str(pays)+"\',\'"+str(ville)+"\')"
           cursor.execute(sql1)

