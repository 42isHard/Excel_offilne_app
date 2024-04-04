import customtkinter as ctk
from tkinter import filedialog, messagebox
import logging
import pandas as pd
from tqdm import tqdm
from Apps.conversion_rate_popup import ConversionRatePopup
from tkinter import ttk, messagebox

class ProgressBarManager:
    def __init__(self, parent):
        self.progress_bar = self.create_progress_bar(parent)

    def create_progress_bar(self, parent):
        progress_bar = ttk.Progressbar(parent, orient='horizontal', mode='determinate')
        progress_bar.pack_forget()
        return progress_bar

    def start_progress(self, max_value):
        self.progress_bar['maximum'] = max_value
        self.progress_bar.pack()

    def update_progress(self, value):
        self.progress_bar["value"] = value

    def stop_progress(self):
        self.progress_bar.pack_forget()


class OperationsView:
    def __init__(self, main_app, parent):
        self.main_app = main_app
        self.parent = parent
        self.progress_manager = ProgressBarManager(parent)
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkButton(self.parent, text="Concaténer les fichiers sélectionnés", command=self.execute_operations).pack(pady=10)
        ctk.CTkButton(self.parent, text="Retour", command=self.main_app.create_main_menu).pack(pady=10)

    def create_label(self, text, **options):
        ttk.Label(self.parent, text=text, style='TLabel').pack(**options)

    def create_button(self, text, command, **options):
        ttk.Button(self.parent, text=text, command=command, style='TButton').pack(**options)

    def execute_operations(self):
        self.progress_manager.start_progress(len(self.main_app.selected_filepaths))
        combined_df = None
        try:
            logging.info("Début de la combinaison des fichiers.")
            combined_df = self.combine_files(self.main_app.selected_filepaths)
            messagebox.showinfo("Succès",
                                "Les fichiers ont été combinés. Veuillez sélectionner un emplacement pour sauvegarder le fichier.")
        except Exception as e:
            logging.exception("Erreur lors de la combinaison des fichiers.")
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la combinaison des fichiers.")
        finally:
            self.progress_manager.stop_progress()

        if combined_df is not None:
            self.save_combined_file(combined_df)

    def save_combined_file(self, dataframe):
        file_types = [('Excel files', '*.xlsx')]
        output_file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=file_types)
        if output_file:
            try:
                dataframe.to_excel(output_file, index=False)
                messagebox.showinfo("Succès", "Fichier enregistré avec succès à: " + output_file)
            except Exception as e:
                logging.exception("Erreur lors de l'enregistrement du fichier.")
                messagebox.showerror("Erreur", f"Une erreur est survenue lors de l'enregistrement du fichier: {e}")

    def combine_files(self, filepaths):
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
                self.progress_manager.update_progress(len(all_dfs))
            except Exception as e:
                logging.error(f"Erreur lors de la lecture du fichier {fp}: {e}")
        return pd.concat(all_dfs, ignore_index=True)

    def read_excel_file(self, filepath):
        df = pd.read_excel(filepath, header=5)
        return df

    def should_convert(self, filepath):
        df = pd.read_excel(filepath, header=None, nrows=2)
        entity_value = df.iloc[0, 2]
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