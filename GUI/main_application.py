import tkinter as tk
from tkinter import ttk
from GUI.file_selection_page import FileSelectionPage


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mon Application")
        self.geometry("600x450")
        self.setup_styles()
        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack(expand=True, fill='both')
        self.selected_filepaths = []
        self.create_main_menu()

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', background='#4a7a8c', foreground='white', font=('Arial', 10, 'bold'), borderwidth=1)
        style.map('TButton', background=[('active', '#3b6978')])
        style.configure('TLabel', background='#dae1e7', font=('Arial', 12, 'bold'))
        style.configure('TFrame', background='#dae1e7')

    def create_main_menu(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text="Sélectionnez une fonctionnalité", style='TLabel').pack(pady=10)
        ttk.Button(self.main_frame, text="Fonctionnalité de sélection de fichiers",
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
        self.main_frame.pack(expand=True, fill='both')


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
