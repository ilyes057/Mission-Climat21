import tkinter as tk
from tkinter import ttk
from utils import display

class Window(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(800, 500, self)
        self.title('Consultation des données de la base')
        display.defineGridDisplay(self, 1, 1)

        # Définition des onglets
        tabControl = ttk.Notebook(self)

        # Onglets existants
        tabs = {
            "Mesures (1000 1ères valeurs)": {
                "columns": ('code_departement', 'date_mesure', 'temperature_min_mesure', 'temperature_max_mesure', 'temperature_moy_mesure'),
                "query": """
                    SELECT code_departement, date_mesure, temperature_min_mesure, temperature_max_mesure, temperature_moy_mesure
                    FROM Mesures
                    ORDER BY date_mesure
                    LIMIT 1, 1000
                """
            },
            "Départements": {
                "columns": ('code_departement', 'nom_departement', 'code_region', 'zone_climatique'),
                "query": """
                    SELECT code_departement, nom_departement, code_region, zone_climatique
                    FROM Departements
                    ORDER BY code_departement
                """
            },
            "Régions": {
                "columns": ('code_region', 'nom_region'),
                "query": """
                    SELECT code_region, nom_region
                    FROM Regions
                    ORDER BY code_region
                """
            },
            # Nouvelles tables ajoutées
            "Communes": {
                "columns": ('code_communes', 'code_departement', 'nom_communes', 'statut_communes', 'altitude_communes', 'population_communes', 'superficie_communes'),
                "query": """
                    SELECT code_communes, code_departement, nom_communes, statut_communes, altitude_communes, population_communes, superficie_communes
                    FROM Communes
                    ORDER BY code_communes
                """
            },
            "Travaux": {
                "columns": ('id_travaux', 'code_departement_travaux', 'code_region_travaux', 'cout_total_ht_travaux', 'cout_induit_ht_travaux', 'annee_travaux', 'type_logement_travaux', 'annee_construction_logement_travaux'),
                "query": """
                    SELECT id_travaux, code_departement_travaux, code_region_travaux, cout_total_ht_travaux, cout_induit_ht_travaux, annee_travaux, type_logement_travaux, annee_construction_logement_travaux
                    FROM Travaux
                    ORDER BY id_travaux
                """
            },
            "Izolations": {
                "columns": ('id_travaux', 'poste_izolation', 'isolant_izolation', 'epaisseur_izolation', 'surface_izolation'),
                "query": """
                    SELECT id_travaux, poste_izolation, isolant_izolation, epaisseur_izolation, surface_izolation
                    FROM Izolations
                    ORDER BY id_travaux
                """
            },
            "Chauffages": {
                "columns": ('id_travaux', 'energie_avant_travaux_chauffage', 'energie_installee_chauffage', 'generateur_chauffage', 'type_chaudiere_chauffage'),
                "query": """
                    SELECT id_travaux, energie_avant_travaux_chauffage, energie_installee_chauffage, generateur_chauffage, type_chaudiere_chauffage
                    FROM Chauffages
                    ORDER BY id_travaux
                """
            },
            "Photovoltaiques": {
                "columns": ('id_travaux', 'puissance_installee_photovoltaique', 'type_panneaux_photovoltaique'),
                "query": """
                    SELECT id_travaux, puissance_installee_photovoltaique, type_panneaux_photovoltaique
                    FROM Photovoltaiques
                    ORDER BY id_travaux
                """
            }
        }

        # Création des onglets et ajout des TreeView
        for tab_name, data in tabs.items():
            tab = ttk.Frame(tabControl)
            tabControl.add(tab, text=tab_name)
            display.defineGridDisplay(tab, 1, 2)

            # Création du TreeView
            tree = display.createTreeViewDisplayQuery(tab, data["columns"], data["query"])
            scrollbar = ttk.Scrollbar(tab, orient='vertical', command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            tree.grid(row=0, sticky="nswe")
            scrollbar.grid(row=0, column=1, sticky="ns")

        tabControl.grid(row=0, column=0, sticky="nswe")
