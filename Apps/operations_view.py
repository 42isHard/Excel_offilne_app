import customtkinter as ctk
from tkinter import filedialog, messagebox
import logging
import pandas as pd
from tqdm import tqdm
from Apps.conversion_rate_popup import ConversionRatePopup
import os


class OperationsView:
    """
    Vue pour les opérations sur les fichiers dans l'application.

    Cette vue permet à l'utilisateur de concaténer des fichiers Excel et de sauvegarder le résultat.
    """

    def __init__(self, main_app, parent):
        """
        Initialise la vue des opérations.

        Args:
            main_app: Instance de l'application principale.
            parent: Widget parent pour cette vue.
        """
        self.main_app = main_app
        self.parent = parent
        self.create_widgets()

    def select_rules_file(self):
        """ Permet à l'utilisateur de sélectionner un fichier de règles Excel. """
        file_types = [('Excel files', '*.xlsx')]
        self.rules_file = filedialog.askopenfilename(filetypes=file_types, title="Sélectionnez le fichier de règles")
        if self.rules_file:
            messagebox.showinfo("Fichier de règles sélectionné",
                                f"Le fichier de règles sélectionné est :\n{self.rules_file}")
        else:
            messagebox.showwarning("Aucun fichier sélectionné", "Veuillez sélectionner un fichier de règles.")

    def create_widgets(self):
        """
        Crée les widgets pour l'interface utilisateur de la vue des opérations.
        """
        ctk.CTkButton(self.parent, text="Choisir le fichier de règles", command=self.select_rules_file).pack(pady=10)
        ctk.CTkButton(self.parent, text="Concaténer les fichiers sélectionnés", command=self.execute_operations).pack(
            pady=10)
        ctk.CTkButton(self.parent, text="Retourner à l'accueil", command=self.main_app.create_main_menu).pack(pady=10)

    def execute_operations(self):
        """
        Exécute le processus de concaténation des fichiers sélectionnés.
        """
        combined_df = None
        try:
            logging.info("Début de la combinaison des fichiers.")
            combined_df = self.combine_files(self.main_app.selected_filepaths)
            messagebox.showinfo("Succès",
                                "Les fichiers ont été combinés. Veuillez sélectionner un emplacement pour sauvegarder le fichier.")
        except Exception as e:
            logging.exception("Erreur lors de la combinaison des fichiers.")
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la combinaison des fichiers.")

        if combined_df is not None:
            self.save_combined_file(combined_df)

    def match_rule(self, row, rules_df):
        pcg = str(row['Compte Général - Code'])
        code_analytique = str(row['Section Analytique - Code'])

        for _, rule in rules_df.iterrows():
            pcg_rule = str(rule['PCG'])
            codes_analytiques_rule = str(rule['Codes analytiques']).split('/')
            #print(rule, rules_df)

            # Vérifier si PCG correspond et si Code Analytique correspond ou commence par les codes spécifiés
            if pcg == pcg_rule and any(
                    code_analytique == code or code_analytique.startswith(code) for code in codes_analytiques_rule):
                #print(pcg, pcg_rule, code_analytique, codes_analytiques_rule)
                return {
                    'Libellés analytiques 2024': rule['Libellés analytiques 2024'],
                    'Regroupements analytiques': rule['Regroupements analytiques']
                }
        return None

    def save_combined_file(self, dataframe):
        """
        Invite l'utilisateur à sauvegarder le fichier Excel combiné.

        Args:
            dataframe: DataFrame contenant les données combinées des fichiers.
        """
        file_types = [('Excel files', '*.xlsx')]
        output_file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=file_types)
        if output_file:
            try:
                dataframe.to_excel(output_file, index=False)
                messagebox.showinfo("Succès", "Fichier enregistré avec succès à: " + output_file)
            except Exception as e:
                logging.exception("Erreur lors de l'enregistrement du fichier.")
                messagebox.showerror("Erreur", "Une erreur est survenue lors de l'enregistrement du fichier: " + str(e))

    def combine_files(self, filepaths):
        """
        Combine plusieurs fichiers Excel en un seul DataFrame.

        Args:
            filepaths: Liste des chemins des fichiers à combiner.

        Returns:
            Un DataFrame combiné contenant les données de tous les fichiers.
        """
        # Vérifier si le fichier de règles est sélectionné
        if not hasattr(self, 'rules_file') or not self.rules_file:
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier de règles.")
            return None

        # Charger le fichier de règles
        rules_df = pd.read_excel(self.rules_file)

        all_dfs = []
        for fp in tqdm(filepaths, total=len(filepaths), unit="file"):
            logging.info(f"Traitement du fichier : {fp}")
            try:
                df = self.read_excel_file(fp)
                file_prefix = self.extract_file_prefix(fp)
                df.iloc[:, 0] = file_prefix
                df.rename(columns={df.columns[0]: 'Origine'}, inplace=True)

                # Application des règles pour chaque ligne
                for index, row in df.iterrows():
                    matched_rule = self.match_rule(row, rules_df)
                    if matched_rule is not None:
                        df.at[index, 'Libellés analytiques 2024'] = matched_rule['Libellés analytiques 2024']
                        df.at[index, 'Regroupements analytiques'] = matched_rule['Regroupements analytiques']

                if self.should_convert(fp):
                    conversion_rate = self.get_conversion_rate()
                    df = self.convert_column(df, 'Solde Tenue de Compte', conversion_rate)

                all_dfs.append(df)
            except Exception as e:
                logging.error("Erreur lors de la lecture du fichier " + fp + ": " + str(e))

        return pd.concat(all_dfs, ignore_index=True)

    def extract_file_prefix(self, filepath):
        # Extraction du préfixe du nom de fichier (tout ce qui se trouve avant le premier "_")
        filename = os.path.basename(filepath)
        file_prefix = filename.split("_")[0]
        return file_prefix

    def read_excel_file(self, filepath):
        """
        Lit un fichier Excel spécifié.

        Args:
            filepath: Chemin du fichier Excel à lire.

        Returns:
            Un DataFrame avec les données du fichier.
        """
        return pd.read_excel(filepath, header=5)

    def should_convert(self, filepath):
        """
        Vérifie si le fichier Excel spécifié doit être converti en utilisant un taux de conversion.

        Args:
            filepath: Chemin du fichier à vérifier.

        Returns:
            True si le fichier nécessite une conversion, sinon False.
        """
        df = pd.read_excel(filepath, header=None, nrows=2)
        entity_value = df.iloc[0, 2]
        return pd.notna(entity_value) and str(entity_value).strip() == 'FIRST FINANCE INSTITUE'

    def get_conversion_rate(self):
        """
        Ouvre une popup pour que l'utilisateur puisse entrer le taux de conversion.

        Returns:
            Le taux de conversion entré par l'utilisateur.
        """
        conversion_popup = ConversionRatePopup(self.parent)
        self.parent.wait_window(conversion_popup)
        return conversion_popup.conversion_rate

    def convert_column(self, dataframe, column, rate):
        """
        Convertit une colonne spécifique d'un DataFrame en utilisant un taux de conversion donné.

        Args:
            dataframe: DataFrame contenant la colonne à convertir.
            column: Nom de la colonne à convertir.
            rate: Taux de conversion à appliquer.

        Returns:
            Le DataFrame avec la colonne convertie.
        """
        if rate is not None:
            dataframe[column] *= rate
        else:
            raise ValueError("Taux de conversion non fourni.")
        return dataframe
