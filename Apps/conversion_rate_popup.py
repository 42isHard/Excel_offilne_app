import customtkinter as ctk
from tkinter import messagebox

class ConversionRatePopup(ctk.CTkToplevel):
    """
    Popup pour entrer le taux de conversion monétaire.

    Cette popup permet à l'utilisateur de saisir un taux de conversion, par exemple de HKD à EUR.
    """

    def __init__(self, parent):
        """
        Initialise la popup de taux de conversion.

        Args:
            parent: Fenêtre parente de la popup.
        """
        super().__init__(parent)
        self.parent = parent  # Enregistrement de la fenêtre parente
        self.title("Taux de conversion")
        self.geometry("300x150")
        self.conversion_rate = None  # Taux de conversion à récupérer
        self.create_widgets()

        # S'assure que la popup est toujours au premier plan par rapport à la fenêtre parente
        self.transient(parent)
        self.grab_set()
        self.focus_set()

    def create_widgets(self):
        """
        Crée les widgets pour la popup de taux de conversion.
        """
        ctk.CTkLabel(self, text="Le logiciel a détecté une colonne en HKD.").pack(pady=5)
        ctk.CTkLabel(self,
                     text="Pour garder la cohérence du fichier concténé").pack(
            pady=5)
        ctk.CTkLabel(self, text="Veuillez entrer le taux de conversion HKD/EUR:").pack(pady=5)
        self.conversion_rate_entry = ctk.CTkEntry(self)
        self.conversion_rate_entry.pack(pady=5)
        ctk.CTkButton(self, text="Confirmer", command=self.confirm).pack(pady=5)

    def confirm(self):
        """
        Confirme la saisie du taux de conversion.

        Tente de convertir la saisie de l'utilisateur en un nombre à virgule flottante.
        Affiche une erreur si la saisie n'est pas valide. Ferme la popup si la saisie est valide.
        """
        try:
            self.conversion_rate = float(self.conversion_rate_entry.get())
            self.destroy()  # Ferme la popup si la conversion réussit
        except ValueError:
            # Affiche une erreur et remet le focus sur l'entrée si la conversion échoue
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide.")
            self.conversion_rate_entry.focus_set()
        finally:
            # Restaure le focus sur la fenêtre parente après la fermeture de la popup
            self.parent.focus_set()