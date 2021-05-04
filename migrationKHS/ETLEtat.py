import config
def ETLEtat(root, cursor):
    id = None
    etat = root.find("ISBD/Z7/T")
    if etat is not None:
      etat = etat.text
      if str(etat).__contains__("'"):
          etat = config.re.sub("'"," ",etat)
     # verification si l etat est en DB
      sql = "SELECT id_etat FROM etats WHERE etat =\'" + str(etat) + "\'"
      cursor.execute(sql)
      res = cursor.fetchall()
      for resultat in res:
        id = resultat[0]
      if id:
        """rien ne se passe"""
      else:
       sql1 ="INSERT INTO etats (etat) VALUES(\'"+str(etat)+"\')"
       cursor.execute(sql1)