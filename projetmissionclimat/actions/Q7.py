import tkinter as tk
from tkinter import ttk
from utils import display
from tkinter import messagebox
import sqlite3

data = sqlite3.connect("data/climat_france.db")
data.execute("PRAGMA foreign_keys = 1")


class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille et du titre de la fenêtre
        display.centerWindow(300, 200, self)
        self.title('Q7 : fonctions pour gerer les travaux')
        # Contrôles de la BDD
        ttk.Label(
            self,
            text="fonctions pour gerer les travaux",
            font=("Helvetica", 12, "bold"),
            anchor="center"
        ).grid(row=0, column=0, pady=(10, 15), sticky="nsew")

        # Boutons pour insérer, modifier et supprimer
        ttk.Button(self, text="Insérer des travaux", command=self.add_travaux).grid(
            row=1, column=0, pady=5
        )
        ttk.Button(self, text="Modifier des travaux", command=self.update_travaux).grid(
            row=2, column=0, pady=5
        )
        ttk.Button(self, text="Supprimer des travaux", command=self.delete_travaux).grid(
            row=3, column=0, pady=5
        )

        # Mettre les boutons au milieu de l'interface
        self.columnconfigure(0, weight=1)

    def add_travaux(self):
        add_travauxfonction(self)

    def update_travaux(self):
        update_travauxfonction(self)

    def delete_travaux(self):
        delete_travauxfonction(self)


class add_travauxfonction(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        # Définition de la taille de la fenêtre
        display.centerWindow(600, 500, self)
        self.title('Ajout de type de travaux')
        self.id_travaux = None  # Stocker l'id du travail ajouté

        # Champs du formulaire
        ttk.Label(self, text="Coût total HT").grid(row=0, column=0, pady=5)
        self.cout_total_HT = ttk.Entry(self)
        self.cout_total_HT.grid(row=0, column=1, pady=5)

        ttk.Label(self, text="Coût induit HT").grid(row=1, column=0, pady=5)
        self.cout_induit_HT = ttk.Entry(self)
        self.cout_induit_HT.grid(row=1, column=1, pady=5)

        ttk.Label(self, text="Année").grid(row=2, column=0, pady=5)
        self.annee = ttk.Entry(self)
        self.annee.grid(row=2, column=1, pady=5)

        ttk.Label(self, text="Type de logement").grid(row=3, column=0, pady=5)
        self.type_logement = ttk.Entry(self)
        self.type_logement.grid(row=3, column=1, pady=5)

        ttk.Label(self, text="Année de construction du logement").grid(row=4, column=0, pady=5)
        self.annee_construction = ttk.Entry(self)
        self.annee_construction.grid(row=4, column=1, pady=5)

        ttk.Label(self, text="Code région").grid(row=5, column=0, pady=5)
        self.code_region = ttk.Entry(self)
        self.code_region.grid(row=5, column=1, pady=5)

        ttk.Label(self, text="Code département").grid(row=6, column=0, pady=5)
        self.code_departement = ttk.Entry(self)
        self.code_departement.grid(row=6, column=1, pady=5)

        # Bouton "Ajouter"
        ttk.Button(self, text="Ajouter", command=self.enregistrer).grid(row=9, columnspan=2, pady=10)

    def enregistrer(self):
        cout_total = self.cout_total_HT.get()
        cout_induit = self.cout_induit_HT.get()
        annee = self.annee.get()
        type_logement = self.type_logement.get()
        annee_construction = self.annee_construction.get()
        code_region = self.code_region.get()
        code_departement = self.code_departement.get()

        cursor = data.cursor()
        try:
            # Insertion dans Travaux
            cursor.execute("""
                INSERT INTO Travaux (cout_total_ht_travaux, cout_induit_ht_travaux, annee_travaux, 
                                     type_logement_travaux, annee_construction_logement_travaux, code_region_travaux, code_departement_travaux)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                           (cout_total, cout_induit, annee, type_logement, annee_construction, code_region,
                            code_departement))

            # Récupération de l'id généré
            self.id_travaux = cursor.lastrowid

            # Confirmation d'enregistrement et demande de choix du type de travaux
            messagebox.showinfo("Succès", "Informations de base enregistrées. Veuillez choisir le type de travaux.")

            # Ouvrir la fenêtre pour sélectionner le type de travaux
            self.choisir_type_travaux()

        except Exception as e:
            data.rollback()
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
        else:
            data.commit()

    def choisir_type_travaux(self):
        # Sélection du type de travaux après insertion
        self.type_travaux_window = tk.Toplevel(self)
        self.type_travaux_window.title("Sélectionner le type de travaux")
        display.centerWindow(300, 150, self.type_travaux_window)

        ttk.Label(self.type_travaux_window, text="Choisir le type de travaux").pack(pady=10)
        self.type_travaux = ttk.Combobox(self.type_travaux_window, values=["Isolation", "Chauffage", "Photovoltaïque"],
                                         state="readonly")
        self.type_travaux.pack(pady=10)

        ttk.Button(self.type_travaux_window, text="Continuer", command=self.gerer_type_travaux).pack(pady=10)

    def gerer_type_travaux(self):
        type_travaux = self.type_travaux.get()

        if not type_travaux:
            messagebox.showerror("Erreur", "Veuillez sélectionner un type de travaux.")
            return

        # Fermer la fenêtre de sélection
        self.type_travaux_window.destroy()

        # Ouvrir la fenêtre correspondante en fonction du type de travaux
        if type_travaux == "Isolation":
            Isolation(self, self.id_travaux)
        elif type_travaux == "Chauffage":
            Chauffage(self, self.id_travaux)
        elif type_travaux == "Photovoltaïque":
            Photovoltaique(self, self.id_travaux)


class Isolation(tk.Toplevel):
    def __init__(self, parent, id_travaux):
        super().__init__(parent)
        self.id_travaux = id_travaux  # Récupérer l'id du travail
        display.centerWindow(300, 200, self)
        self.title("Détails de l'Isolation")

        ttk.Label(self, text="Poste d'isolation").grid(row=0, column=0, pady=5, sticky="w")
        self.poste_isolation = ttk.Combobox(self, values=["COMBLES PERDUES", "ITI", "ITE", "RAMPANTS", "SARKING",
                                                          "TOITURE TERASSE", "PLANCHER BAS"], state="readonly")
        self.poste_isolation.grid(row=0, column=1, pady=5)

        ttk.Label(self, text="Isolant").grid(row=1, column=0, pady=5, sticky="w")
        self.isolant_isolation = ttk.Combobox(self, values=["AUTRES", "LAINE VEGETALE", "LAINE MINERALE", "PLASTIQUES"],
                                              state="readonly")
        self.isolant_isolation.grid(row=1, column=1, pady=5)

        ttk.Label(self, text="Épaisseur").grid(row=2, column=0, pady=5, sticky="w")
        self.epaisseur_isolation = ttk.Entry(self)
        self.epaisseur_isolation.grid(row=2, column=1, pady=5)

        ttk.Label(self, text="Surface").grid(row=3, column=0, pady=5, sticky="w")
        self.surface_isolation = ttk.Entry(self)
        self.surface_isolation.grid(row=3, column=1, pady=5)

        ttk.Button(self, text="Enregistrer", command=self.save_isolation).grid(row=4, columnspan=2, pady=10)

    def save_isolation(self):
        poste = self.poste_isolation.get()
        isolant = self.isolant_isolation.get()
        epaisseur = self.epaisseur_isolation.get()
        surface = self.surface_isolation.get()

        cursor = data.cursor()
        cursor.execute("""
            INSERT INTO Izolations (id_travaux, poste_izolation, isolant_izolation, epaisseur_izolation, surface_izolation)
            VALUES (?, ?, ?, ?, ?)""",
                       (self.id_travaux, poste, isolant, epaisseur, surface))
        data.commit()
        messagebox.showinfo("Parfait", "Travaux ajouté")
        self.destroy()


class Chauffage(tk.Toplevel):
    def __init__(self, parent, id_travaux):
        super().__init__(parent)
        self.id_travaux = id_travaux  # Récupérer l'id du travail
        display.centerWindow(300, 200, self)

        ttk.Label(self, text="Énergie avant travaux").grid(row=0, column=0, pady=5, sticky="w")
        self.energie_avant = ttk.Combobox(self, values=[
            "AUTRES", "BOIS", "ELECTRICITE", "FIOUL", "GAZ"
        ], state="readonly")
        self.energie_avant.grid(row=0, column=1, pady=5)

        ttk.Label(self, text="Énergie après travaux").grid(row=1, column=0, pady=5, sticky="w")
        self.energie_apres = ttk.Combobox(self, values=[
            "AUTRES", "BOIS", "ELECTRICITE", "FIOUL", "GAZ"
        ], state="readonly")
        self.energie_apres.grid(row=1, column=1, pady=5)

        ttk.Button(self, text="Enregistrer", command=self.save_chauffage).grid(row=4, columnspan=2, pady=10)

    def save_chauffage(self):
        energie_avant = self.energie_avant.get()
        energie_apres = self.energie_apres.get()

        cursor = data.cursor()
        cursor.execute("""
            INSERT INTO Chauffages (id_travaux, energie_avant_travaux_chauffage, energie_installee_chauffage)
            VALUES (?, ?, ?)""", (self.id_travaux, energie_avant, energie_apres))
        data.commit()
        messagebox.showinfo("Parfait", "Chauffage ajouté")
        self.destroy()


class Photovoltaique(tk.Toplevel):
    def __init__(self, parent, id_travaux):
        super().__init__(parent)
        self.id_travaux = id_travaux  # Récupérer l'id du travail
        display.centerWindow(300, 200, self)

        ttk.Label(self, text="Surface").grid(row=0, column=0, pady=5, sticky="w")
        self.surface_photovoltaique = ttk.Entry(self)
        self.surface_photovoltaique.grid(row=0, column=1, pady=5)

        ttk.Label(self, text="Puissance").grid(row=1, column=0, pady=5, sticky="w")
        self.puissance_photovoltaique = ttk.Entry(self)
        self.puissance_photovoltaique.grid(row=1, column=1, pady=5)

        ttk.Button(self, text="Enregistrer", command=self.save_photovoltaique).grid(row=4, columnspan=2, pady=10)

    def save_photovoltaique(self):
        surface = self.surface_photovoltaique.get()
        puissance = self.puissance_photovoltaique.get()

        cursor = data.cursor()
        cursor.execute("""
            INSERT INTO Photovoltaiques (id_travaux, puissance_installee_photovoltaique, type_panneaux_photovoltaique)
            VALUES (?, ?, ?)""", (self.id_travaux, surface, puissance))
        data.commit()
        messagebox.showinfo("Parfait", "Travaux ajouté")
        self.destroy()
class delete_travauxfonction(tk.Toplevel):
        def __init__(self, parent):
            super().__init__(parent)
            display.centerWindow(300, 250, self)
            self.title("Suppression d'un type de travaux")

            ttk.Label(self, text="ID du travaux à supprimer :").grid(row=0, column=0, pady=5, sticky="w")
            self.id_travaux = ttk.Entry(self)
            self.id_travaux.grid(row=1, column=1, pady=5)

            ttk.Button(self, text="Confirmer la suppression", command=self.supprimer_travaux).grid(row=2, columnspan=2,
                                                                                                   pady=10)
            self.columnconfigure(0, weight=1)

        def supprimer_travaux(self):
            id_travaux = self.id_travaux.get().strip()  # Enlever les espaces blancs

            if not id_travaux:
                messagebox.showerror("Erreur", "Veuillez entrer un ID valide.")
                return

            cursor = data.cursor()

            try:
                # Suppression du travail et de ses entrées associées
                cursor.execute("DELETE FROM Travaux WHERE id_travaux = ?", (id_travaux,))
                data.commit()
                messagebox.showinfo("Succès", "Le travaux a été supprimé avec succès.")
                self.destroy()  # Fermer la fenêtre après la suppression
            except sqlite3.IntegrityError as e:
                messagebox.showerror("Erreur d'intégrité", f"Impossible de supprimer l'entrée : {e}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")