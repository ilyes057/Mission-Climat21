import sqlite3
from sqlite3 import IntegrityError
import pandas

# Pointeur sur la base de données
data = sqlite3.connect("data/climat_france.db")
data.execute("PRAGMA foreign_keys = 1")

# Fonction permettant d'exécuter toutes les requêtes sql d'un fichier
# Elles doivent être séparées par un point-virgule
def updateDBfile(data:sqlite3.Connection, file):

    # Lecture du fichier et placement des requêtes dans un tableau
    createFile = open(file, 'r')
    createSql = createFile.read()
    createFile.close()
    sqlQueries = createSql.split(";")

    # Exécution de toutes les requêtes du tableau
    cursor = data.cursor()
    for query in sqlQueries:
        cursor.execute(query)

# Action en cas de clic sur le bouton de création de base de données
def createDB():
    try:
        # On exécute les requêtes du fichier de création
        updateDBfile(data, "data/createDB.sql")
    except Exception as e:
        print ("L'erreur suivante s'est produite lors de la création de la base : " + repr(e) + ".")
    else:
        data.commit()
        print("Base de données créée avec succès.")

# En cas de clic sur le bouton d'insertion de données
#TODO Q4 Modifier la fonction insertDB pour insérer les données dans les nouvelles tables
def insertDB():
    try:
        # '{}' : paramètre de la requête qui doit être interprété comme une chaine de caractères dans l'insert
        # {}   : paramètre de la requête qui doit être interprété comme un nombre dans l'insert
        # la liste de noms en 3e argument de read_csv_file correspond aux noms des colonnes dans le CSV
        # ATTENTION : les attributs dans la BD sont généralement différents des noms de colonnes dans le CSV
        # Exemple : date_mesure dans la BD et date_obs dans le CSV

        # On ajoute les anciennes régions
        read_csv_file(
            "data/csv/Communes.csv", ';',
            "insert into Regions values (?,?)",
            ['Code Région', 'Région']
        )

        # On ajoute les nouvelles régions
        read_csv_file(
            "data/csv/AnciennesNouvellesRegions.csv", ';',
            "insert into Regions values (?,?)",
            ['Nouveau Code', 'Nom Officiel Région Majuscule']
        )

        # On ajoute les départements référencés avec les anciennes régions
        read_csv_file(
            "data/csv/Communes.csv", ';',
            "insert into Departements (code_departement, nom_departement,code_region) values (?, ?, ?)",
            ['Code Département', 'Département', 'Code Région']
        )

        # On renseigne la zone climatique des départements
        read_csv_file(
            "data/csv/ZonesClimatiques.csv", ';',
            "update Departements set zone_climatique = ? where code_departement = ?",
            ['zone_climatique', 'code_departement']
        )

        # On modifie les codes région des départements pour les codes des nouvelles régions
        read_csv_file(
            "data/csv/AnciennesNouvellesRegions.csv", ';',
            "update Departements set code_region = ? where code_region = ?",
            ['Nouveau Code', 'Anciens Code']
        )

        # On supprime les anciennes régions, sauf si l'ancien code et le nouveau sont identiques (pour ne pas perdre les régions qui n'ont pas changé de code)
        read_csv_file(
            "data/csv/AnciennesNouvellesRegions.csv", ';',
            "delete from Regions where code_region = ? and ? <> ?",
            ['Anciens Code', 'Anciens Code', 'Nouveau Code']
        )
        print("Les erreurs UNIQUE constraint sont normales car on insère une seule fois les Regions et les Départements")
        print("Insertion de mesures en cours...cela peut prendre un peu de temps")
        # On ajoute les mesures
        read_csv_file(
             "data/csv/Mesures.csv", ';',
             "insert into Mesures values (?, ?, ?, ?, ?)",
             ['code_insee_departement', 'date_obs', 'tmin', 'tmax', 'tmoy']
        )
        read_csv_file(
            "data/csv/Communes.csv", ';',
            "insert into Communes values (?,?,?,?,?,?,?,?,?)",
            ['Code Commune', 'Code Département', 'Commune', 'Statut', 'Population', 'Altitude Moyenne', 'Superficie',
             'Code Canton', 'Code Arrondissement']
        )
        # Insertion des données générales des travaux
        read_csv_file_2table(
            "data/csv/Isolation.csv", ';',
            "INSERT INTO Travaux VALUES ({},'{}', {}, {}, {}, {}, '{}', {})",
            ['code_departement', 'code_region', 'cout_total_ht', 'cout_induit_ht', 'annee_travaux', 'type_logement',
             'annee_construction'],
            "INSERT INTO Izolations VALUES ({}, '{}','{}', {},  {},{}, '{}', {}, {}, {}, '{}', {})",
            ['poste_isolation', 'isolant', 'epaisseur', 'surface', 'code_region', 'code_departement', 'cout_total_ht',
             'cout_induit_ht', 'annee_travaux', 'type_logement', 'annee_construction'],
            40
        )

        read_csv_file_2table(
            "data/csv/Photovoltaique.csv", ';',
            "INSERT INTO Travaux VALUES ({},'{}', {}, {}, {}, {}, '{}', {})",
            ['code_departement', 'code_region', 'cout_total_ht', 'cout_induit_ht', 'annee_travaux', 'type_logement',
             'annee_construction'],
            "INSERT INTO Photovoltaiques VALUES ({}, {}, '{}', {}, '{}', {}, {}, {}, '{}', {})",
            ['puissance_installee', 'type_panneaux', 'code_region', 'code_departement', 'cout_total_ht',
             'cout_induit_ht', 'annee_travaux', 'type_logement', 'annee_construction'],
            1
        )

        read_csv_file_2table(
            "data/csv/Chauffage.csv", ';',
            "INSERT INTO Travaux VALUES ({},'{}', {}, {}, {}, {}, '{}', {})",
            ['code_departement', 'code_region', 'cout_total_ht', 'cout_induit_ht', 'annee_travaux', 'type_logement',
             'annee_construction'],
            "INSERT INTO Chauffages VALUES ({},'{}','{}', '{}',  '{}',{}, '{}', {}, {}, {}, '{}', {})",
            ['energie_chauffage_avt_travaux', 'energie_chauffage_installee', 'generateur', 'type_chaudiere',
             'code_region', 'code_departement', 'cout_total_ht', 'cout_induit_ht', 'annee_travaux', 'type_logement',
             'annee_construction'],
            5001
        )



    except Exception as e:
        print ("L'erreur suivante s'est produite lors de l'insertion des données : " + repr(e) + ".")
    else:
        data.commit()
        print("Un jeu de test a été inséré dans la base avec succès.")

# En cas de clic sur le bouton de suppression de la base
def deleteDB():
    try:
        updateDBfile(data, "data/deleteDB.sql")
    except Exception as e:
        print ("L'erreur suivante s'est produite lors de la destruction de la base : " + repr(e) + ".")
    else:
        data.commit()
        print("La base de données a été supprimée avec succès.")

def read_csv_file(csvFile, separator, query, columns):
    # Lecture du fichier CSV csvFile avec le séparateur separator
    # pour chaque ligne, exécution de query en la formatant avec les colonnes columns
    df = pandas.read_csv(csvFile, sep=separator)
    df = df.where(pandas.notnull(df), None)

    cursor = data.cursor()
    for ix, row in df.iterrows():
        try:
            tab = []
            for i in range(len(columns)):

                # pour échapper les noms avec des apostrophes, on remplace dans les chaines les ' par ''
                if isinstance(row[columns[i]], str):
                    row[columns[i]] = row[columns[i]].replace("'","''")
                tab.append(row[columns[i]])

            print(query)
            cursor.execute(query, tuple(tab))
        except IntegrityError as err:
            print(err)


def read_csv_file_2table(csvFile, separator, query, columns, query1, columns1, iddep):
    # Chargement du CSV
    df = pandas.read_csv(csvFile, sep=separator)
    df = df.where(pandas.notnull(df), 'null')  # Remplace NaN par 'null'
    idcopie = iddep
    cursor = data.cursor()

    for ix, row in df.iterrows():
        try:
            tab = []
            tab2 = []

            # Traitement des colonnes pour la première table
            for i in range(len(columns)):
                value = row[columns[i]]

                # Nettoyage des données
                #if columns[i] == 'annee_construction' and isinstance(value, str):
                 #   value = extract_year(value)
                if columns[i] == 'code_departement' and isinstance(value, float):
                    value = int(value)
                if isinstance(value, str):
                    value = value.replace("'", "''")  # Échappe les apostrophes

                tab.append(value)

            # Traitement des colonnes pour la deuxième table
            for i in range(len(columns1)):
                value = row[columns1[i]]

                # Nettoyage des données
                #if columns1[i] == 'annee_construction' and isinstance(value, str):
                #    value = extract_year(value)
                if columns1[i] == 'code_departement' and isinstance(value, float):
                    value = int(value)
                if isinstance(value, str):
                    value = value.replace("'", "''")  # Échappe les apostrophes

                tab2.append(value)

            # Formatage des requêtes SQL
            formatedQuery = query.format(*([idcopie] + tab))
            formatedQuery1 = query1.format(*([idcopie] + tab2))
            idcopie += 1

            # Débogage : affichage des requêtes
            print("Execution Query 1:", formatedQuery)
            cursor.execute(formatedQuery)
            print("Execution Query 2:", formatedQuery1)
            cursor.execute(formatedQuery1)

        except IntegrityError as err:
            print(f"IntegrityError at row {ix}: {err}")
        except Exception as e:
            print(f"Error at row {ix}: {e}")


