import customtkinter as ctk
from Apps.file_selection_page import FileSelectionPage


class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mon Application")
        self.geometry("600x450")

        ctk.set_appearance_mode("System")  # "System", "Dark", ou "Light"
        ctk.set_default_color_theme("blue")

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)  # Ajout de padding ici
        self.selected_filepaths = []
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="Sélectionnez une fonctionnalité").pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Fonctionnalité de sélection de fichiers",
                      command=self.open_file_selection).pack(pady=10)

    def open_file_selection(self):
        self.clear_frame()
        FileSelectionPage(self.main_frame, self)

    def set_filepaths(self, filepaths):
        self.selected_filepaths = filepaths

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.pack_forget()
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
