import customtkinter as ctk
import mysql.connector
from PIL import Image
import os


class pantallaLogin(ctk.CTkFrame):
    def __init__(self, master, controlador):

        # Inicializacion de frame (pantalla)
        super().__init__(master, fg_color = "#2b2b2b")
        self.controlador = controlador

        self.cuadroLogin = ctk.CTkFrame(
            master = self, fg_color = "#ffffff", corner_radius = 25
        )
        self.cuadroLogin.place(
            relx = 0.5, rely = 0.5, anchor = "center", relwidth = 0.85, relheight = 0.85
        )

        # -- Sección izquierda
        self.leftFrame = ctk.CTkFrame(
            self.cuadroLogin, fg_color = "transparent", corner_radius = 0
        )
        self.leftFrame.place(relx = 0.0, rely = 0.0, relwidth = 0.5, relheight = 1.0)

        self.contentLeft = ctk.CTkFrame(self.leftFrame, fg_color = "transparent")
        self.contentLeft.place(relx = 0.5, rely = 0.5, anchor = "center", relwidth = 0.85)

        self.titulo = ctk.CTkLabel(
            self.contentLeft,
            text = "Iniciar Sesión",
            font = ctk.CTkFont(family = "Roboto", size = 26, weight = "bold"),
            text_color = "#1a1a1a",
        )
        self.titulo.pack(pady = (0, 20))

        self.entryUser = ctk.CTkEntry(
            self.contentLeft,
            placeholder_text = "Usuario",
            width = 260,
            height = 42,
            corner_radius = 12,
            fg_color = "#f4f4f4",
            border_width = 0,
            text_color = "#1b1b1b",
            font = ctk.CTkFont(family = "Roboto", size = 13)
        )
        self.entryUser.pack(pady = 10)

        self.entryPassword = ctk.CTkEntry(
            self.contentLeft,
            placeholder_text = "Password",
            show = "*",
            width = 260,
            height = 42,
            corner_radius = 12,
            fg_color = "#f4f4f4",
            border_width = 0,
            text_color="#1b1b1b",
            font = ctk.CTkFont(family = "Roboto", size = 13)
        )
        self.entryPassword.pack(pady = 10)

        self.btnLogin = ctk.CTkButton(
            self.contentLeft,
            text = "Entrar",
            width = 140,
            height = 40,
            corner_radius = 20,
            fg_color = "#2b2b2b",
            hover_color = "#444444",
            text_color = "#ffffff",
            font = ctk.CTkFont(family = "Roboto", size = 13)
        )
        self.btnLogin.pack(pady = (20, 5))

        # -- Sección derecha
        self.rightFrame = ctk.CTkFrame(
            self.cuadroLogin, fg_color = "#f7d13e", corner_radius = 0
        )
        self.rightFrame.place(relx = 0.5, rely = 0.0, relwidth = 0.5, relheight = 1.0)

        self.contentRight = ctk.CTkFrame(self.rightFrame, fg_color = "transparent")
        self.contentRight.place(relx = 0.5, rely = 0.5, anchor = "center", relwidth = 0.85)

        self.lblWelcome1 = ctk.CTkLabel(
            self.contentRight,
            text = "¡Bienvenido a",
            font = ctk.CTkFont(family = "Roboto", size = 24),
            text_color = "#ffffff"
        )
        self.lblWelcome1.pack(anchor = "center")

        self.lblWelcome2 = ctk.CTkLabel(
            self.contentRight,
            text = "MySQL!",
            font = ctk.CTkFont(family = "Roboto", size = 28),
            text_color = "#ffffff"
        )
        self.lblWelcome2.pack(anchor = "center", pady = (0, 10))

        self.lblSub = ctk.CTkLabel(
            self.contentRight,
            text = "Del ITSUR A Sus MANOS",
            font = ctk.CTkFont(family = "Roboto", size = 13),
            text_color = "#ffffff",
            justify = "center"
        )
        self.lblSub.pack(anchor = "center", pady = (0, 20))

class mainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("800x520")
        self.title("my app")
        self.resizable(False, False)

        self.pantallaActual = None
        self.cambiarPantalla(pantallaLogin)

    def cambiarPantalla(self, clasePantalla):
        if self.pantallaActual is not None:
            self.pantallaActual.destroy()

        self.pantallaActual = clasePantalla(master = self, controlador = self)

        self.pantallaActual.pack(fill = "both", expand = True)

# Función main
if __name__ == "__main__":
    app = mainApp()
    app.mainloop()