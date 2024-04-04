import customtkinter as ctk
from tkinter import filedialog, messagebox
import logging
import pandas as pd
from tqdm import tqdm
from Apps.conversion_rate_popup import ConversionRatePopup


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

    def create_widgets(self):
        """
        Crée les widgets pour l'interface utilisateur de la vue des opérations.
        """
        ctk.CTkButton(self.parent, text="Concaténer les fichiers sélectionnés", command=self.execute_operations).pack(
            pady=10)
        ctk.CTkButton(self.parent, text="Retour", command=self.main_app.create_main_menu).pack(pady=10)

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
        all_dfs = []
        for fp in tqdm(filepaths, total=len(filepaths), unit="file"):
            logging.info(f"Traitement du fichier : {fp}")
            try:
                df = self.read_excel_file(fp)
                df.drop(df.columns[0], axis=1, inplace=True)
                if self.should_convert(fp):
                    conversion_rate = self.get_conversion_rate()
                    df = self.convert_column(df, 'Solde Tenue de Compte', conversion_rate)
                all_dfs.append(df)
            except Exception as e:
                logging.error("Erreur lors de la lecture du fichier " + fp + ": " + str(e))
        return pd.concat(all_dfs, ignore_index=True)

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
