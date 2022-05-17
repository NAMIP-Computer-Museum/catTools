import string

import mysql.connector

lettres_par_défaut = lambda exceptions, lettres: [
    lettre for lettre in lettres if lettre not in exceptions
]


def localisation_to_string(lieu: str, armoire: str, colonne: str, planche: str) -> str:
    return "%s-%s%s.%s" % (lieu, armoire, colonne, planche)


def liste_lettres(debut: str, fin: str) -> list:
    lettres = list(string.ascii_uppercase)

    i_debut = lettres.index(debut.upper())
    i_fin = lettres.index(fin.upper())

    return lettres[i_debut : (i_fin + 1)]


def gen_localisations_biblio_bull():
    localisations = []

    for colonne in range(1, 12):
        if colonne == 1:
            for planche in range(1, 6):
                localisations.append("B-R" + str(colonne) + "." + str(planche))
        elif colonne in ([2, 3, 6, 7, 8, 9, 10, 11]):
            for planche in range(1, 7):
                localisations.append("B-R" + str(colonne) + "." + str(planche))
        else:
            for planche in range(1, 8):
                localisations.append("B-R" + str(colonne) + "." + str(planche))

    return localisations


def gen_localisations(
    lieu: str, armoires: list, colonnes: list, planches: dict
) -> list:
    localisations = []
    nb_planches = 0
    for armoire in armoires:
        for colonne in colonnes:
            for i in range(len(planches)):
                if armoire in planches[i]["lettres"]:
                    nb_planches = planches[i]["nombre"]
                    break
            for i in range(1, nb_planches + 1):
                localisations.append(
                    localisation_to_string(lieu, armoire, str(colonne), str(i))
                )

    return localisations


def check_localisations(localisations: list) -> list:
    try:
        check = []
        connexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234",
            database="test_khs",
        )
        cursor = connexion.cursor()
        sql = "SELECT localisation FROM localisations"
        cursor.execute(sql)
        result = cursor.fetchall()
        result = [result[i][0] for i in range(len(result))]
        for loc in localisations:
            check.append({"localisation": loc, "est_présente": loc in result})

        return check
    except:
        pass
    finally:
        connexion.close()


if __name__ == "__main__":
    armoires_biblio = liste_lettres("A", "N")
    colonnes_biblio = list(range(1, 4))
    planches_biblio = [
        {"lettres": lettres_par_défaut(["N", "F", "G"], armoires_biblio), "nombre": 5},
        {"lettres": ["N"], "nombre": 4},
        {"lettres": ["F", "G"], "nombre": 6},
    ]
    armoires_mur = liste_lettres("A", "R")
    colonnes_mur = [1]
    planches_mur = [
        {"lettres": ["O"], "nombre": 1},
        {"lettres": ["I", "J", "K", "L"], "nombre": 4},
        {"lettres": ["C", "D", "E", "H", "M", "N"], "nombre": 5},
        {"lettres": ["A", "B", "F", "G", "P", "Q", "R"], "nombre": 6},
    ]
    armoires_c8 = liste_lettres("A", "R")
    colonnes_c8 = [1]
    planches_c8 = [
        {
            "lettres": lettres_par_défaut(
                ["C", "P", "Q", "R", "A", "B", "F"], armoires_c8
            ),
            "nombre": 5,
        },
        {"lettres": ["C", "P", "Q", "R"], "nombre": 4},
        {"lettres": ["A", "B", "F"], "nombre": 6},
    ]
    armoires_c6 = liste_lettres("A", "K")
    colonnes_c6 = [1]
    planches_c6 = [
        {"lettres": lettres_par_défaut(["I", "J", "K"], armoires_c6), "nombre": 5},
        {"lettres": ["I"], "nombre": 4},
        {"lettres": ["J"], "nombre": 6},
        {"lettres": ["K"], "nombre": 7},
    ]
    armoires_c7 = liste_lettres("A", "F")
    colonnes_c7 = [1]
    planches_c7 = [{"lettres": armoires_c7, "nombre": 5}]
    armoires_c4 = liste_lettres("A", "R")
    colonnes_c4 = [1]
    planches_c4 = [
        {
            "lettres": lettres_par_défaut(
                ["A", "B", "E", "D", "F", "G", "H"], armoires_c4
            ),
            "nombre": 5,
        },
        {"lettres": ["A", "B"], "nombre": 4},
        {"lettres": ["E"], "nombre": 6},
        {"lettres": ["D", "F", "G", "H"], "nombre": 7},
    ]
    armoires_c5 = liste_lettres("A", "H")
    colonnes_c5 = [1]
    planches_c5 = [
        {"lettres": ["A", "B", "C", "D"], "nombre": 4},
        {"lettres": ["E", "F", "G", "H"], "nombre": 5},
    ]

    localisations = gen_localisations(
        "B", armoires_biblio, colonnes_biblio, planches_biblio
    )
    localisations += gen_localisations("R", armoires_mur, colonnes_mur, planches_mur)
    localisations += gen_localisations("C6", armoires_c6, colonnes_c6, planches_c6)
    localisations += gen_localisations("C8", armoires_c8, colonnes_c8, planches_c8)
    localisations += gen_localisations("C7", armoires_c7, colonnes_c7, planches_c7)
    localisations += gen_localisations("C5", armoires_c5, colonnes_c5, planches_c5)
    localisations += gen_localisations("C4", armoires_c4, colonnes_c4, planches_c4)
    localisations += gen_localisations_biblio_bull()

    check = check_localisations(localisations)

    file = open("localisations\\localisations.csv", mode="w")
    for loc in check:
        file.write(
            loc["localisation"]
            + ","
            + ("PRESENTE" if loc["est_présente"] else "ABSENTE")
            + "\n"
        )
    file.close()
