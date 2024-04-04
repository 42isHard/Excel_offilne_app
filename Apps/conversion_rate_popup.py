import customtkinter as ctk
from tkinter import messagebox

class ConversionRatePopup(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Enregistrement de la fenêtre parente
        self.title("Taux de conversion")
        self.geometry("300x100")
        self.conversion_rate = None
        self.create_widgets()

        # S'assurer que la popup est toujours au premier plan
        self.transient(parent)
        self.grab_set()
        self.focus_set()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Entrez le taux de conversion HKD/EUR:").pack(pady=5)
        self.conversion_rate_entry = ctk.CTkEntry(self)
        self.conversion_rate_entry.pack(pady=5)
        ctk.CTkButton(self, text="Confirmer", command=self.confirm).pack(pady=5)

    def confirm(self):
        try:
            self.conversion_rate = float(self.conversion_rate_entry.get())
            self.destroy()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide.")
            self.conversion_rate_entry.focus_set()  # Remettre le focus sur l'entrée
        finally:
            self.parent.focus_set()  # Restaurer le focus sur la fenêtre parente après la fermeture de la popup

# Assurez-vous d'ajuster les autres composants de votre application pour être compatibles avec CustomTkinter.
