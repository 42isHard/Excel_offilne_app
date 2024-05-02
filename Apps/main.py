import customtkinter as ctk
from Apps.file_selection_page import FileSelectionPage
from Apps.conversion_page import ConversionPage


class MainApplication(ctk.CTk):
    """
    Classe principale de l'application Automatisation First Finance.

    Cette application fournit une interface graphique pour concaténer plusieurs fichiers Excel (xlsx) et pour convertir les codes comptables.
    Elle utilise CustomTkinter pour un style d'interface utilisateur moderne et personnalisable.
    """

    def __init__(self):
        """
        Initialisation de l'application.
        """
        super().__init__()
        self.title("Automatisation First Finance")
        self.geometry("600x450")

        ctk.set_appearance_mode("Dark")  # Choix du mode d'apparence : "System", "Dark", ou "Light"
        ctk.set_default_color_theme("blue")  # Thème de couleur par défaut

        self.main_frame = ctk.CTkFrame(self)  # Création du cadre principal
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        self.selected_filepaths = []  # Liste pour stocker les chemins des fichiers sélectionnés

        self.create_main_menu()

    def create_main_menu(self):
        """
        Crée le menu principal de l'application.
        """
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="Veuillez sélectionner une fonctionnalité").pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Concaténer plusieurs fichiers xlsx",
                      command=self.open_file_selection).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Conversion codes comptables",
                      command=self.open_conversion_feature).pack(pady=10)  # Nouveau bouton pour la conversion

    def open_file_selection(self):
        """
        Ouvre la page de sélection de fichiers.
        """
        self.clear_frame()
        FileSelectionPage(self.main_frame, self)

    def open_conversion_feature(self):
        """
        Ouvre la fonctionnalité de conversion des codes comptables.
        """
        self.clear_frame()
        ConversionPage(self.main_frame, self)  # Assurez-vous que la classe ConversionPage est correctement définie

    def set_filepaths(self, filepaths):
        """
        Définit les chemins de fichiers sélectionnés.
        """
        self.selected_filepaths = filepaths

    def clear_frame(self):
        """
        Efface tous les widgets du cadre principal.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.pack_forget()
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
