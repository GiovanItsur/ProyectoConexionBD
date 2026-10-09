import customtkinter as ctk
import mysql.connector

class login(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración general de login, columnas y filas
        self.title("Login MySQL")
        self.geometry("450x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # Title
        self.labelTitle = ctk.CTkLabel(self, text = "Inicio de sesión")
        self.labelTitle.grid(row = 0, column = 0, padx = 10, pady = (10, 0), sticky = "n")


# Función main
if __name__ == "__main__":
    app = login()
    app.mainloop()

"""
class login(ctk.CTk):
    def __init__(self):
        super().__init__()

        # -- Parametros de pantalla
        self.title("my app")
        self.geometry("400x180")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # -- Creación de checkboxes
        self.checkbox1 = ctk.CTkCheckBox(self, text = "Checkbox1")
        self.checkbox1.grid(row = 0, column = 0, padx = 10, pady = (10, 0), sticky = "w")
        self.checkbox2 = ctk.CTkCheckBox(self, text = "Checkbox2")
        self.checkbox2.grid(row = 1, column = 0, padx = 10, pady = (10, 0), sticky = "w")

        self.mainloop()

# Función main y main loop
if __name__ == "__main__":
    app = login()
    app.mainloop()
"""