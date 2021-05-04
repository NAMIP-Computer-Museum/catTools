from xml.etree.ElementTree import ParseError
import traceback
import config
def ETLProducteur(root, cursor):
 try:
    id = None
    idA = root.find("INVID").text
    producteur = root.findall("ISBD/Z4/NXP")
    if len(producteur) == 0:
         "rien ne se passe"
    elif len(producteur) == 1:
        prod = producteur[0].text
        if str(prod).__contains__("'"):
         prod = config.re.sub("'", ' ', prod)
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
    elif len(producteur) == 3:
         pays = producteur[0].text
         ville = producteur[1].text
         prod = producteur[2].text
         if str(prod).__contains__("'"):
          prod = config.re.sub("'", ' ', prod)
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
    else:
        pays = producteur[0].text
        prod = producteur[1].text
        if str(prod).__contains__("'"):
         prod = config.re.sub("'", ' ', prod)
        if str(prod) != "s.n.":
         sql = "SELECT id_producteur FROM producteurs WHERE producteur =\'" + str(prod) + "\'"
         cursor.execute(sql)
         res = cursor.fetchall()
         for resultat in res:
            id = resultat[0]
         if id:
            """rien ne se passe"""
         else:
            sql1 = "INSERT INTO producteurs (producteur,pays) VALUES(\'" + str(prod) + "\',\'" + str(pays) + "\')"
            cursor.execute(sql1)
 except ParseError as e:
     print ( e.args[0],e.args[1])
     traceback.print_exc()
