import tkinter as tk
import customtkinter as ctk

from backEnd.CRUD import EmpleadosCRUD

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class pantallaMenu(ctk.CTkFrame):
    def __init__(self, master, controlador, rolUsuario):
        super().__init__(master, fg_color = "#2b2b2b")
        self.controlador = controlador
        self.rolUsuario = rolUsuario
        self.crud = EmpleadosCRUD()

        # Contenedor principal
        self.mainContainer = ctk.CTkFrame(
            master = self, fg_color = "#f4f4f4", corner_radius = 25
        )
        self.mainContainer.place(
            relx = 0.5, rely = 0.5, anchor = "center", relwidth = 0.9, relheight = 0.9
        )

        # Barra lateral
        self.sidebar = ctk.CTkFrame(
            self.mainContainer, fg_color = "#2b2b2b", corner_radius = 25
        )
        self.sidebar.place(relx = 0.0, rely = 0.0, relwidth = 0.28, relheight = 1.0)

        self.lblSidebarTitle = ctk.CTkLabel(
            self.sidebar,
            text = f"Panel ({self.rolUsuario.upper()})",
            font = ctk.CTkFont(family = "Roboto", size = 18, weight = "bold"),
            text_color = "#ffffff"
        )
        self.lblSidebarTitle.pack(pady = (40, 30))

        self.btnVerUsuario = ctk.CTkButton(
            self.sidebar,
            text = "👥 Ver Usuarios",
            fg_color = "transparent",
            hover_color = "#3d3d3d",
            text_color = "#ffffff",
            anchor = "w",
            font = ctk.CTkFont(size = 14),
            command = self.accionVerUsuarios
        )
        self.btnVerUsuario.pack(fill = "x", padx = 20, pady = 10)

        if self.rolUsuario.lower() == "admin":
            self.btnRegistrarUsuario = ctk.CTkButton(
                self.sidebar,
                text = "➕ Registrar Usuario",
                fg_color = "transparent",
                hover_color = "#3d3d3d",
                text_color = "#ffffff",
                anchor = "w",
                font = ctk.CTkFont(size = 14),
                command = self.accionRegistrarUsuario
            )
            self.btnRegistrarUsuario.pack(fill = "x", padx = 15, pady = 8)

            self.btnEditarUsuarios = ctk.CTkButton(
                self.sidebar,
                text="⚙️ Editar / Eliminar",
                fg_color="transparent",
                hover_color="#3d3d3d",
                text_color="#ffffff",
                anchor="w",
                font=ctk.CTkFont(size=14),
                command=self.accionEditarUsuarios,
            )
            self.btnEditarUsuarios.pack(fill="x", padx=20, pady=10)

        self.btnSalir = ctk.CTkButton(
            self.sidebar,
            text="🚪 Salir",
            fg_color="#d9534f",
            hover_color="#c9302c",
            text_color="#ffffff",
            anchor="w",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.cerrarSesion,
        )
        self.btnSalir.pack(side="bottom", fill="x", padx=20, pady=30)

        # Contenido principal
        self.contentArea = ctk.CTkFrame(
            self.mainContainer, fg_color = "#ffffff", corner_radius = 0
        )
        self.contentArea.place(relx = 0.28, rely = 0.0, relwidth = 0.72, relheight = 1.0)

        self.mostrarBienvenida()

    def accionRegistrarUsuario(self):
        self.limpiarAreaContenido()

        lblTitle = ctk.CTkLabel(
            self.contentArea,
            text = "Registro de Nuevo Empleado",
            font = ctk.CTkFont(family = "Roboto", size = 18, weight = "bold"),
            text_color = "#1a1a1a"
        )
        lblTitle.pack(anchor = "w", padx = 25, pady = (15, 5))

        self.scrollReg = ctk.CTkScrollableFrame(
            self.contentArea, fg_color = "#f9f9f9", height = 430
        )
        self.scrollReg.pack(padx = 25, pady = 5, fill = "both", expand = True)



    def limpiarAreaContenido(self):
        for widget in self.contentArea.winfo_children():
            widget.destroy()

    def mostrarBienvenida(self):
        self.limpiarAreaContenido()
        self.lblBienvenida = ctk.CTkLabel(
            self.contentArea,
            text = "Bienvenido al Sístema de Gestión",
            font = ctk.CTkFont(family = "Roboto", size = 22, weight = "bold"),
            text_color = "#1a1a1a"
        )
        self.lblBienvenida.place(relx = 0.1, rely = 0.1)

        self.lblSub = ctk.CTkLabel(
            self.contentArea,
            text = (
                "Selecciona una opción en el menú lateral para interactuar con la"
                " base de datos."
            ),
            font = ctk.CTkFont(family = "Roboto", size = 14),
            text_color = "#666666"
        )
        self.lblSub.place(relx = 0.1, rely = 0.18)

    def accionVerUsuarios(self):
        self.limpiarAreaContenido()

        lblTituloGrid = ctk.CTkLabel(
            self.contentArea,
            text="Lista de Reporte de Usuarios",
            font=ctk.CTkFont(family="Roboto", size=20, weight="bold"),
            text_color="#1a1a1a",
        )
        lblTituloGrid.pack(anchor="w", padx=30, pady=(20, 10))

        gridContainer = ctk.CTkFrame(self.contentArea, fg_color="#f9f9f9")
        gridContainer.pack(padx=30, pady=10, fill="both", expand=True)

        self.canvas = tk.Canvas(
            gridContainer, bg="#f9f9f9", highlightthickness=0, height=350
        )

        # Barras de desplazamiento personalizada con CustomTkinter
        scrollHoriz = ctk.CTkScrollbar(
            gridContainer, orientation="horizontal", command=self.canvas.xview
        )
        scrollVert = ctk.CTkScrollbar(
            gridContainer, orientation="vertical", command=self.canvas.yview
        )

        self.canvas.configure(
            xscrollcommand=scrollHoriz.set, yscrollcommand=scrollVert.set
        )

        scrollHoriz.pack(side="bottom", fill="x")
        scrollVert.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollGrid = ctk.CTkFrame(self.canvas, fg_color="#f9f9f9")
        self.canvas.create_window((0, 0), window=self.scrollGrid, anchor="nw")

        def ajustarScroll(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.scrollGrid.bind("<Configure>", ajustarScroll)

        if self.rolUsuario.lower() == "admin":
            exito, datos = self.crud.mostrar_empleados_admin()
        else:
            exito, datos = self.crud.mostrar_empleados_normal()

        if exito:
            if not datos:
                lblVacio = ctk.CTkLabel(
                    self.scrollGrid,
                    text="No hay registros en la base de datos.",
                    text_color="gray",
                )
                lblVacio.pack(pady=20)
                return

            headers = [
                "ID",
                "Nombre",
                "Apellido",
                "Genero",
                "Domicilio",
                "Est. Civil",
                "Turno",
                "Email",
                "Rol Trabajo",
                "Nacionalidad",
                "CURP",
                "Departamento",
                "RFC",
                "Teléfono",
                "NSS",
            ]
            headerFrame = ctk.CTkFrame(self.scrollGrid, fg_color="#2b2b2b", height=35)
            headerFrame.pack(fill="x", pady=2)

            for h in headers:
                lbl = ctk.CTkLabel(
                    headerFrame,
                    text=h,
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#ffffff",
                    width=110,
                )
                lbl.pack(side="left", padx=2)

            # Filas de la base de datos
            for fila in datos:
                rowFrame = ctk.CTkFrame(self.scrollGrid, fg_color="#ffffff", height=32)
                rowFrame.pack(fill="x", pady=2)

                for valor in fila:
                    lblVal = ctk.CTkLabel(
                        rowFrame,
                        text=str(valor) if valor is not None else "",
                        font=ctk.CTkFont(size=10),
                        text_color="#333333",
                        width=110,
                    )
                    lblVal.pack(side="left", padx=2)

        else:
            lblError = ctk.CTkLabel(
                self.scrollGrid, text=f"Error al obtener datos: {datos}", text_color="red"
            )
            lblError.pack(pady=20)

    def accionEditarUsuarios(self):
        self.limpiarAreaContenido()

        lblEdit = ctk.CTkLabel(
            self.contentArea,
            text = "Gestión y Edición de Empleados",
            font = ctk.CTkFont(family = "Roboto", size = 20, weight = "bold"),
            text_color = "#1a1a1a"
        )
        lblEdit.pack(anchor = "w", padx = 25, pady = (15, 5))

        self.scrollForm = ctk.CTkScrollableFrame(
            self.contentArea, fg_color = "#f9f9f9", height = 420
        )
        self.scrollForm.pack(padx = 25, pady = 5, fill = "both", expand = True)

        # Registro de empleado

        lblSecReg = ctk.CTkLabel(
            self.scrollForm,
            text = "➕ Registrar Nuevo Empleado",
            font = ctk.CTkFont(size = 15, weight = "bold"),
            text_color = "#2b2b2b"
        )
        lblSecReg.pack(anchor = "w", pady = (10, 10), padx = 10)

    def cerrarSesion(self):
        self.controlador.cambiarPantalla(pantallaLogin)


class pantallaLogin(ctk.CTkFrame):
    def __init__(self, master, controlador):
        super().__init__(master, fg_color = "#2b2b2b")
        self.controlador = controlador
        self.crud = EmpleadosCRUD()

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

        self.lblMensaje = ctk.CTkLabel(
            self.contentLeft, text = "", font = ctk.CTkFont(size = 11), text_color = "red"
        )
        self.lblMensaje.pack(pady = 5)

        self.btnLogin = ctk.CTkButton(
            self.contentLeft,
            text = "Entrar",
            width = 140,
            height = 40,
            corner_radius = 20,
            fg_color = "#2b2b2b",
            hover_color = "#444444",
            text_color = "#ffffff",
            font = ctk.CTkFont(family = "Roboto", size = 13),
            command = self.goToMenu
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

    def goToMenu(self):
        usuario = self.entryUser.get().strip()
        password = self.entryPassword.get().strip()

        if not usuario or not password:
            self.lblMensaje.configure(text = "Rellena todos los campos")
            return

        exito, mensaje, rol = self.crud.validar_login(usuario, password)

        if exito:
            self.controlador.cambiarPantallaConRol(pantallaMenu, rol)
        else:
            self.lblMensaje.configure(text = mensaje)



class mainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1050x580")
        self.title("Sistema Azure MySQL")
        self.resizable(False, False)

        self.pantallaActual = None
        self.cambiarPantalla(pantallaLogin)

    def cambiarPantalla(self, clasePantalla):
        if self.pantallaActual is not None:
            self.pantallaActual.destroy()

        self.pantallaActual = clasePantalla(master = self, controlador = self)
        self.pantallaActual.pack(fill = "both", expand = True)

    def cambiarPantallaConRol(self, clasePantalla, rol):
        if self.pantallaActual is not None:
            self.pantallaActual.destroy()

        self.pantallaActual = clasePantalla(
            master = self, controlador = self, rolUsuario = rol
        )
        self.pantallaActual.pack(fill = "both", expand = True)


# Función main
if __name__ == "__main__":
    app = mainApp()
    app.mainloop()