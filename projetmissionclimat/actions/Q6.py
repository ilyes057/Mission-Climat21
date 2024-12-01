import tkinter as tk
from utils import display
from utils import db
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(1500, 800, self)
        self.title('Q6 : températures en Isère en 2018')
        display.defineGridDisplay(self, 1, 1)

        # Requête pour obtenir les records de température historiques (min et max)
        query = """
            SELECT 
            strftime('%Y-%m-%d', date_mesure) AS date,STRFTIME("%d", date_mesure) AS Jour,
            STRFTIME("%m", date_mesure) AS Mois,
            MIN(temperature_moy_mesure) AS temp_min_historique,
            MAX(temperature_moy_mesure) AS temp_max_historique
            FROM Mesures
            WHERE NOT (STRFTIME("%d", date_mesure) = '29' AND STRFTIME("%m", date_mesure) = '02')
            GROUP BY Jour, Mois
            ORDER BY Mois, Jour
        """
        try:
            cursor = db.data.cursor()
            result = cursor.execute(query).fetchall()
            cursor.close()
        except Exception as e:
            print(f"Erreur lors de la requête des records de températures : {repr(e)}")
            return

        # Préparation des données pour le graphique
        graph1, graph2, graph3, graph4 = [], [], [], []
        tabx = []

        for row in result:
            graph1.append(row[3])  # Record minimum temperature
            graph2.append(row[4])  # Record maximum temperature

        # Requête pour obtenir les départements les plus chauds et froids de la zone H1 pour 2018
        query2 = """
        WITH depatement_temp_moy_H1 AS (
            SELECT code_departement, AVG(temperature_moy_mesure) AS moyenne_temperature
            FROM Mesures
            JOIN Departements USING (code_departement)
            WHERE zone_climatique = 'H1' AND strftime('%Y', date_mesure) = '2018'
            GROUP BY code_departement
            )
            SELECT 
            DISTINCT code_departement AS Dep_plus_froid
            FROM depatement_temp_moy_H1
            WHERE moyenne_temperature = (SELECT MIN(moyenne_temperature) FROM depatement_temp_moy_H1)

            UNION ALL

            SELECT 
            DISTINCT code_departement AS Dep_plus_chaud
            FROM depatement_temp_moy_H1
            WHERE moyenne_temperature = (SELECT MAX(moyenne_temperature) FROM depatement_temp_moy_H1);
        """
        try:
            cursor = db.data.cursor()
            row = cursor.execute(query2).fetchall()  # Récupère à la fois les départements froid et chaud
            Dep_Min = row[0][0]  # Département le plus froid
            Dep_Max = row[1][0]  # Département le plus chaud
        except Exception as e:
            print(f"Erreur lors de la requête des départements H1 : {repr(e)}")
            return

        # Récupération des températures pour le département le plus froid
        query3 = """
            SELECT date_mesure, temperature_moy_mesure
            FROM Mesures
            WHERE code_departement = ? AND strftime('%Y', date_mesure) = '2018'
            ORDER BY date_mesure
        """
        try:
            cursor = db.data.cursor()
            result3 = cursor.execute(query3, [Dep_Min]).fetchall()
            cursor.close()
        except Exception as e:
            print(f"Erreur lors de la requête des températures froides : {repr(e)}")
            return

        # Récupération des températures pour le département le plus chaud
        query4 = """
            SELECT date_mesure, temperature_moy_mesure 
            FROM Mesures
            WHERE code_departement = ? AND strftime('%Y', date_mesure) = '2018'
            ORDER BY date_mesure
        """
        try:
            cursor = db.data.cursor()
            result4 = cursor.execute(query4, [Dep_Max]).fetchall()
            cursor.close()
        except Exception as e:
            print(f"Erreur lors de la requête des températures chaudes : {repr(e)}")
            return

        # Préparation des données des départements les plus froids et chauds
        for row in result3:
            tabx.append(row[0])
            graph3.append(row[1])  # Température du département le plus froid

        for row in result4:
            graph4.append(row[1])  # Température du département le plus chaud

        # Formatage des dates pour l'affichage sur l'axe x
        datetime_dates = [datetime.strptime(date, '%Y-%m-%d') for date in tabx]
        # Création du graphique
        fig = Figure(figsize=(15, 8), dpi=100)
        plot1 = fig.add_subplot(111)

        # Affichage des courbes
        plot1.plot(range(len(datetime_dates)), graph1, color='#00FFFF', label='Records de fraîcheur historiques')
        plot1.plot(range(len(datetime_dates)), graph2, color='#FF8300', label='Records de chaleur historiques')
        plot1.plot(range(len(datetime_dates)), graph3, color='#0000FF', label='Département le plus froid (2018)')
        plot1.plot(range(len(datetime_dates)), graph4, color='#FF0000', label='Département le plus chaud (2018)')

        # Configuration de l'axe x pour n'afficher que le premier jour de chaque mois
        xticks = [i for i, date in enumerate(datetime_dates) if date.day == 1]
        xticklabels = [date.strftime('%Y-%m-%d') for date in datetime_dates if date.day == 1]
        plot1.set_xticks(xticks)
        plot1.set_xticklabels(xticklabels, rotation=45)
        plot1.legend()

        # Affichage du graphique
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()