import customtkinter as ctk
from tkinter import filedialog, messagebox
from operations_view import OperationsView

class FileSelectionPage:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.file_labels = []  # Pour stocker les labels des fichiers
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self.parent, text="Sélectionnez les fichiers à concaténer").pack(pady=10)
        ctk.CTkButton(self.parent, text="Sélectionner les fichiers", command=self.open_file_dialog).pack(pady=10)
        self.files_frame = ctk.CTkFrame(self.parent)
        self.files_frame.pack(pady=10, fill="both", expand=True)
        ctk.CTkButton(self.parent, text="Suivant", command=self.save_filepaths_and_continue).pack(pady=10)
        self.add_back_button()

    def open_file_dialog(self):
        filepaths = filedialog.askopenfilenames()
        self.update_file_labels(filepaths)

    def update_file_labels(self, filepaths):
        # Supprimer les labels des fichiers existants
        for label in self.file_labels:
            label.destroy()
        self.file_labels.clear()

        # Créer un nouveau label pour chaque fichier sélectionné
        for filepath in filepaths:
            label = ctk.CTkLabel(self.files_frame, text=filepath)
            label.pack(pady=2, padx=10, fill='x')
            self.file_labels.append(label)

    def save_filepaths_and_continue(self):
        filepaths = [label.cget("text") for label in self.file_labels]
        if self.validate_selected_files(filepaths):
            self.main_app.set_filepaths(filepaths)
            self.main_app.clear_frame()
            OperationsView(self.main_app, self.main_app.main_frame)

    def validate_selected_files(self, filepaths):
        for filepath in filepaths:
            if not filepath.endswith('.xlsx'):
                messagebox.showerror("Erreur", "Veuillez sélectionner uniquement des fichiers Excel (.xlsx).")
                return False
        return True

    def add_back_button(self):
        ctk.CTkButton(self.parent, text="Retour", command=self.main_app.create_main_menu).pack(pady=10)
