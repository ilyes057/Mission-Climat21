import tkinter as tk
from tkinter import ttk
from utils import display
from utils import db


class Window(tk.Toplevel):
    treeView = None
    region_selector = None
    errorLabel = None

    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre et des lignes/colonnes
        display.centerWindow(600, 450, self)
        self.title('Q3 : nombre de mesures prises et moyenne des températures (version dynamique)')
        display.defineGridDisplay(self, 3, 3)
        self.grid_rowconfigure(3, weight=10)  # Poids plus important pour la dernière ligne

        ttk.Label(self,
                  text="On a modifié l'interface pour permettre un choix de la région via un menu déroulant, "
                       "et la requête pour afficher le nombre de mesures prises et la moyenne des températures moyennes "
                       "par département pour la région choisie.",
                  wraplength=500,
                  anchor="center",
                  font=('Helvetica', '10', 'bold')
                  ).grid(sticky="we", row=0, columnspan=3)

        # Récupération des régions depuis la base
        try:
            cursor = db.data.cursor()
            regions = cursor.execute("SELECT nom_region FROM Regions").fetchall()
            self.regions_list = [r[0] for r in regions]
        except Exception as e:
            self.regions_list = []
            print(f"Erreur lors de la récupération des régions : {repr(e)}")

        # Affichage du menu déroulant pour sélectionner une région
        ttk.Label(self,
                  text='Veuillez choisir une région :',
                  anchor="center",
                  font=('Helvetica', '10', 'bold')
                  ).grid(row=1, column=0)

        self.region_selector = ttk.Combobox(self, values=self.regions_list, state="readonly")
        self.region_selector.grid(row=1, column=1)
        self.region_selector.bind("<<ComboboxSelected>>", self.searchRegion)

        ttk.Button(self,
                   text='Valider',
                   command=self.searchRegion
                   ).grid(row=1, column=2)

        # Label pour afficher les erreurs
        self.errorLabel = ttk.Label(self, anchor="center", font=('Helvetica', '10', 'bold'))
        self.errorLabel.grid(columnspan=3, row=2, sticky="we")

        # Préparation du TreeView pour afficher les résultats
        columns = ('code_departement', 'nom_departement', 'num_mesures', 'moy_temp_moyenne')
        self.treeView = ttk.Treeview(self, columns=columns, show='headings')
        for column in columns:
            self.treeView.column(column, anchor=tk.CENTER, width=15)
            self.treeView.heading(column, text=column)
        self.treeView.grid(columnspan=3, row=3, sticky='nswe')

    def searchRegion(self, event=None):
        # On vide le TreeView
        self.treeView.delete(*self.treeView.get_children())

        # On récupère la région sélectionnée
        region = self.region_selector.get()

        # Si aucune région n'est sélectionnée, on affiche une erreur
        if not region:
            self.errorLabel.config(foreground='red', text="Veuillez choisir une région !")
            return

        # Exécution de la requête
        try:
            cursor = db.data.cursor()
            result = cursor.execute("""
                SELECT D.code_departement, D.nom_departement, COUNT(M.date_mesure) AS num_mesures, 
                       AVG(M.temperature_moy_mesure) AS moy_temp_moy
                FROM Departements D
                JOIN Regions R ON D.code_region = R.code_region
                JOIN Mesures M ON D.code_departement = M.code_departement
                WHERE R.nom_region = ?
                GROUP BY D.code_departement, D.nom_departement
                ORDER BY D.code_departement
            """, [region])
        except Exception as e:
            self.errorLabel.config(foreground='red', text="Erreur : " + repr(e))
        else:
            i = 0
            for row in result:
                self.treeView.insert('', tk.END, values=row)
                i += 1

            if i == 0:
                self.errorLabel.config(foreground='orange', text=f"Aucun résultat pour la région \"{region}\" !")
            else:
                self.errorLabel.config(foreground='green', text=f"Voici les résultats pour la région \"{region}\" :")
