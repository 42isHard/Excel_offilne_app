import customtkinter as ctk
from tkinter import filedialog, messagebox
from operations_view import OperationsView


class FileSelectionPage:
    """
    Page de sélection de fichiers pour l'application Automatisation First Finance.

    Permet à l'utilisateur de sélectionner des fichiers Excel au format XLSX pour les traiter.
    """

    def __init__(self, parent, main_app):
        """
        Initialiser la page de sélection de fichiers.

        Args:
            parent: Widget parent dans lequel la page est incorporée.
            main_app: Référence à l'application principale pour l'accès aux fonctionnalités globales.
        """
        self.parent = parent
        self.main_app = main_app
        self.file_labels = []  # Pour stocker les labels des fichiers
        self.create_widgets()

    def create_widgets(self):
        """
        Créer les widgets pour la page de sélection de fichiers.
        """
        ctk.CTkLabel(self.parent, text="Veuillez sélectionner les fichiers à concaténer").pack(pady=10)
        ctk.CTkLabel(self.parent,
                     text="Les fichiers doivent être au format XLSX et la structure doit être celle par défaut sur SAGE").pack(
            pady=10)
        ctk.CTkButton(self.parent, text="Sélectionner les fichiers", command=self.open_file_dialog).pack(pady=10)
        self.files_frame = ctk.CTkFrame(self.parent)
        self.files_frame.pack(pady=10, fill="both", expand=True)
        ctk.CTkButton(self.parent, text="Suivant", command=self.save_filepaths_and_continue).pack(pady=10)
        self.add_back_button()

    def open_file_dialog(self):
        """
        Ouvrir un dialogue pour choisir les fichiers à concaténer.
        """
        filepaths = filedialog.askopenfilenames()
        self.update_file_labels(filepaths)

    def update_file_labels(self, filepaths):
        """
        Mettre à jour l'affichage des fichiers sélectionnés.

        Args:
            filepaths: Liste des chemins des fichiers sélectionnés.
        """
        for label in self.file_labels:
            label.destroy()
        self.file_labels.clear()

        for filepath in filepaths:
            label = ctk.CTkLabel(self.files_frame, text=filepath)
            label.pack(pady=2, padx=10, fill='x')
            self.file_labels.append(label)

    def save_filepaths_and_continue(self):
        """
        Sauvegarder les chemins de fichiers sélectionnés et continuer vers la prochaine étape.
        """
        filepaths = [label.cget("text") for label in self.file_labels]
        if self.validate_selected_files(filepaths):
            self.main_app.set_filepaths(filepaths)
            self.main_app.clear_frame()
            OperationsView(self.main_app, self.main_app.main_frame)

    def validate_selected_files(self, filepaths):
        """
        Valider les fichiers sélectionnés pour s'assurer qu'ils sont au format XLSX.

        Args:
            filepaths: Liste des chemins des fichiers sélectionnés.

        Returns:
            bool: True si tous les fichiers sont au format XLSX, False sinon.
        """
        for filepath in filepaths:
            if not filepath.endswith('.xlsx'):
                messagebox.showerror("Erreur", "Veuillez sélectionner uniquement des fichiers Excel (.xlsx).")
                return False
        return True

    def add_back_button(self):
        """
        Ajouter un bouton de retour pour revenir au menu principal.
        """
        ctk.CTkButton(self.parent, text="Retourner à l'accueil", command=self.main_app.create_main_menu).pack(pady=10)
