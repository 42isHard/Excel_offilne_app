import tkinter as tk
from tkinter import ttk, messagebox


class ConversionRatePopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Taux de conversion")
        self.geometry("300x100")
        self.conversion_rate = None
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Entrez le taux de conversion HKD/EUR:").pack(pady=5)
        self.conversion_rate_entry = tk.Entry(self)
        self.conversion_rate_entry.pack(pady=5)
        tk.Button(self, text="Confirmer", command=self.confirm).pack(pady=5)

    def confirm(self):
        try:
            self.conversion_rate = float(self.conversion_rate_entry.get())
            self.destroy()
        except ValueError:
            tk.messagebox.showerror("Erreur", "Veuillez entrer un nombre valide.")
