# coding: utf-8
from catTools import config
import mysql.connector
"""
etat ok .
producteur ok .
donateur ok
appartenance ok .
localisation ok 
conditionnement ok
usage ok .
famille ok . 
artefact ok
recolement ok 
images ok
liens attente 
"""
try:
 conn = mysql.connector.connect(host=config.host, user=config.user, password=config.passwd, database=config.database)
 cursor = conn.cursor()
 #delete de toute les tables avant recreation de celles-ci
 cursor.execute("""
 DROP TABLE IF EXISTS etats,producteurs,donateurs,appartenances,localisations,conditionnements,
 usages,familles,artefacts,recolements,images,liens;
 """)
 #creation de la table etat
 cursor.execute("""
 CREATE TABLE IF NOT EXISTS etats(
     id_etat int(10) NOT NULL AUTO_INCREMENT,
     etat varchar(255) NOT NULL,
     PRIMARY KEY(id_etat)
 );
 """)
 #creation de la table producteur
 cursor.execute("""
 CREATE TABLE IF NOT EXISTS producteurs(
     id_producteur int(10) NOT NULL AUTO_INCREMENT,
     producteur varchar(255) NOT NULL,
     PRIMARY KEY(id_producteur)
 );
 """)
#creation de la table donateur
 cursor.execute("""
 CREATE TABLE IF NOT EXISTS donateurs(
     id_donateur int(10) NOT NULL AUTO_INCREMENT,
     donateur varchar(255) NOT NULL,
     PRIMARY KEY(id_donateur)
 );
 """)
#creation de la table appartenance
 cursor.execute("""
 CREATE TABLE IF NOT EXISTS appartenances(
     id_appart int(10) NOT NULL AUTO_INCREMENT,
     appartenance varchar(255) NOT NULL,
     PRIMARY KEY(id_appart)
 );
 """)
#creation de la table localisation
 cursor.execute("""
 CREATE TABLE IF NOT EXISTS localisations(
     id_local int(10) NOT NULL AUTO_INCREMENT,
     localisation varchar(255) NOT NULL,
     PRIMARY KEY(id_local)
 );
 """)
#creation de la table conditionnement
 cursor.execute("""
 CREATE TABLE IF NOT EXISTS conditionnements(
     id_cond int(10) NOT NULL AUTO_INCREMENT,
     conditionnement varchar(255) NOT NULL,
     localisation_key int NULL,
     PRIMARY KEY(id_cond),
     FOREIGN KEY (localisation_key)
     REFERENCES localisations(id_local)
 );
 """)
#creation de la table usage
 cursor.execute("""
 CREATE TABLE IF NOT EXISTS usages(
     id_usage int(10) NOT NULL AUTO_INCREMENT,
     libelleUsage varchar(255) NOT NULL,
     PRIMARY KEY(id_usage)
 );
 """)
#creation de la table famille
 cursor.execute("""
 CREATE TABLE IF NOT EXISTS familles(
     id_famille int(10) NOT NULL AUTO_INCREMENT,
     famille varchar(255) NOT NULL,
     usage_key int NOT NULL,
     PRIMARY KEY(id_famille),
     FOREIGN KEY (usage_key)
     REFERENCES usages(id_usage)
 );
 """)
#creation de la table d'artefacts
 cursor.execute("""
CREATE TABLE IF NOT EXISTS artefacts (
    id_artefact int(10) NOT NULL,
    libelle varchar(255) DEFAULT NULL,
    modele varchar(255) DEFAULT NULL,
    numSerie varchar(255) DEFAULT NULL,
    anProd int(4) DEFAULT NULL,
    quantite int(5) DEFAULT NULL,
    dateIn date DEFAULT NULL,
    longueur double(3,3) DEFAULT NULL,
    largeur double(3,3) DEFAULT NULL,
    hauteur double(3,3) DEFAULT NULL,
    poids double(3,3) DEFAULT NULL,
    commentaire varchar(255) DEFAULT NULL,
    donateur_key int NULL,
    cond_key int NULL,
    prod_key int NULL,
    etat_key int NULL,
    localisation_key int NULL,
    appart_key int NULL,
    famille_key int NOT NULL,
    PRIMARY KEY(id_artefact),
    FOREIGN KEY (donateur_key) 
    REFERENCES donateurs(id_donateur),
    FOREIGN KEY (cond_key) 
    REFERENCES conditionnements (id_cond),
    FOREIGN KEY (prod_key) 
    REFERENCES producteurs(id_producteur),
    FOREIGN KEY (etat_key) 
    REFERENCES etats(id_etat),
    FOREIGN KEY (localisation_key) 
    REFERENCES localisations(id_local),
    FOREIGN KEY (appart_key) 
    REFERENCES appartenances(id_appart),
    FOREIGN KEY (famille_key) 
    REFERENCES familles(id_famille)    
 );
 """)
 #creation de la table de recolement
 cursor.execute("""
 CREATE TABLE IF NOT EXISTS recolements(
     id_recol int(10) NOT NULL AUTO_INCREMENT,
     recolement date NOT NULL,
     artefact_key int NOT NULL,
     PRIMARY KEY(id_recol),
     FOREIGN KEY (artefact_key)
     REFERENCES artefacts(id_artefact)
 );
 """)
 #creation de la table d'images
 cursor.execute("""
 CREATE TABLE IF NOT EXISTS images(
     id_image int(10) NOT NULL AUTO_INCREMENT,
     image varchar(255) NOT NULL,
     artefact_key int NOT NULL,
     PRIMARY KEY(id_image),
     FOREIGN KEY (artefact_key)
     REFERENCES artefacts(id_artefact)
 );
 """)
 #creation de la table des liens
 #peut etre id d'un artefact ou le numero d'un conditionnement why ?
 cursor.execute("""
 CREATE TABLE IF NOT EXISTS liens(
     principale int NOT NULL,
     secondaire int NOT NULL,
     FOREIGN KEY (principale)
     REFERENCES artefacts(id_artefact),
     FOREIGN KEY (secondaire)
     REFERENCES artefacts(id_artefact),
     PRIMARY KEY (principale,secondaire)
 );
 """)
 conn.commit()
except mysql.connector.errors as e:
     print("Error %d: %s" % (e.args[0], e.args[1]))
finally:
    if conn:
        conn.close()

