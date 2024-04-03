import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import logging
import pandas as pd
from tqdm import tqdm
import os
from Apps.conversion_rate_popup import ConversionRatePopup


class OperationsView:
    def __init__(self, main_app, parent):
        self.main_app = main_app
        self.parent = parent
        self.create_widgets()
        self.output_filename = ""  # Variable pour stocker le nom du fichier validé

    def create_widgets(self):
        ttk.Label(self.parent, text="Opérations sur les fichiers", style='TLabel').pack(pady=10)
        ttk.Label(self.parent, text="Répertoire de sortie :").pack(pady=5)
        self.output_directory_entry = tk.Entry(self.parent)
        self.output_directory_entry.pack(pady=5)
        ttk.Button(self.parent, text="Sélectionner le répertoire", command=self.browse_output_directory,
                   style='TButton').pack(pady=5)
        ttk.Label(self.parent, text="Nom du fichier de sortie :").pack(pady=5)
        self.output_filename_entry = tk.Entry(self.parent)
        self.output_filename_entry.pack(pady=5)
        ttk.Button(self.parent, text="Valider le nom du fichier", command=self.validate_output_filename,
                   style='TButton').pack(pady=5)
        ttk.Button(self.parent, text="Exécuter l'opération", command=self.execute_operations, style='TButton').pack(
            pady=10)
        self.progress_bar = ttk.Progressbar(self.parent, orient='horizontal', mode='determinate')
        self.add_back_button()

    def validate_output_filename(self):
        output_filename = self.output_filename_entry.get()
        if not output_filename:
            messagebox.showerror("Erreur", "Veuillez entrer un nom de fichier.")
        else:
            self.output_filename = output_filename  # Stockez le nom du fichier validé
            messagebox.showinfo("Validation", f"Le nom du fichier de sortie est : {output_filename}")

    def browse_output_directory(self):
        output_directory = filedialog.askdirectory()
        self.output_directory_entry.delete(0, tk.END)
        self.output_directory_entry.insert(0, output_directory)

    def execute_operations(self):
        self.start_progress(len(self.main_app.selected_filepaths))
        try:
            logging.info("Début de la combinaison des fichiers.")
            combined_df = self.combine_files(self.main_app.selected_filepaths)
            self.save_combined_file(combined_df)
            messagebox.showinfo("Succès", "Les fichiers ont été combinés avec succès.")
            logging.info("Les fichiers ont été combinés avec succès.")
        except Exception as e:
            logging.exception("Erreur lors de la combinaison des fichiers.")
            messagebox.showerror("Erreur",
                                 "Une erreur est survenue. Consultez le fichier de logs pour plus d'informations.")
        finally:
            self.stop_progress()

    def start_progress(self, max_value):
        self.progress_bar['maximum'] = max_value
        self.progress_bar.pack(pady=10)

    def stop_progress(self):
        self.progress_bar.pack_forget()

    def save_combined_file(self, dataframe):
        output_filename = self.output_filename_entry.get()
        output_directory = self.output_directory_entry.get()
        if not output_filename:
            output_filename = "combined_file"
        output_path = os.path.join(output_directory, output_filename + ".xlsx")
        dataframe.to_excel(output_path, index=False)

    def combine_files(self, filepaths):
        all_dfs = []
        for fp in tqdm(filepaths, total=len(filepaths), unit="file"):
            logging.info(f"Traitement du fichier : {fp}")
            try:
                df = self.read_excel_file(fp)
                if self.should_convert(fp):
                    conversion_rate = self.get_conversion_rate()
                    df = self.convert_column(df, 'Solde Tenue de Compte', conversion_rate)
                all_dfs.append(df)
                self.update_progress_bar(len(all_dfs))
            except Exception as e:
                logging.error(f"Erreur lors de la lecture du fichier {fp}: {e}")
                # Continue avec les autres fichiers
        return pd.concat(all_dfs, ignore_index=True)

    def read_excel_file(self, filepath):
        df = pd.read_excel(filepath, header=5)
        return df

    def should_convert(self, filepath):
        df = pd.read_excel(filepath, header=None, nrows=2)
        entity_value = df.iloc[0, 2]
        print(entity_value)
        if pd.notna(entity_value):
            return str(entity_value).strip() == 'FIRST FINANCE INSTITUE'
        else:
            return False

    def get_conversion_rate(self):
        conversion_popup = ConversionRatePopup(self.parent)
        self.parent.wait_window(conversion_popup)
        return conversion_popup.conversion_rate

    def convert_column(self, dataframe, column, rate):
        if rate is not None:
            dataframe[column] = dataframe[column] * rate
        else:
            raise ValueError("Taux de conversion non fourni.")
        return dataframe

    def update_progress_bar(self, value):
        self.progress_bar["value"] = value
        self.parent.update_idletasks()  # Force la mise à jour de l'UI

    def add_back_button(self):
        ttk.Button(self.parent, text="Retour", command=self.main_app.create_main_menu, style='TButton').pack(pady=10)
