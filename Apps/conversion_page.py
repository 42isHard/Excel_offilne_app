import os  # Ajoutez cette importation pour manipuler les chemins de fichiers
import customtkinter as ctk
from tkinter import filedialog
import pandas as pd


class ConversionPage:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self.parent, text="Sélectionnez le fichier de mapping").pack(pady=10)
        ctk.CTkButton(self.parent, text="Choisir le fichier de mapping", command=self.select_mapping_file).pack(pady=10)
        ctk.CTkLabel(self.parent, text="Sélectionnez les fichiers cibles pour la conversion").pack(pady=10)
        ctk.CTkButton(self.parent, text="Sélectionner les fichiers", command=self.select_target_files).pack(pady=10)
        ctk.CTkButton(self.parent, text="Appliquer la conversion", command=self.apply_conversion).pack(pady=10)
        ctk.CTkButton(self.parent, text="Retourner au menu principal", command=self.main_app.create_main_menu).pack(
            pady=10)

    def select_mapping_file(self):
        self.mapping_file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")],
                                                            title="Choisir le fichier de mapping")

    def select_target_files(self):
        self.target_file_paths = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx")],
                                                             title="Sélectionner les fichiers cibles")

    def apply_conversion(self):
        mapping_df = pd.read_excel(self.mapping_file_path)
        code_map = dict(zip(mapping_df['FFI_CODE'].astype(str), mapping_df['CODE_FR'].astype(str)))
        for file_path in self.target_file_paths:
            df = pd.read_excel(file_path, header=5)
            if 'Compte Général - Code' in df.columns:
                df['Compte Général - Code'] = df['Compte Général - Code'].astype(str).map(code_map).fillna(
                    df['Compte Général - Code'])
                # Créer un nouveau chemin pour le fichier converti
                base, ext = os.path.splitext(file_path)
                new_file_path = f"{base}_CODE_FR{ext}"
                df.to_excel(new_file_path, index=False)
                print(f"Le fichier converti a été enregistré sous : {new_file_path}")
            else:
                print(f"La colonne 'Compte Général - Code' n'a pas été trouvée dans {file_path}")
