import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from operations_view import OperationsView


class FileSelectionPage:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.parent, text="Sélectionnez les fichiers à concaténer", style='TLabel').pack(pady=10)
        ttk.Button(self.parent, text="Sélectionner les fichiers", command=self.open_file_dialog, style='TButton').pack(
            pady=10)
        self.files_list = tk.Listbox(self.parent, height=10, width=50, border=0)
        self.files_list.pack(pady=10)
        ttk.Button(self.parent, text="Suivant", command=self.save_filepaths_and_continue, style='TButton').pack(pady=10)
        self.add_back_button()

    def open_file_dialog(self):
        filepaths = filedialog.askopenfilenames()
        self.files_list.delete(0, tk.END)
        for filepath in filepaths:
            self.files_list.insert(tk.END, filepath)

    def validate_selected_files(self, filepaths):
        for filepath in filepaths:
            if not filepath.endswith('.xlsx'):
                messagebox.showerror("Erreur", "Veuillez sélectionner uniquement des fichiers Excel (.xlsx).")
                return False
            # Ajoutez d'autres vérifications si nécessaire
        return True

    def save_filepaths_and_continue(self):
        filepaths = [self.files_list.get(idx) for idx in range(self.files_list.size())]
        if self.validate_selected_files(filepaths):
            self.main_app.set_filepaths(filepaths)
            self.main_app.clear_frame()
            OperationsView(self.main_app, self.main_app.main_frame)

    def add_back_button(self):
        ttk.Button(self.parent, text="Retour", command=self.main_app.create_main_menu, style='TButton').pack(pady=10)
