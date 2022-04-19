import logging

"""
Initialisation de l'écriture dans le fichier de logs
"""
logging.basicConfig(
    level=logging.INFO, filename="errorlog.csv", filemode="w+", format="%(levelname)s;%(message)s"
)

def message_avertissement(id_artefact, message, mauvaise_valeur=None):
    logging.warning(str(id_artefact) + ";" + message + ";" + ("" if mauvaise_valeur is None else str(mauvaise_valeur)))


def message_erreur(erreur, id_artefact=None):
    if id_artefact == None:
        logging.error(";Erreur : " + str(erreur))
    else:
        logging.error(str(id_artefact) + ";Erreur : " + str(erreur))
        
def message_info(détails, id_artefact=None, nouvelle_valeur=None, ancienne_valeur=None):
    message = ""
    
    if id_artefact is not None:
        message += str(id_artefact)
    message += ";" + détails + ";"
    if nouvelle_valeur is not None:
        message += str(nouvelle_valeur)
    message += ";"
    if ancienne_valeur is not None:
        message += str(ancienne_valeur)
        
    logging.info(message)


"""
Constantes pour boucler dans le fichier excel de BULL
"""
ligne_min = 15
ligne_max = 3580
colonne_min = 0
colonne_max = 34

"""
Constantes pour les chemins d'accès aux différents fichiers sources
"""
pathkhs = "E:\\NAM-IP\\catTools-git\\catTools_app\\data\\khs"
pathbull = "E:\\NAM-IP\\catTools-git\\catTools_app\\data\\bull\\Inventaire FEBB Master A&R_2022-22-03.xlsm"

"""Constantes pour les paramètres de la base de données"""
host = "localhost"
user = "root"
passwd = "root1234"
database = "test_khs"
