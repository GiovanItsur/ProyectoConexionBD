import re
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
            master=self, fg_color="#f4f4f4", corner_radius=0
        )
        self.mainContainer.place(
            relx=0.5, rely=0.5, anchor="center", relwidth=1.0, relheight=1.0
        )

        # Barra lateral
        self.sidebar = ctk.CTkFrame(
            self.mainContainer, fg_color="#2b2b2b", corner_radius=0
        )
        self.sidebar.place(relx=0.0, rely=0.0, relwidth=0.25, relheight=1.0)

        self.lblSidebarTitle = ctk.CTkLabel(
            self.sidebar,
            text=f"Panel ({self.rolUsuario.upper()})",
            font=ctk.CTkFont(family="Roboto", size=20, weight="bold"),
            text_color="#f7d13e"
        )
        self.lblSidebarTitle.pack(pady=(35, 10))

        self.separador = ctk.CTkFrame(self.sidebar, fg_color="#3d3d3d", height=2)
        self.separador.pack(fill="x", padx=20, pady=(0, 20))

        self.btnVerUsuario = ctk.CTkButton(
            self.sidebar,
            text = "⚙ Ver Usuarios",
            fg_color = "transparent",
            hover_color = "#3d3d3d",
            text_color = "#ffffff",
            anchor = "w",
            corner_radius= 8,
            font = ctk.CTkFont(size = 14),
            command = self.accionVerUsuarios
        )
        self.btnVerUsuario.pack(fill = "x", padx = 20, pady = 5)

        if self.rolUsuario.lower() == "admin":
            self.btnRegistrarUsuario = ctk.CTkButton(
                self.sidebar,
                text = "⚙ Registrar Usuario",
                fg_color = "transparent",
                hover_color = "#3d3d3d",
                text_color = "#ffffff",
                anchor = "w",
                corner_radius=8,
                font = ctk.CTkFont(size = 14),
                command = self.accionRegistrarUsuario
            )
            self.btnRegistrarUsuario.pack(fill = "x", padx = 20, pady = 5)

            self.btnEditarUsuarios = ctk.CTkButton(
                self.sidebar,
                text="⚙ Editar / Eliminar",
                fg_color="transparent",
                hover_color="#3d3d3d",
                text_color="#ffffff",
                anchor="w",
                corner_radius=8,
                font=ctk.CTkFont(size=14),
                command=self.accionEditarUsuarios,
            )
            self.btnEditarUsuarios.pack(fill="x", padx=20, pady=5)

        self.btnSalir = ctk.CTkButton(
            self.sidebar,
            text="Salir",
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
            self.mainContainer, fg_color="#ffffff", corner_radius=0
        )
        self.contentArea.place(relx=0.25, rely=0.0, relwidth=0.75, relheight=1.0)

        self.mostrarBienvenida()

    def accionRegistrarUsuario(self):
        self.limpiarAreaContenido()

        lblTitle = ctk.CTkLabel(
            self.contentArea,
            text="Registro de Nuevo Empleado",
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold"),
            text_color="#1a1a1a",
        )
        lblTitle.pack(anchor="w", padx=25, pady=(15, 5))

        self.scrollReg = ctk.CTkScrollableFrame(
            self.contentArea, fg_color="#f9f9f9", height=430
        )
        self.scrollReg.pack(padx=25, pady=5, fill="both", expand=True)

        self.entriesReg = {}
        camposReg = [
            ("Usuario (Sistema)", "usuario"),
            ("Contraseña (Sistema)", "password"),
            ("Rol del Sistema (admin/empleado)", "rol_sistema"),
            ("Nombre", "nombre"),
            ("Apellido", "apellido"),
            ("Género", "genero"),
            ("Domicilio", "domicilio"),
            ("Estado Civil", "estado_civil"),
            ("Turno", "turno"),
            ("Email", "email"),
            ("Rol de Trabajo", "rol_trabajo"),
            ("Nacionalidad", "nacionalidad"),
            ("CURP", "curp"),
            ("Departamento", "departamento"),
            ("RFC (Cifrado AES)", "rfc"),
            ("Teléfono (Cifrado AES)", "telefono"),
            ("NSS (Cifrado AES)", "nss"),
        ]

        for label_text, key in camposReg:
            frm = ctk.CTkFrame(self.scrollReg, fg_color="transparent")
            frm.pack(fill="x", pady=4, padx=10)
            ctk.CTkLabel(frm, text=label_text + ":", width=220, anchor="w").pack(
                side="left", padx=5
            )
            ent = ctk.CTkEntry(frm, width=320, height=32)
            if "password" in key:
                ent.configure(show="*")
            ent.pack(side="left", padx=5)
            self.entriesReg[key] = ent

        self.lblMsgReg = ctk.CTkLabel(
            self.scrollReg, text="", font=ctk.CTkFont(size=12)
        )
        self.lblMsgReg.pack(pady=5)

        btnRegistrar = ctk.CTkButton(
            self.scrollReg,
            text="Guardar Registro en Azure",
            fg_color="#f7d13e",
            hover_color="#d6b534",
            text_color="#1a1a1a",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            command=self.ejecutar_registro,
        )
        btnRegistrar.pack(pady=15)

    def ejecutar_registro(self):
        vals = {k: e.get().strip() for k, e in self.entriesReg.items()}

        if not all(vals.values()):
            self.lblMsgReg.configure(text="Error: Todos los campos son obligatorios.", text_color="#d9534f")
            return

        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", vals["email"]):
            self.lblMsgReg.configure(text="Error: Formato de correo electrónico inválido.", text_color="#d9534f")
            return

        if not re.match(r"^\d{10}$", vals["telefono"]):
            self.lblMsgReg.configure(text="Error: El teléfono debe tener 10 dígitos.", text_color="#d9534f")
            return

        if not re.match(r"^[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z\d]\d$", vals["curp"].upper()):
            self.lblMsgReg.configure(text="Error: CURP inválida (Revisa longitud y formato).", text_color="#d9534f")
            return

        if not re.match(r"^[A-ZÑ&]{3,4}\d{6}[A-Z\d]{3}$", vals["rfc"].upper()):
            self.lblMsgReg.configure(text="Error: RFC inválido (Debe tener 12 o 13 caracteres).", text_color="#d9534f")
            return

        if not re.match(r"^\d{11}$", vals["nss"]):
            self.lblMsgReg.configure(text="Error: El NSS debe tener 11 dígitos numéricos.", text_color="#d9534f")
            return

        exito, mensaje = self.crud.registrar_empleado_completo(
            usuario=vals["usuario"],
            contrasenia=vals["password"],
            rol_sistema=vals["rol_sistema"],
            nombre=vals["nombre"],
            apellido=vals["apellido"],
            genero=vals["genero"],
            domicilio=vals["domicilio"],
            estado_civil=vals["estado_civil"],
            turno=vals["turno"],
            email=vals["email"],
            rol_trabajo=vals["rol_trabajo"],
            nacionalidad=vals["nacionalidad"],
            curp=vals["curp"].upper(),
            departamento=vals["departamento"],
            rfc=vals["rfc"].upper(),
            telefono=vals["telefono"],
            nss=vals["nss"],
        )

        if exito:
            self.lblMsgReg.configure(text=mensaje, text_color="green")
            for e in self.entriesReg.values():
                e.delete(0, "end")
        else:
            self.lblMsgReg.configure(text=mensaje, text_color="#d9534f")

    def ejecutar_modificacion(self):
        vals = {k: e.get().strip() for k, e in self.entriesMod.items()}
        if not all(vals.values()):
            self.lblMsgMod.configure(
                text="Error: Todos los campos son obligatorios para actualizar.",
                text_color="#d9534f",
            )
            return

        if not vals["id_empleado"].isdigit() or not vals["id_usuario"].isdigit():
            self.lblMsgMod.configure(text="Error: ID numéricos.", text_color="#d9534f")
            return
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", vals["email"]):
            self.lblMsgMod.configure(text="Error: Formato de correo inválido.", text_color="#d9534f")
            return
        if not re.match(r"^\d{10}$", vals["telefono"]):
            self.lblMsgMod.configure(text="Error: El teléfono debe tener 10 dígitos.", text_color="#d9534f")
            return
        if not re.match(r"^[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z\d]\d$", vals["curp"].upper()):
            self.lblMsgMod.configure(text="Error: CURP inválida.", text_color="#d9534f")
            return
        if not re.match(r"^[A-ZÑ&]{3,4}\d{6}[A-Z\d]{3}$", vals["rfc"].upper()):
            self.lblMsgMod.configure(text="Error: RFC inválido (12-13 caracteres).", text_color="#d9534f")
            return
        if not re.match(r"^\d{11}$", vals["nss"]):
            self.lblMsgMod.configure(text="Error: El NSS debe tener 11 dígitos.", text_color="#d9534f")
            return

        exito, mensaje = self.crud.modificar_empleado(
            id_empleado=int(vals["id_empleado"]),
            id_usuario=int(vals["id_usuario"]),
            usuario=vals["usuario"],
            contrasenia=vals["contrasenia"],
            rol_sistema=vals["rol_sistema"],
            nombre=vals["nombre"],
            apellido=vals["apellido"],
            genero=vals["genero"],
            domicilio=vals["domicilio"],
            estado_civil=vals["estado_civil"],
            turno=vals["turno"],
            email=vals["email"],
            rol=vals["rol"],
            nacionalidad=vals["nacionalidad"],
            curp=vals["curp"].upper(),
            departamento=vals["departamento"],
            rfc=vals["rfc"].upper(),
            telefono=vals["telefono"],
            nss=vals["nss"],
        )

        if exito:
            self.lblMsgMod.configure(text=mensaje, text_color="green")
            for e in self.entriesMod.values():
                e.delete(0, "end")
        else:
            self.lblMsgMod.configure(text=mensaje, text_color="#d9534f")

    def limpiarAreaContenido(self):
        for widget in self.contentArea.winfo_children():
            widget.destroy()

    def mostrarBienvenida(self):
        self.limpiarAreaContenido()
        self.lblBienvenida = ctk.CTkLabel(
            self.contentArea,
            text="Bienvenido al Sistema de Gestión",
            font=ctk.CTkFont(family="Roboto", size=26, weight="bold"),
            text_color="#2b2b2b"
        )
        self.lblBienvenida.place(relx=0.08, rely=0.1)

        self.decorador = ctk.CTkFrame(self.contentArea, fg_color="#f7d13e", width=60, height=4)
        self.decorador.place(relx=0.08, rely=0.16)

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

            if self.rolUsuario.lower() == "admin":
                headers = [
                    "ID Emp", "ID Usr", "Usuario", "Nombre", "Apellido", "Género",
                    "Domicilio", "Est. Civil", "Turno", "Email", "Rol Trabajo",
                    "Nacionalidad", "CURP", "Depto", "RFC", "Teléfono", "NSS"
                ]
            else:
                headers = [
                    "ID", "Nombre", "Apellido", "Género", "Domicilio", "Est. Civil",
                    "Turno", "Email", "Rol Trabajo", "Nacionalidad", "CURP",
                    "Depto", "RFC", "Teléfono", "NSS"
                ]

            headerFrame = ctk.CTkFrame(self.scrollGrid, fg_color="#f7d13e", height=35)
            headerFrame.pack(fill="x", pady=2)

            for h in headers:
                lbl = ctk.CTkLabel(
                    headerFrame,
                    text=h,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color="#1a1a1a",
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
        self.id_seleccionado = None
        self.datos_seleccionados = None

        lblTitle = ctk.CTkLabel(
            self.contentArea,
            text="Gestión de Edición y Bajas de Empleados",
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold"),
            text_color="#1a1a1a",
        )
        lblTitle.pack(anchor="w", padx=25, pady=(15, 5))

        frmAcciones = ctk.CTkFrame(self.contentArea, fg_color="transparent")
        frmAcciones.pack(fill="x", padx=25, pady=5)

        self.btnAbrirEdicion = ctk.CTkButton(
            frmAcciones,
            text="✏️ Editar Seleccionado",
            state="disabled",
            fg_color="#f0ad4e",
            hover_color="#ec971f",
            text_color="#ffffff",
            font=ctk.CTkFont(weight="bold"),
            command=self.mostrarFormularioEdicion
        )
        self.btnAbrirEdicion.pack(side="left", padx=(0, 10))

        self.btnBorrarSeleccion = ctk.CTkButton(
            frmAcciones,
            text="🗑️ Eliminar Seleccionado",
            state="disabled",
            fg_color="#d9534f",
            hover_color="#c9302c",
            text_color="#ffffff",
            font=ctk.CTkFont(weight="bold"),
            command=self.ejecutar_eliminacion_seleccionada
        )
        self.btnBorrarSeleccion.pack(side="left")

        self.lblMsgAccion = ctk.CTkLabel(frmAcciones, text="", font=ctk.CTkFont(size=12))
        self.lblMsgAccion.pack(side="left", padx=15)

        gridContainer = ctk.CTkFrame(self.contentArea, fg_color="#f9f9f9")
        gridContainer.pack(padx=25, pady=10, fill="both", expand=True)

        self.canvasEdit = tk.Canvas(gridContainer, bg="#f9f9f9", highlightthickness=0)
        scrollVert = ctk.CTkScrollbar(gridContainer, orientation="vertical", command=self.canvasEdit.yview)
        self.canvasEdit.configure(yscrollcommand=scrollVert.set)

        scrollVert.pack(side="right", fill="y")
        self.canvasEdit.pack(side="left", fill="both", expand=True)

        self.scrollGridEdit = ctk.CTkFrame(self.canvasEdit, fg_color="#f9f9f9")
        self.canvasEdit.create_window((0, 0), window=self.scrollGridEdit, anchor="nw")
        self.scrollGridEdit.bind("<Configure>",
                                 lambda e: self.canvasEdit.configure(scrollregion=self.canvasEdit.bbox("all")))

        exito, datos = self.crud.mostrar_empleados_admin()

        if not exito or not datos:
            ctk.CTkLabel(self.scrollGridEdit, text="No hay registros disponibles.", text_color="gray").pack(pady=20)
            return

        headers = ["ID Emp", "Nombre", "Apellido", "Rol de Trabajo"]
        headerFrame = ctk.CTkFrame(self.scrollGridEdit, fg_color="#f7d13e", height=35)
        headerFrame.pack(fill="x", pady=2)

        anchos = [80, 200, 200, 180]
        for h, ancho in zip(headers, anchos):
            ctk.CTkLabel(
                headerFrame, text=h, font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#1a1a1a", width=ancho, anchor="w"
            ).pack(side="left", padx=10)

        self.filas_frames = []

        for fila in datos:
            rowFrame = ctk.CTkFrame(self.scrollGridEdit, fg_color="#ffffff", height=32, cursor="hand2")
            rowFrame.pack(fill="x", pady=2)

            valores_mostrar = [fila[0], fila[3], fila[4], fila[10]]

            def hacer_seleccion(f_id, f_data, f_frame):
                def seleccionar(event):
                    self.id_seleccionado = f_id
                    self.datos_seleccionados = f_data

                    for fr in self.filas_frames:
                        fr.configure(fg_color="#ffffff")

                    f_frame.configure(fg_color="#e2e8f0")

                    # Habilitar los botones superiores
                    self.btnAbrirEdicion.configure(state="normal")
                    self.btnBorrarSeleccion.configure(state="normal")
                    self.lblMsgAccion.configure(text=f"Seleccionado: ID {f_id}", text_color="#1a1a1a")

                return seleccionar

            evento_click = hacer_seleccion(fila[0], fila, rowFrame)
            rowFrame.bind("<Button-1>", evento_click)
            self.filas_frames.append(rowFrame)

            for valor, ancho in zip(valores_mostrar, anchos):
                lblVal = ctk.CTkLabel(
                    rowFrame, text=str(valor) if valor is not None else "",
                    font=ctk.CTkFont(size=11), text_color="#333333", width=ancho, anchor="w"
                )
                lblVal.pack(side="left", padx=10)
                # El clic en el texto también dispara la selección de la fila
                lblVal.bind("<Button-1>", evento_click)

    def ejecutar_eliminacion_seleccionada(self):
        if hasattr(self, 'id_seleccionado') and self.id_seleccionado:
            exito, mensaje = self.crud.eliminar_empleado(int(self.id_seleccionado))
            if exito:
                self.accionEditarUsuarios()  # Recarga la tabla limpia
                self.lblMsgAccion.configure(text="Registro eliminado correctamente.", text_color="green")
            else:
                self.lblMsgAccion.configure(text=mensaje, text_color="#d9534f")

    def mostrarFormularioEdicion(self):
        self.limpiarAreaContenido()

        lblTitle = ctk.CTkLabel(
            self.contentArea,
            text=f"✏️ Modificando Empleado ID: {self.id_seleccionado}",
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold"),
            text_color="#1a1a1a",
        )
        lblTitle.pack(anchor="w", padx=25, pady=(15, 5))

        self.scrollEdit = ctk.CTkScrollableFrame(self.contentArea, fg_color="#f9f9f9", height=430)
        self.scrollEdit.pack(padx=25, pady=5, fill="both", expand=True)

        self.entriesMod = {}
        camposMod = [
            ("ID Empleado a Modificar", "id_empleado"),
            ("ID Usuario asociado", "id_usuario"),
            ("Usuario (Sistema)", "usuario"),
            ("Contraseña (Nueva)", "contrasenia"),
            ("Rol del Sistema (admin/empleado)", "rol_sistema"),
            ("Nombre", "nombre"),
            ("Apellido", "apellido"),
            ("Género", "genero"),
            ("Domicilio", "domicilio"),
            ("Estado Civil", "estado_civil"),
            ("Turno", "turno"),
            ("Email", "email"),
            ("Rol de Trabajo", "rol"),
            ("Nacionalidad", "nacionalidad"),
            ("CURP", "curp"),
            ("Departamento", "departamento"),
            ("RFC (Nuevo Cifrado AES)", "rfc"),
            ("Teléfono (Nuevo Cifrado AES)", "telefono"),
            ("NSS (Nuevo Cifrado AES)", "nss"),
        ]

        mapeo_datos = {
            "id_empleado": 0, "id_usuario": 1, "usuario": 2, "nombre": 3,
            "apellido": 4, "genero": 5, "domicilio": 6, "estado_civil": 7,
            "turno": 8, "email": 9, "rol": 10, "nacionalidad": 11,
            "curp": 12, "departamento": 13, "rfc": 14, "telefono": 15, "nss": 16
        }

        for label_text, key in camposMod:
            frm = ctk.CTkFrame(self.scrollEdit, fg_color="transparent")
            frm.pack(fill="x", pady=3, padx=10)
            ctk.CTkLabel(frm, text=label_text + ":", width=220, anchor="w").pack(side="left", padx=5)

            ent = ctk.CTkEntry(frm, width=320, height=32)

            if "contrasenia" in key:
                ent.configure(show="*")
                ent.insert(0, "")
            elif "rol_sistema" in key:
                ent.insert(0, "empleado")
            elif key in mapeo_datos:
                idx = mapeo_datos[key]
                valor_actual = self.datos_seleccionados[idx]
                if valor_actual is not None:
                    ent.insert(0, str(valor_actual))

            if key in ["id_empleado", "id_usuario"]:
                ent.configure(state="disabled", fg_color="#e0e0e0")

            ent.pack(side="left", padx=5)
            self.entriesMod[key] = ent

        self.lblMsgMod = ctk.CTkLabel(self.scrollEdit, text="", font=ctk.CTkFont(size=12))
        self.lblMsgMod.pack(pady=5)

        frmBotones = ctk.CTkFrame(self.scrollEdit, fg_color="transparent")
        frmBotones.pack(pady=10)

        ctk.CTkButton(
            frmBotones, text="Cancelar", fg_color="#d9534f", hover_color="#c9302c",
            command=self.accionEditarUsuarios
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            frmBotones, text="Actualizar en Azure", fg_color="#f7d13e", hover_color="#d6b534",
            text_color="#1a1a1a", font=ctk.CTkFont(weight="bold"),
            command=self.ejecutar_modificacion
        ).pack(side="left", padx=10)

    def cerrarSesion(self):
        self.limpiarAreaContenido()

        self.controlador.cambiarPantalla(pantallaLogin)

class pantallaLogin(ctk.CTkFrame):
    def __init__(self, master, controlador):
        super().__init__(master, fg_color = "#ffffff")
        self.controlador = controlador
        self.crud = EmpleadosCRUD()

        self.cuadroLogin = ctk.CTkFrame(
            master = self, fg_color = "#ffffff", corner_radius = 25
        )
        self.cuadroLogin.place(
            relx = 0.5, rely = 0.5, anchor = "center", relwidth = 1.0 , relheight = 1.0
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