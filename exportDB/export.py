from catTools import config
import os
import utilitaireExport
try:
 conn = config.mysql.connector.connect(host=config.host, user=config.user, password=config.passwd, database=config.database)
 cursor = conn.cursor()
 if not os.path.isfile(config.filename):
     print("nouveau fichier")
     wb = config.openpyxl.Workbook()
     ws = wb.active
     ws.title = "db"
     utilitaireExport.stylesheet(ws)
     utilitaireExport.insertArtefact(ws,cursor)
     utilitaireExport.wrapcolumn(ws,5000)
finally:
    conn.close
    wb.save(filename=config.filename)
