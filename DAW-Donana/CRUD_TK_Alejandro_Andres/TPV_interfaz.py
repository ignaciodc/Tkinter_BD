import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from TPV_modelo import Mesa, Alergeno, Producto, Linea_pedido, Pedido
import TPV_base_datos as bd

# --- CONFIGURACIÓN DE ESTILOS GLOBALES ---
BG_GENERAL = "#FDF8F5"   
BG_ACCENT = "#431E0E"       
BG_BUTTON = "#72481E"     
FG_LIGHT = "#FFFFFF"        
FG_DARK = "#2D2D2D"        
FUENTE_TITULO = ("Segoe UI", 55, "italic")
FUENTE_TEXTO = ("Segoe UI", 12)

# --- ALÉRGENOS OFICIALES UE ---
ALERGENOS_UE = [
    "Gluten", "Crustáceos", "Huevos", "Pescado", "Cacahuetes", 
    "Soja", "Lácteos", "Frutos de cáscara", "Apio", "Mostaza", 
    "Sésamo", "Sulfitos", "Altramuces", "Moluscos"
]

class Aplicacion(tk.Tk):
    """
    Aplicación del tpv, contiene todas las ventanas.
    """
    def __init__(self) -> None:
        super().__init__()
        self.title('Gestión de Restaurante')
        self.attributes('-fullscreen', True)
        self.geometry("1500x900")
        self.configure(bg=BG_GENERAL)
        self.option_add('*Font','SegoeUI 12')

        container = tk.Frame(self, bg=BG_GENERAL)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        bd.abrir_db()

        self.frames = {}

        # Recargamos la información real de la base de datos
        self.mesas = bd.obtener_mesas()
        self.productos = bd.obtener_productos()
        self.pedidos = bd.obtener_pedidos()
        
        self.mesa_seleccionada = None
        self.pedido_actual = None
        self.producto_actual = None

        # Comprobamos que frame tenemos que mostrar
        for F in (Pagina_Inicio, Ver_pedidos, Ver_mesas, Gestion_mesa, Anadir_linea_pedido, Hacer_pedido, Panel_Administrador):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Pagina_Inicio")

    def show_frame(self, nombre_frame):
        """
        Muestra el frame indicado
        """
        frame = self.frames[nombre_frame]
        if hasattr(frame, "actualizar"):
            frame.actualizar()
        frame.tkraise()

class Pagina_Inicio(tk.Frame):
    def __init__(self, parent, controller):  
        self.controller = controller
        super().__init__(parent, bg="#1A1A1A") 

        self.grid_columnconfigure(0, weight=1)

        # --- BOTÓN DE ADMINISTRACIÓN ---
        self.__but_admin = tk.Button(
            self, text='⚙️ ADMINISTRAR', font=('Segoe UI', 11, 'bold'), 
            bg="#2A2A2A", fg="#D4AF37", activebackground="#3A3A3A", activeforeground="#D4AF37",
            relief="flat", cursor="hand2", padx=15, pady=8,
            command=lambda: controller.show_frame("Panel_Administrador")
        )
        
        self.__but_admin.grid(row=0, column=0, sticky="ne", padx=25, pady=25)

        # Título de Bienvenida
        self.__label_bienvenida = tk.Label(
            self, text='Bienvenido', font=("Segoe UI", 80, "bold italic"), bg="#1A1A1A", fg="#D4AF37"
        )
        
        self.__label_bienvenida.grid(row=0, column=0, pady=(180, 10))

        self.__frame_opciones = tk.Frame(self, bg="#1A1A1A", padx=20, pady=20)
        self.__frame_opciones.grid(row=2, column=0)

        btn_params = {
            "font": ('Segoe UI', 14, 'bold'), "bg": "#C17A2D", "fg": "white",
            "relief": "flat", "padx": 25, "pady": 15, "activebackground": "#A66624",
            "activeforeground": "white", "cursor": "hand2"
        }

        # Botón Hacer pedidos
        self.__but_hacer_pedido = tk.Button(
            self.__frame_opciones, text='+ COBRO RÁPIDO', width=20, 
            command=lambda: controller.show_frame("Hacer_pedido"), **btn_params
        )
        self.__but_hacer_pedido.grid(row=0, column=0, padx=15)
        
        # Botón Ver pedidos
        self.__but_ver_pedidos = tk.Button(
            self.__frame_opciones, text='VER PEDIDOS', width=20, 
            command=lambda: controller.show_frame("Ver_pedidos"), **btn_params
        )
        self.__but_ver_pedidos.grid(row=0, column=1, padx=15)


        # Botón Ver mesas
        self.__but_ver_mesas = tk.Button(
            self, text='MAPA DE MESAS', width=45, command=lambda: controller.show_frame("Ver_mesas"), 
            font=('Segoe UI', 15, 'bold'), bg="#431E0E", fg="white", relief="flat", pady=15, cursor="hand2"
        )
        self.__but_ver_mesas.grid(row=3, column=0, pady=25)

        # Botón salir
        self.__but_salir = tk.Button(
            self, text='CERRAR SISTEMA', width=20, command=self.salir, bg="#E7DADA", fg="#121111",
            relief="flat", font=('Segoe UI', 10, 'bold'), activebackground="#1A1A1A", activeforeground="#FF4444", cursor="hand2"
        )
        self.__but_salir.grid(row=4, column=0, pady=60)

    def salir(self):
        """
        Sale del programa
        """
        bd.cerrar_bd() # Cerramos conexión a la base de datos
        exit()

class Ver_pedidos(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_GENERAL)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)

        # --- 1. SECCIÓN: PEDIDOS REALIZADOS ---
        self.__label_pedidos_realizados = tk.Label(self, text='Pedidos Realizados', font=("Segoe UI", 40, "italic"), bg=BG_GENERAL, fg=BG_ACCENT)
        self.__label_pedidos_realizados.grid(row=0, column=0, pady=(100, 10))

        # Frame contenedor para la lista de realizados y su scrollbar
        self.__frame_realizados = tk.Frame(self, bg=BG_GENERAL)
        self.__frame_realizados.grid(row=1, column=0, pady=10, padx=300, sticky="ew")

        self.__scroll_realizados = tk.Scrollbar(self.__frame_realizados, orient="vertical")
        self.__scroll_realizados.pack(side="right", fill="y")

        # Lista de pedidos realizados
        self.__lista_pedidos_realizados = tk.Listbox(
            self.__frame_realizados, height=15, bg="white", fg=FG_DARK, 
            font=('Consolas', 12), borderwidth=2, relief="groove", 
            yscrollcommand=self.__scroll_realizados.set
        )
        self.__lista_pedidos_realizados.pack(side="left", fill="both", expand=True)
        self.__scroll_realizados.config(command=self.__lista_pedidos_realizados.yview)


        # --- 2. SECCIÓN: PEDIDOS EN ESPERA ---
        self.__label_pedidos_pendientes = tk.Label(self, text='Pedidos en Espera', font=("Segoe UI", 40, "italic"), bg=BG_GENERAL, fg=BG_ACCENT)
        self.__label_pedidos_pendientes.grid(row=2, column=0, pady=(20, 10))

        # Frame contenedor para la lista de espera y su scrollbar
        self.__frame_espera = tk.Frame(self, bg=BG_GENERAL)
        self.__frame_espera.grid(row=3, column=0, pady=10, padx=300, sticky="ew")

        self.__scroll_espera = tk.Scrollbar(self.__frame_espera, orient="vertical")
        self.__scroll_espera.pack(side="right", fill="y")

        self.__lista_pedidos_espera = tk.Listbox(
            self.__frame_espera, height=15, bg="white", fg=FG_DARK, 
            font=('Consolas', 12), borderwidth=2, relief="groove",
            yscrollcommand=self.__scroll_espera.set
        )
        self.__lista_pedidos_espera.pack(side="left", fill="both", expand=True)
        self.__scroll_espera.config(command=self.__lista_pedidos_espera.yview)
        
        # Evento de doble click
        self.__lista_pedidos_espera.bind('<Double-Button-1>', self.seleccionar_e_ir2)


        # --- 3. SECCIÓN: BOTONES INFERIORES ---
        self.__frame_botones = tk.Frame(self, bg=BG_GENERAL)
        self.__frame_botones.grid(row=4, column=0, pady=20)

        self.__bot_borrar = tk.Button(self.__frame_botones, text="BORRAR SELECCIONADO", width=25, font=('Segoe UI', 12, 'bold'), 
                                      command=self.borrar_pedido_seleccionado, bg="#E74C3C", fg=FG_LIGHT, relief="flat", cursor="hand2")
        self.__bot_borrar.pack(side="left", padx=10)

        self.__bot_volver = tk.Button(self.__frame_botones, text="VOLVER", width=15, font=('Segoe UI', 12, 'bold'), 
                                      command=lambda: controller.show_frame("Pagina_Inicio"), bg=BG_ACCENT, fg=FG_LIGHT, relief="flat", cursor="hand2")
        self.__bot_volver.pack(side="left", padx=10)

    def borrar_pedido_seleccionado(self):
        """
        Obtiene el pedido seleccionado en la lista de espera y procede a eliminarlo.
        Si el pedido tiene una mesa asignada, libera la mesa y actualiza su estado.
        Finalmente, intenta eliminar el pedido de la base de datos y de la memoria.
        """
        seleccion = self.__lista_pedidos_espera.curselection()
        if seleccion:
            texto_completo = self.__lista_pedidos_espera.get(seleccion)
            numero_pedido = int(texto_completo.split('#')[1].split(',')[0])
            
            pedido_a_borrar = self.controller.pedidos.get(numero_pedido)
            if pedido_a_borrar:
                # Si el pedido tiene una mesa asignada, cambia su estado a libre en memoria y BD
                if pedido_a_borrar.mesa:
                    pedido_a_borrar.mesa.liberar_mesa()
                    bd.actualizar_mesa(pedido_a_borrar.mesa) 
            try:    
                # Intenta eliminar el registro de la base de datos y del diccionario del controlador
                bd.borrar_pedido(pedido_a_borrar)
                del self.controller.pedidos[numero_pedido]
                self.actualizar()
            except bd.sqlite3.IntegrityError:
                # Captura el error de integridad referencial de SQL si el pedido ya tiene productos
                messagebox.showerror('Error', 'No puedes borrar un pedido con productos')

    def actualizar(self):
        """
        Sincroniza la aplicación con la base de datos obteniendo los últimos pedidos.
        Limpia los listbox de la interfaz y redistribuye los pedidos en la lista de 
        espera (activos) o realizados (finalizados) según corresponda.
        """
        # Sincroniza el diccionario de pedidos con la base de datos
        self.controller.pedidos = bd.obtener_pedidos() 
        # Vacía por completo ambos listbox antes de repoblarlos
        self.__lista_pedidos_espera.delete(0, tk.END)
        self.__lista_pedidos_realizados.delete(0, tk.END)
        
        # Clasifica e inserta cada pedido en su lista correspondiente según su estado
        for pedido in self.controller.pedidos.values():
            texto = f"Pedido #{pedido.numero}, Numero: {pedido.numero_diario} - Mesa {pedido.mesa.numero}"
            if pedido.estado.lower() == 'activo':
                self.__lista_pedidos_espera.insert(tk.END, texto)
            else:
                self.__lista_pedidos_realizados.insert(tk.END, texto)

    def seleccionar_e_ir2(self, event):
        """
        Manejador de eventos que se dispara al interactuar con la lista de espera.
        Extrae el ID del pedido seleccionado, lo establece como el pedido activo 
        en el sistema junto a su mesa, y redirige a la pantalla de gestión de mesa.
        """
        seleccion = self.__lista_pedidos_espera.curselection()
        if seleccion:
            # Extrae el identificador numérico del pedido aislando el texto entre '#' y ','
            numero = int(self.__lista_pedidos_espera.get(seleccion).split('#')[1].split(',')[0])
            pedido_objeto = self.controller.pedidos[numero]
            
            # Asigna el contexto actual en el controlador global
            self.controller.pedido_actual = pedido_objeto
            self.controller.mesa_seleccionada = pedido_objeto.mesa
            
            # Cambia la vista de la interfaz a la pantalla de gestión
            self.controller.show_frame("Gestion_mesa")

class Ver_mesas(tk.Frame):
    """
    Pantalla que muestra un mapa visual interactivo de las mesas del restaurante.
    Permite ver el estado en tiempo real (libre u ocupada) y acceder a la gestión de cada una.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_GENERAL)
        self.controller = controller

        # --- CABECERA ---
        self.__label_mesas = tk.Label(self, text='Mapa de Mesas', font=("Segoe UI", 55, "italic"), bg=BG_GENERAL, fg=BG_ACCENT)
        self.__label_mesas.pack(pady=(80, 10))
        
        self.__label_subtitulo = tk.Label(self, text='Verde = Libre', font=("Segoe UI", 14, "bold"), fg="#41D41D", bg=BG_GENERAL)
        self.__label_subtitulo.pack(pady=(0, 5))

        self.__label_subtitulo2 = tk.Label(self, text= 'Rojo = Ocupada', font=("Segoe UI", 14, "bold"), fg="#EB0B0B", bg=BG_GENERAL)
        self.__label_subtitulo2.pack(pady=(0, 10))

        # --- CONTENEDOR DEL MAPA Y BOTONES ---
        self.__frame_mapa = tk.Frame(self, bg=BG_GENERAL)
        self.__frame_mapa.pack(pady=20)

        self.__bot_volver_mesas = tk.Button(self, text="VOLVER AL MENÚ", width=20, font=('Segoe UI', 14, 'bold'), command=lambda: controller.show_frame("Pagina_Inicio"), bg=BG_ACCENT, fg=FG_LIGHT, relief="flat")
        self.__bot_volver_mesas.pack(pady=40)

    def actualizar(self):
        """
        Sincroniza los datos de las mesas y pedidos con la base de datos y 
        redibuja la cuadrícula de botones para reflejar el estado actual del salón.
        """
        # Refrescamos diccionarios desde la BD
        self.controller.mesas = bd.obtener_mesas()
        self.controller.pedidos = bd.obtener_pedidos_activos()

        # Limpiamos los botones generados anteriormente para evitar superposiciones
        for widget in self.__frame_mapa.winfo_children():
            widget.destroy()

        columna, fila = 0, 0
        for mesa in self.controller.mesas.values():
            
            # Si es la mesa 0 (Barra), la ignoramos y no la dibujamos en el mapa del salón
            if int(mesa.numero) == 0:
                continue 
            
            # Asignamos el color dependiendo del estado de la mesa (Verde para libre, Rojo para cualquier otro)
            color_fondo = "#4CAF50" if mesa.estado.lower() == 'libre' else "#F44336"
            
            # Creamos el botón interactivo que representa físicamente a la mesa
            btn_mesa = tk.Button(
                self.__frame_mapa, 
                text=f"MESA {mesa.numero}\n\n{mesa.estado.upper()}\nCap: {mesa.capacidad}", 
                width=16, height=5, bg=color_fondo, fg="white",
                font=('Segoe UI', 11, 'bold'), relief="raised", cursor="hand2",
                command=lambda m=mesa: self.gestionar_click_mapa(m)
            )
            btn_mesa.grid(row=fila, column=columna, padx=15, pady=15)
            
            # Lógica para distribuir las mesas en una cuadrícula (máximo 6 columnas, del 0 al 5)
            columna += 1
            if columna > 5:
                columna = 0; fila += 1

    def gestionar_click_mapa(self, mesa):
        """
        Maneja la acción de pulsar sobre una mesa en el mapa. 
        Identifica si la mesa ya tiene un pedido en curso, actualiza el controlador 
        con este contexto y redirige a la vista de gestión.
        """
        # Establecemos la mesa seleccionada en el estado global de la app
        self.controller.mesa_seleccionada = mesa
        
        # Buscamos en el diccionario de pedidos si existe alguno activo asociado a esta mesa
        pedido_existente = next((p for p in self.controller.pedidos.values() 
                                 if p.mesa.numero == mesa.numero and p.estado.lower() == 'activo'), None)
        
        # Asignamos el pedido encontrado (o None si no hay) al estado global
        self.controller.pedido_actual = pedido_existente
        
        # Redirigimos al usuario a la pantalla para editar o abrir el pedido
        self.controller.show_frame("Gestion_mesa")

class Gestion_mesa(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FDF8F5") 
        self.controller = controller

        self.__label_ver_mesa = tk.Label(self, text='Detalles de la Mesa', font=FUENTE_TITULO, bg="#FDF8F5", fg=BG_ACCENT)
        self.__label_ver_mesa.pack(pady=(110,0))

        self.__frame_detalle_mesa = tk.Frame(self, bg="#FDF8F5")
        self.__frame_detalle_mesa.pack(pady=(40,5))

        label_style = {"font":('Segoe UI', 18), "bg":"#FDF8F5", "fg":FG_DARK}
        
        self.__label_numero_mesa_info = tk.Label(self.__frame_detalle_mesa, text='Número de mesa: ', **label_style)
        self.__label_numero_mesa_info.grid(row=0, column=0, sticky="e")

        self.__label_numero_mesa_text = tk.Label(self.__frame_detalle_mesa, font=('Segoe UI', 18, 'bold'), bg="#FDF8F5", fg=BG_ACCENT, width=15, anchor="w")
        self.__label_numero_mesa_text.grid(row=0, column=1, sticky="w")

        self.__label_estado_mesa_info = tk.Label(self.__frame_detalle_mesa, text='Estado actual: ', **label_style)
        self.__label_estado_mesa_info.grid(row=2, column=0, sticky="e")

        self.__label_estado_mesa_text = tk.Label(self.__frame_detalle_mesa, font=('Segoe UI', 18, 'bold'), bg="#FDF8F5", fg=FG_DARK, width=15, anchor="w")
        self.__label_estado_mesa_text.grid(row=2, column=1, sticky='w')

        self.__bot_ocupar_mesa = tk.Button(self.__frame_detalle_mesa, font=('Segoe UI', 14, 'bold'), width=20, bg=BG_BUTTON, fg=FG_LIGHT, command=self.cambiar_estado, relief="flat", cursor="hand2")
        self.__bot_ocupar_mesa.grid(row=3, columnspan=2, pady=30)

        self.__label_pedidos_mesa = tk.Label(self.__frame_detalle_mesa, text='Líneas del Pedido', font=("Segoe UI", 28, "italic"), bg="#FDF8F5", fg=BG_ACCENT)
        self.__label_pedidos_mesa.grid(row=4, columnspan=2, pady=(20, 10))

        # Creamos un frame que contendrá el listbox y el scrollbar
        self.__frame_lista_mesa = tk.Frame(self.__frame_detalle_mesa, bg="white", borderwidth=1, relief="groove")
        self.__frame_lista_mesa.grid(row=5, columnspan=2, sticky="ew")

        # Creamos y ubicamos el scrollbar a la derecha
        self.__scroll_mesa = tk.Scrollbar(self.__frame_lista_mesa, orient="vertical")
        self.__scroll_mesa.pack(side="right", fill="y")

        # Creamos el Listbox
        self.__lista_pedidos_mesa = tk.Listbox(
            self.__frame_lista_mesa, width=50, height=8, font=('Consolas', 11), 
            bg="white", fg=FG_DARK, relief="flat", borderwidth=0, 
            yscrollcommand=self.__scroll_mesa.set
        )
        self.__lista_pedidos_mesa.pack(side="left", fill="both", expand=True)
        
        # Vinculamos el scrollbar a la vista del listbox
        self.__scroll_mesa.config(command=self.__lista_pedidos_mesa.yview)

        
        self.__bot_anadir_linea_pedido = tk.Button(self.__frame_detalle_mesa, text='+ AÑADIR PRODUCTOS', width=30, font=('Segoe UI', 14, 'bold'), bg="#2ECC71", fg=FG_LIGHT, command=lambda: controller.show_frame("Anadir_linea_pedido"), relief="flat", cursor="hand2")
        self.__bot_anadir_linea_pedido.grid(row=6, columnspan=2, pady=20)

        self.__bot_finalizar_pedido = tk.Button(self.__frame_detalle_mesa, text='FINALIZAR Y COBRAR', width=30, font=('Segoe UI', 14, 'bold'), bg="#DE1212", fg=FG_LIGHT, command=self.cobrar_pedido, relief="flat", cursor="hand2")
        self.__bot_finalizar_pedido.grid(row=7, columnspan=2, pady=20)

        self.__bot_volver = tk.Button(self, text="VOLVER AL MAPA", width=20, font=('Segoe UI', 13, 'bold'), command=lambda: controller.show_frame("Ver_mesas"), bg=BG_ACCENT, fg=FG_LIGHT, relief="flat", cursor="hand2")
        self.__bot_volver.pack(pady=10)

    def cobrar_pedido(self):
        """Finaliza el pedido en base de datos, muestra el ticket y libera la mesa"""
        if self.controller.pedido_actual:
            # Lanzamos el Toplevel de la propina
            ventana_propina = VentanaPropina(self)
            self.wait_window(ventana_propina) 
            
            # Recogemos la propina que seleccionó el usuario
            propina_elegida = ventana_propina.propina_final
            
            # Se la asignamos al objeto pedido actual 
            self.controller.pedido_actual.propina = propina_elegida
            
            VentanaTicket(self, self.controller.pedido_actual)
            
            # Procesamos el cierre en la base de datos
            bd.transaccion_finalizar_y_cobrar_pedido(self.controller.pedido_actual)
            
            self.controller.pedido_actual = None
            self.controller.show_frame("Ver_mesas")

    def cambiar_estado(self):
        """Actualiza el estado en RAM y lo persiste en la BD"""
        mesa_actual = self.controller.mesa_seleccionada
        if mesa_actual:
            if mesa_actual.estado.lower() == 'libre': 
                mesa_actual.ocupar_mesa()
            else: 
                mesa_actual.liberar_mesa()
            
            bd.actualizar_mesa(mesa_actual)
            self.actualizar()
        
    def actualizar(self):
        mesa_actual = self.controller.mesa_seleccionada
        pedido_actual = self.controller.pedido_actual
        
        if mesa_actual:
            self.__label_numero_mesa_text.config(text=str(mesa_actual.numero))
            self.__label_estado_mesa_text.config(text=mesa_actual.estado.upper())
            self.__label_estado_mesa_text.config(fg="#E74C3C" if mesa_actual.estado.lower() == 'ocupada' else "#2ECC71")
            self.__bot_ocupar_mesa.config(text='LIBERAR MESA' if mesa_actual.estado == 'ocupada' else 'OCUPAR MESA')

            self.__lista_pedidos_mesa.delete(0, tk.END)
            
            # Ocultar botones si la mesa está libre o no hay pedido
            if pedido_actual and mesa_actual.estado.lower() == 'ocupada':
                self.__bot_finalizar_pedido.grid()
                for linea in pedido_actual.lineas_de_pedidos:
                    self.__lista_pedidos_mesa.insert(tk.END, f" • {linea.cantidad}x {linea.producto.nombre} - {linea.cantidad * linea.producto.precio:.2f}€")
            else:
                self.__bot_finalizar_pedido.grid_remove() # Ocultamos el botón de cobrar si no hay pedido

class Anadir_linea_pedido(tk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent, bg=BG_GENERAL)
        self.controller = controller
        self.lineas_temporales = {}

        #Reparto proporcional de pantalla
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(3, weight=1) # Da prioridad de estiramiento hacia abajo

        self.__label_producto = tk.Label(self, text='Seleccione Productos', font=("Segoe UI", 45, "italic"), bg=BG_GENERAL, fg=BG_ACCENT)
        self.__label_producto.grid(row=0, column=0, columnspan=2, pady=(20, 5))

        self.__label_mesa = tk.Label(self, font=("Segoe UI", 16, "bold"), fg="#777777", bg=BG_GENERAL)
        self.__label_mesa.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # --- FILTRO DE ALÉRGENOS ---
        self.__frame_filtros = tk.LabelFrame(self, text="FILTRO DE ALÉRGENOS (Marcar para OCULTAR) ", bg=BG_GENERAL, font=("Segoe UI", 10, "bold"))
        self.__frame_filtros.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")
        
        self.dict_variables_alergenos = {}
        for index, nombre in enumerate(ALERGENOS_UE):
            var = tk.BooleanVar(value=False)
            self.dict_variables_alergenos[nombre] = var
            chk = tk.Checkbutton(
                self.__frame_filtros, text=nombre, variable=var, bg=BG_GENERAL, 
                font=('Segoe UI', 10), cursor="hand2", command=self.dibujar_botones_carta
            )
            chk.grid(row=index//7, column=index%7, sticky="w", padx=15, pady=2)

        # --- CARTA Y TICKET ---
        self.__frame_carta = tk.LabelFrame(self, text=" CARTA ", bg=BG_GENERAL, font=("Segoe UI", 12, "bold"))
        self.__frame_carta.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        self.__frame_ticket = tk.LabelFrame(self, text=" TICKET ACTUAL ", bg="white", font=("Segoe UI", 12, "bold"))
        self.__frame_ticket.grid(row=3, column=1, padx=20, pady=10, sticky="nsew")

        self.__lbl_total_general = tk.Label(self.__frame_ticket, text="TOTAL: 0.00€", font=('Segoe UI', 20, 'bold'), bg="white", fg="#2E7D32")
        self.__lbl_total_general.pack(side="bottom", fill="x", padx=15, pady=15)

        self.__frame_acciones = tk.Frame(self, bg=BG_GENERAL)
        self.__frame_acciones.grid(row=4, column=0, columnspan=2, pady=20)

        self.__bot_guardar = tk.Button(self.__frame_acciones, text="GUARDAR CAMBIOS", width=25, font=('Segoe UI', 14, 'bold'), bg="#4CAF50", fg="white", command=self.guardar_lineas_en_pedido, relief="flat", cursor="hand2")
        self.__bot_guardar.grid(row=0, column=0, padx=10)

        self.__bot_volver = tk.Button(self.__frame_acciones, text="CANCELAR", width=15, font=('Segoe UI', 14, 'bold'), bg=BG_ACCENT, fg="white", command=self.cancelar_y_volver, relief="flat", cursor="hand2")
        self.__bot_volver.grid(row=0, column=1, padx=10)

    def producto_tiene_alergeno(self, producto, nombre_alergeno_buscar) -> bool:
        if isinstance(producto.alergenos, dict):
            lista_alergenos = producto.alergenos.values()
        else:
            lista_alergenos = producto.alergenos
        for alg in lista_alergenos:
            if alg.nombre.lower() == nombre_alergeno_buscar.lower():
                return True
        return False

    def actualizar(self):
        self.dibujar_botones_carta()
        self.cargar_pedido_en_pantalla()

    def cargar_pedido_en_pantalla(self):
        for item in self.lineas_temporales.values(): item["frame"].destroy()
        self.lineas_temporales.clear()
        
        if self.controller.mesa_seleccionada:
            self.__label_mesa['text'] = f'Editando Pedido - Mesa {self.controller.mesa_seleccionada.numero}'
        
        pedido_actual = self.controller.pedido_actual
        if pedido_actual and hasattr(pedido_actual, 'lineas_de_pedidos'):
            for linea in pedido_actual.lineas_de_pedidos:
                self.crear_fila_en_ticket(linea.producto, linea.cantidad)
        self.actualizar_total_general()

    def dibujar_botones_carta(self):
            for child in self.__frame_carta.winfo_children(): child.destroy()
            
            # --- Cálculo dinámico de filas ---
            total_productos = len(self.controller.productos.values())
            filas_necesarias = (total_productos + 3) // 4  
            
            for i in range(filas_necesarias): self.__frame_carta.grid_rowconfigure(i, weight=0)
            
            for i in range(4): self.__frame_carta.grid_columnconfigure(i, weight=1)
            
            alergenos_a_ocultar = [nombre for nombre, var in self.dict_variables_alergenos.items() if var.get()]
            
            col, fil = 0, 0
            for producto in self.controller.productos.values():
                if producto.disponibilidad.lower() != 'disponible': continue
                
                debe_ocultarse = any(self.producto_tiene_alergeno(producto, alg) for alg in alergenos_a_ocultar)
                if debe_ocultarse: continue

                if col == 0: self.__frame_carta.grid_rowconfigure(fil, weight=1)

                btn = tk.Button(self.__frame_carta, text=f"{producto.nombre}\n{producto.precio}€", bg="#F0EAD6", font=('Segoe UI', 10, 'bold'), command=lambda p=producto: self.pulsar_producto(p), relief="flat")
                btn.grid(row=fil, column=col, padx=8, pady=8, sticky="nsew")
                
                col += 1
                if col > 3:
                    col = 0
                    fil += 1

    def pulsar_producto(self, producto):
        if producto.codigo in self.lineas_temporales:
            var = self.lineas_temporales[producto.codigo]["variable_cantidad"]
            var.set(var.get() + 1)
            self.actualizar_precio_item(producto.codigo)
        else:
            self.crear_fila_en_ticket(producto, 1)
        self.actualizar_total_general()

    def crear_fila_en_ticket(self, producto, cantidad):
        f = tk.Frame(self.__frame_ticket, bg="white", pady=5)
        f.pack(fill="x", padx=10, before=self.__lbl_total_general)
        
        tk.Label(f, text=producto.nombre, width=30, anchor="w", bg="white", font=('Segoe UI', 11)).pack(side="left", fill="x", expand=True)
        
        var = tk.IntVar(value=cantidad)
        tk.Spinbox(f, from_=1, to=99, width=5, textvariable=var, command=lambda: self.actualizar_precio_item(producto.codigo)).pack(side="left", padx=10)
        lbl_p = tk.Label(f, text=f"{cantidad*producto.precio:.2f}€", width=8, anchor="e", bg="white", font=('Segoe UI', 11, 'bold'))
        lbl_p.pack(side="left")
        self.lineas_temporales[producto.codigo] = {"producto": producto, "variable_cantidad": var, "label_precio": lbl_p, "frame": f}

    def actualizar_precio_item(self, id_p):
        d = self.lineas_temporales[id_p]
        d["label_precio"].config(text=f"{d['variable_cantidad'].get()*d['producto'].precio:.2f}€")
        self.actualizar_total_general()

    def actualizar_total_general(self):
        t = sum(i["variable_cantidad"].get() * i["producto"].precio for i in self.lineas_temporales.values())
        self.__lbl_total_general.config(text=f"TOTAL: {t:.2f}€")

    def guardar_lineas_en_pedido(self):
        mesa = self.controller.mesa_seleccionada
        es_pedido_nuevo = False
        
        if self.controller.pedido_actual is None:
            nuevo_pedido = Pedido(mesa=mesa, estado='activo')
            self.controller.pedido_actual = nuevo_pedido
            es_pedido_nuevo = True

        p = self.controller.pedido_actual
        p.lineas_de_pedidos.clear() 

        for i in self.lineas_temporales.values():
            p.agregar_linea_pedido(p.numero, i["producto"], i["variable_cantidad"].get())

        if es_pedido_nuevo:
            bd.transaccion_abrir_pedido_nuevo(p)
            self.controller.pedidos[p.numero] = p
        else:
            bd.transaccion_actualizar_lineas_pedido(p)

        self.controller.show_frame("Gestion_mesa")

    def cancelar_y_volver(self):
        self.controller.show_frame("Gestion_mesa")

class Hacer_pedido(tk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent, bg=BG_GENERAL)
        self.controller = controller
        self.productos_venta = {}

        tk.Label(self, text='Caja Rápida / Barra', font=FUENTE_TITULO, bg=BG_GENERAL, fg=BG_ACCENT).pack(pady=(20, 10))

        # --- FILTRO DE ALÉRGENOS ---
        self.__frame_filtros = tk.LabelFrame(self, text=" FILTRO DE ALÉRGENOS (Marcar para OCULTAR) ", bg=BG_GENERAL, font=("Segoe UI", 10, "bold"))
        self.__frame_filtros.pack(fill="x", padx=20, pady=(0, 10))
        
        self.dict_variables_alergenos = {}
        fila_sup = tk.Frame(self.__frame_filtros, bg=BG_GENERAL)
        fila_sup.pack(fill="x")
        fila_inf = tk.Frame(self.__frame_filtros, bg=BG_GENERAL)
        fila_inf.pack(fill="x")

        for index, nombre in enumerate(ALERGENOS_UE):
            var = tk.BooleanVar(value=False)
            self.dict_variables_alergenos[nombre] = var
            padre = fila_sup if index < 7 else fila_inf
            chk = tk.Checkbutton(
                padre, text=nombre, variable=var, bg=BG_GENERAL, 
                font=('Segoe UI', 10), cursor="hand2", command=self.dibujar_carta
            )
            chk.pack(side="left", padx=15, pady=5)

        # --- CONTENEDOR PRINCIPAL CARTA / TICKET ---
        self.__main_container = tk.Frame(self, bg=BG_GENERAL)
        self.__main_container.pack(fill="both", expand=True, padx=20)

        self.__main_container.grid_columnconfigure(0, weight=3)
        self.__main_container.grid_columnconfigure(1, weight=2)
        self.__main_container.grid_rowconfigure(0, weight=1)

        self.__frame_izq = tk.LabelFrame(self.__main_container, text=" PRODUCTOS ", bg=BG_GENERAL, font=("Segoe UI", 12, "bold"))
        self.__frame_izq.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.__frame_der = tk.LabelFrame(self.__main_container, text=" TICKET ACTUAL ", bg="white", font=("Segoe UI", 12, "bold"))
        self.__frame_der.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.__lbl_total = tk.Label(self.__frame_der, text="TOTAL: 0.00€", font=('Segoe UI', 20, 'bold'), bg="white", fg="#2E7D32")
        self.__lbl_total.pack(side="bottom", fill="x", padx=15, pady=15)

        self.__ticket_list = tk.Frame(self.__frame_der, bg="white")
        self.__ticket_list.pack(fill="both", expand=True)

        self.__frame_btns = tk.Frame(self, bg=BG_GENERAL)
        self.__frame_btns.pack(fill="x", side="bottom", pady=20)

        self.__bot_cobrar = tk.Button(self.__frame_btns, text="COBRAR E IMPRIMIR", width=25, font=('Segoe UI', 14, 'bold'), bg="#2ECC71", fg="white", command=self.finalizar_venta, relief="flat", cursor="hand2")
        self.__bot_cobrar.pack(side="right", padx=50)

        self.__bot_cancelar = tk.Button(self.__frame_btns, text="CANCELAR", width=15, font=('Segoe UI', 14, 'bold'), bg=BG_ACCENT, fg="white", command=self.cancelar_venta, relief="flat", cursor="hand2")
        self.__bot_cancelar.pack(side="left", padx=50)

    def producto_tiene_alergeno(self, producto, nombre_alergeno_buscar) -> bool:
        if isinstance(producto.alergenos, dict):
            lista_alergenos = producto.alergenos.values()
        else:
            lista_alergenos = producto.alergenos
        for alg in lista_alergenos:
            if alg.nombre.lower() == nombre_alergeno_buscar.lower():
                return True
        return False

    def dibujar_carta(self):
        for child in self.__frame_izq.winfo_children(): child.destroy()
        
        # --- Cálculo dinámico de filas ---
        total_productos = len(self.controller.productos.values())
        filas_necesarias = (total_productos + 3) // 4  
            
        for i in range(filas_necesarias): self.__frame_izq.grid_rowconfigure(i, weight=0)
            
        for i in range(4): self.__frame_izq.grid_columnconfigure(i, weight=1)
        
        alergenos_a_ocultar = [nombre for nombre, var in self.dict_variables_alergenos.items() if var.get()]
        
        col, row = 0, 0
        for producto in self.controller.productos.values():
            if producto.disponibilidad.lower() != 'disponible': continue
            
            debe_ocultarse = any(self.producto_tiene_alergeno(producto, alg) for alg in alergenos_a_ocultar)
            if debe_ocultarse: continue
            
            if col == 0: self.__frame_izq.grid_rowconfigure(row, weight=1)
            
            btn = tk.Button(self.__frame_izq, text=f"{producto.nombre}\n{producto.precio}€", 
                            bg="#F0EAD6", font=('Segoe UI', 10, 'bold'),
                            command=lambda p=producto: self.anadir_al_ticket(p), relief="flat")
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            col += 1
            if col > 3: col=0; row+=1

    def anadir_al_ticket(self, producto):
        if producto.codigo in self.productos_venta:
            var = self.productos_venta[producto.codigo]["variable_cantidad"]
            var.set(var.get() + 1)
            self.actualizar_precio_item(producto.codigo)
        else:
            self.crear_fila_en_ticket(producto, 1)
        self.actualizar_total_general()

    def crear_fila_en_ticket(self, producto, cantidad):
        f = tk.Frame(self.__ticket_list, bg="white", pady=5)
        f.pack(fill="x", padx=10)
        
        # AJUSTE: Subimos 'width' a 30 aquí también para total consistencia
        tk.Label(f, text=producto.nombre, width=30, anchor="w", bg="white", font=('Segoe UI', 11)).pack(side="left", fill="x", expand=True)
        
        var = tk.IntVar(value=cantidad)
        tk.Spinbox(f, from_=1, to=99, width=5, textvariable=var, command=lambda: self.actualizar_precio_item(producto.codigo)).pack(side="left", padx=10)
        
        lbl_p = tk.Label(f, text=f"{cantidad*producto.precio:.2f}€", width=8, anchor="e", bg="white", font=('Segoe UI', 11, 'bold'))
        lbl_p.pack(side="left")
        
        self.productos_venta[producto.codigo] = {"producto": producto, "variable_cantidad": var, "label_precio": lbl_p, "frame": f}

    def actualizar_precio_item(self, id_p):
        d = self.productos_venta[id_p]
        d["label_precio"].config(text=f"{d['variable_cantidad'].get()*d['producto'].precio:.2f}€")
        self.actualizar_total_general()

    def actualizar_total_general(self):
        t = sum(i["variable_cantidad"].get() * i["producto"].precio for i in self.productos_venta.values())
        self.__lbl_total.config(text=f"TOTAL: {t:.2f}€")

    def finalizar_venta(self):
        if not self.productos_venta: return
        
        mesa_barra = self.controller.mesas.get(0)
        if not mesa_barra:
            mesa_barra = Mesa(numero=0, capacidad=0, estado="libre")
            self.controller.mesas[0] = mesa_barra

        nuevo_p = Pedido(mesa=mesa_barra, estado='activo')
        
        for item in self.productos_venta.values():
            nuevo_p.agregar_linea_pedido(nuevo_p.numero, item['producto'], item['variable_cantidad'].get())
        
        bd.transaccion_abrir_pedido_nuevo(nuevo_p)
        bd.transaccion_finalizar_y_cobrar_pedido(nuevo_p)

        VentanaTicket(self, nuevo_p)
        self.cancelar_venta()

    def cancelar_venta(self):
        for item in self.productos_venta.values(): item["frame"].destroy()
        self.productos_venta.clear()
        self.actualizar_total_general()
        
        for var in self.dict_variables_alergenos.values(): var.set(False)
        self.controller.show_frame("Pagina_Inicio")

    def actualizar(self):
        self.dibujar_carta()
        for item in self.productos_venta.values(): item["frame"].destroy()
        self.productos_venta.clear()
        self.actualizar_total_general()

class VentanaTicket(tk.Toplevel):
    """
    Es la clase que hace de ventana para mostrar el ticket al finalizar un pedido
    """
    def __init__(self, parent, pedido):
        super().__init__(parent)
        self.title("Simulación de Ticket Impreso")
        self.geometry("380x650") # Subido a 650 para dar espacio al desglose de propina
        self.configure(bg="#E0E0E0") 
        self.resizable(False, False)
        
        self.grab_set() 
        
        papel = tk.Frame(self, bg="white", bd=2, relief="groove", padx=20, pady=20)
        papel.pack(fill="both", expand=True, padx=20, pady=20)
        
        txt = tk.Text(papel, font=("Consolas", 10), bg="white", fg="black", bd=0, highlightthickness=0)
        txt.pack(fill="both", expand=True)
        

        #=======================
        #IMPRESIÓN DEL TICKET
        #=======================

        ticket_texto =  "      ***  MI RESTAURANTE ***       \n"
        ticket_texto += " \n    Calle de la Gastro, nº 12    \n"
        ticket_texto += "==================================\n"
        
        if pedido.mesa.numero == 0:
            ticket_texto += " ZONA: BARRA / CAJA RÁPIDA        \n"
        else:
            ticket_texto += f" ZONA: SALÓN - MESA {pedido.mesa.numero}\n"
            
        ticket_texto += "==================================\n"
        ticket_texto += "Cant   Producto            Total  \n"
        ticket_texto += "----------------------------------\n"
        
        subtotal_productos = 0
        for linea in pedido.lineas_de_pedidos:
            cant = linea.cantidad
            nombre = linea.producto.nombre
            precio_linea = cant * linea.producto.precio
            subtotal_productos += precio_linea
            
            nombre_corto = nombre[:17]
            item_str = f"{str(cant).ljust(4)}  {nombre_corto.ljust(18)} {precio_linea:>7.2f}€\n"
            ticket_texto += item_str
            
        ticket_texto += "----------------------------------\n"
        
        #LÓGICA DE  PROPINA ---
        propina = pedido.propina
        total_final = subtotal_productos + propina
        
        # Si el cliente dejó propina, mostramos el desglose completo
        if propina > 0:
            ticket_texto += f" SUBTOTAL:                {subtotal_productos:>7.2f}€\n"
            ticket_texto += f" PROPINA:                 {propina:>7.2f}€\n"
            ticket_texto += "----------------------------------\n"
            
        # El total a pagar siempre incluirá la propina calculada
        ticket_texto += f" TOTAL A PAGAR:           {total_final:>7.2f}€\n"
        # --------------------------------------------
        
        ticket_texto += "==================================\n"
        ticket_texto += "\n     ¡Gracias por su visita!      \n"
        ticket_texto += "       Le esperamos pronto        \n"
        
        txt.insert(tk.END, ticket_texto)
        txt.config(state="disabled") 
        
        #botón de aceptar
        btn_cerrar = tk.Button(
            self, text=" ENTENDIDO / IMPRIMIR", font=("Segoe UI", 11, "bold"), 
            bg="#2ECC71", fg="white", relief="flat", command=self.destroy, cursor="hand2"
        )
        btn_cerrar.pack(fill="x", padx=20, pady=(0, 20))

class VentanaPropina(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Pantalla del Cliente")
        self.geometry("400x300")
        self.configure(bg="#FDF8F5")
        self.resizable(False, False)
        
        # Bloquea la ventana principal hasta que esta se cierre
        self.transient(parent)
        self.grab_set()
        
        # Variable donde guardaremos el resultado final
        self.propina_final = 0

        tk.Label(
            self, text="¿Desea añadir una propina?", 
            font=("Segoe UI", 18, "bold"), bg="#FDF8F5", fg=BG_ACCENT
        ).pack(pady=(30, 10))

        tk.Label(
            self, text="Deslice para seleccionar la cantidad:", 
            font=("Segoe UI", 11), bg="#FDF8F5", fg=FG_DARK
        ).pack()

        # El selector de propina
        self.scale_p = tk.Scale(
            self, from_=0, to=100, orient="horizontal", length=250,
            font=('Segoe UI', 12, 'bold'), bg="#FDF8F5", fg=FG_DARK,
            troughcolor="white", activebackground=BG_ACCENT
        )
        self.scale_p.pack(pady=20)

        # Botón para confirmar
        tk.Button(
            self, text="CONFIRMAR Y PAGAR", font=('Segoe UI', 12, 'bold'),
            bg="#2ECC71", fg=FG_LIGHT, relief="flat", cursor="hand2",
            command=self.aceptar
        ).pack(pady=10)

    def aceptar(self):
        # Guardamos el valor en el atributo antes de destruir la ventana
        self.propina_final = self.scale_p.get()
        self.destroy()

class Panel_Administrador(tk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent, bg=controller.BG_GENERAL if hasattr(controller, 'BG_GENERAL') else "#F5F5F5")
        self.controller = controller
        
        self.bg_general = controller.BG_GENERAL if hasattr(controller, 'BG_GENERAL') else "#F5F5F5"
        self.bg_accent = controller.BG_ACCENT if hasattr(controller, 'BG_ACCENT') else "#333333"

        # Título Principal
        tk.Label(self, text='Panel de Administración', font=("Segoe UI", 32, "bold"), bg=self.bg_general, fg=self.bg_accent).pack(pady=10)

        # Contenedor de Pestañas (Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # Crear los frames para cada pestaña
        self.tab_productos = tk.Frame(self.notebook, bg=self.bg_general)
        self.tab_mesas = tk.Frame(self.notebook, bg=self.bg_general)

        self.notebook.add(self.tab_productos, text=" GESTIÓN DE CARTA ")
        self.notebook.add(self.tab_mesas, text=" GESTIÓN DE MESAS ")

        # Inicializar los componentes de cada pestaña
        self.init_tab_productos()
        self.init_tab_mesas()

        # Botón Volver al Menú Principal
        btn_volver = tk.Button(self, text="⬅ VOLVER AL INICIO", font=('Segoe UI', 12, 'bold'), 
                               bg=self.bg_accent, fg="white", 
                               command=lambda: self.controller.show_frame("Pagina_Inicio"), 
                               relief="flat", cursor="hand2", padx=20, pady=5)
        btn_volver.pack(side="bottom", pady=15)

    def actualizar(self):
        self.refrescar_tabla_productos()
        self.refrescar_tabla_mesas()

    # =========================================================================
    # PESTAÑA: GESTIÓN DE PRODUCTOS (CARTA)
    # =========================================================================
    def init_tab_productos(self):
        frame_tabla = tk.Frame(self.tab_productos, bg=self.bg_general)
        frame_tabla.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # --- COLUMNAS ---
        self.tree_productos = ttk.Treeview(frame_tabla, columns=("Nombre", "Precio", "Estado", "Alergenos"), show="headings")
        self.tree_productos.heading("Nombre", text="Producto")
        self.tree_productos.heading("Precio", text="Precio")
        self.tree_productos.heading("Estado", text="Estado")
        self.tree_productos.heading("Alergenos", text="Alérgenos")

        # Ajuste de anchos
        self.tree_productos.column("Nombre", minwidth=240)
        self.tree_productos.column("Precio", minwidth=50, anchor="center")
        self.tree_productos.column("Estado", minwidth=100, anchor="center")
        self.tree_productos.column("Alergenos", width=350, minwidth=200, anchor="w") 
        
        self.tree_productos.pack(fill="both", expand=True)

        frame_btns = tk.Frame(self.tab_productos, bg=self.bg_general)
        frame_btns.pack(side="right", fill="y", padx=10, pady=10)

        tk.Button(frame_btns, text="+ AÑADIR PRODUCTO", bg="#4CAF50", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", command=self.ventana_anadir_producto, cursor="hand2").pack(fill="x", pady=5)
        tk.Button(frame_btns, text=" MODIFICAR PRODUCTO", bg="#F39C12", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", command=self.cambiar_precio_producto, cursor="hand2").pack(fill="x", pady=5)
        tk.Button(frame_btns, text=" ALTERNAR ESTADO\n(Disponible/Agotado)", bg="#2980B9", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", command=self.alternar_estado_producto, cursor="hand2").pack(fill="x", pady=5)

    def refrescar_tabla_productos(self):
        """
        Limpia y rellena la tabla incluyendo la nueva columna de alérgenos
        """
        for item in self.tree_productos.get_children(): 
            self.tree_productos.delete(item)
            
        for p in self.controller.productos.values():
            # Extraer nombres de alérgenos según el formato del objeto (dict o lista)
            if isinstance(p.alergenos, dict):
                nombres = [a.nombre for a in p.alergenos.values()]
            else:
                nombres = [a.nombre for a in p.alergenos]
            
            cadena_alergenos = ", ".join(nombres) if nombres else "Sin alérgenos"
            
            self.tree_productos.insert("", "end", iid=p.codigo, values=(
                p.nombre, 
                f"{p.precio:.2f}€", 
                p.disponibilidad.upper(),
                cadena_alergenos # Cuarta columna
            ))

    #cambiar el precio de un producto seleccionado
    def cambiar_precio_producto(self):
        selected = self.tree_productos.selection()
        if not selected:
            messagebox.showwarning("Atención", "Por favor, selecciona un producto de la lista.")
            return
        
        codigo_p = int(selected[0])
        producto = self.controller.productos[codigo_p]
        
        # Crear ventana de edición
        v = tk.Toplevel(self)
        v.title(f"Editar Producto: {producto.nombre}")
        v.geometry("500x700")
        v.grab_set()
        v.configure(bg=BG_GENERAL)

        # Campo de Precio
        tk.Label(v, text=f"Modificar precio de '{producto.nombre}':", bg=BG_GENERAL, font=("Segoe UI", 10, "bold")).pack(pady=(15, 5))
        entry_pre = tk.Entry(v, font=("Segoe UI", 11))
        entry_pre.insert(0, str(producto.precio))
        entry_pre.pack(fill="x", padx=40)

        # Panel de Alérgenos
        frame_al = tk.LabelFrame(v, text=" Alérgenos del Producto ", bg=BG_GENERAL)
        frame_al.pack(fill="both", expand=True, padx=20, pady=20)

        # Cargamos todos los alérgenos disponibles en la BD
        alergenos_db = bd.obtener_alergenos()
        
        vars_al = {} 
        for idx, (id_al, obj_al) in enumerate(alergenos_db.items()):
            var = tk.BooleanVar()
            
            # MARCAR SI EL PRODUCTO YA LO TIENE:
            # Comprobamos si el ID del alérgeno está en el diccionario del producto
            if id_al in producto.alergenos:
                var.set(True)
            
            vars_al[id_al] = var
            tk.Checkbutton(frame_al, text=obj_al.nombre, variable=var, bg=BG_GENERAL).grid(row=idx//2, column=idx%2, sticky="w", padx=10)

        # Lógica de Guardado
        def guardar_cambios():
            try:
                # Validar nuevo precio
                nuevo_precio = float(entry_pre.get().replace(',', '.'))
                
                # Recolectar nuevos alérgenos seleccionados
                nuevos_alergenos = {}
                for id_al, variable in vars_al.items():
                    if variable.get():
                        nuevos_alergenos[id_al] = alergenos_db[id_al]

                # Guardar valores antiguos por si falla la BD
                precio_antiguo = producto.precio
                alergenos_antiguos = producto.alergenos.copy()

                # Actualizar objeto temporalmente
                producto.precio = nuevo_precio
                producto.alergenos = nuevos_alergenos

                # GUARDAR EN BASE DE DATOS
                # Esta función debe borrar los antiguos en la tabla intermedia y meter los nuevos
                bd.transaccion_modificar_producto_con_alergenos(producto)
                
                self.refrescar_tabla_productos()
                v.destroy()
                messagebox.showinfo("Éxito", "Producto actualizado correctamente.")

            except ValueError:
                messagebox.showerror("Error", "El precio no es válido.")
            except Exception as e:
                # Si falla la BD, revertimos los cambios en el objeto de memoria
                producto.precio = precio_antiguo
                producto.alergenos = alergenos_antiguos
                messagebox.showerror("Error", f"No se pudo actualizar: {e}")

        tk.Button(v, text=" GUARDAR CAMBIOS", bg=BG_ACCENT, fg="white", 
                  font=("Segoe UI", 12, "bold"), command=guardar_cambios, pady=10).pack(fill="x", padx=40, pady=20)


    # Cambiamos el estado de un producto('DISPONIBLE'|'NO DISPONIBLE')
    def alternar_estado_producto(self):
        selected = self.tree_productos.selection()
        if not selected:
            messagebox.showwarning("Atención", "Por favor, selecciona un producto de la lista.")
            return
        
        codigo_p = int(selected[0])
        producto = self.controller.productos[codigo_p]
        
        nuevo_estado = "No Disponible" if producto.disponibilidad.lower() == "disponible" else "Disponible"
        producto.disponibilidad = nuevo_estado
        
        try:
            bd.transaccion_modificar_producto_con_alergenos(producto)
            self.refrescar_tabla_productos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la BD: {e}")
            producto.disponibilidad = "Disponible" if nuevo_estado == "No Disponible" else "No Disponible"

    # Ventana donde se puede añadir un nuevo producto
    def ventana_anadir_producto(self):
        v = tk.Toplevel(self)
        v.title("Nuevo Producto")
        v.geometry("500x700")
        v.grab_set()
        v.configure(bg=BG_GENERAL)

        tk.Label(v, text="Nombre del Producto:", bg=BG_GENERAL, font=("Segoe UI", 10, "bold")).pack(pady=5)
        entry_nom = tk.Entry(v, font=("Segoe UI", 11))
        entry_nom.pack(fill="x", padx=40)

        tk.Label(v, text="Precio (€):", bg=BG_GENERAL, font=("Segoe UI", 10, "bold")).pack(pady=5)
        entry_pre = tk.Entry(v, font=("Segoe UI", 11))
        entry_pre.pack(fill="x", padx=40)

        frame_al = tk.LabelFrame(v, text=" Seleccionar Alérgenos ", bg=BG_GENERAL)
        frame_al.pack(fill="both", expand=True, padx=20, pady=10)

        # CARGAR ALÉRGENOS REALES DE LA BD
        alergenos_db = bd.obtener_alergenos()
        
        vars_al = {} # Aquí guardamos los Checkbuttons
        for idx, (id_al, obj_al) in enumerate(alergenos_db.items()):
            var = tk.BooleanVar()
            vars_al[id_al] = var # Guardamos la variable usando el ID como clave
            tk.Checkbutton(frame_al, text=obj_al.nombre, variable=var, bg=BG_GENERAL).grid(row=idx//2, column=idx%2, sticky="w", padx=10)

        def guardar():
            nombre = entry_nom.get().strip()
            try:
                precio = float(entry_pre.get().replace(',', '.'))
                if not nombre: raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Revisa el nombre y el precio (usa punto para decimales)")
                return

            # RECOLECTAMOS LOS IDS DE LOS MARCADOS
            alergenos_seleccionados = {}
            for id_al, variable in vars_al.items():
                if variable.get():
                    alergenos_seleccionados[id_al] = alergenos_db[id_al]

            # CREAMOS EL OBJETO PRODUCTO
            nuevo_p = Producto(codigo=0, nombre=nombre, precio=precio, 
                               disponibilidad="disponible", alergenos=alergenos_seleccionados)

            try:
                # CREACIÓN REAL EN BD
                bd.transaccion_crear_producto_con_alergenos(nuevo_p)
                
                # ACTUALIZACIÓN DE LA APP EN VIVO
                self.controller.productos[nuevo_p.codigo] = nuevo_p
                self.refrescar_tabla_productos()
                
                v.destroy()
                messagebox.showinfo("Éxito", f"Producto '{nombre}' creado con sus alérgenos.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(v, text="GUARDAR PRODUCTO", bg=BG_ACCENT, fg="white", 
                  font=("Segoe UI", 12, "bold"), command=guardar, pady=10).pack(fill="x", padx=40, pady=20)
        
    # =========================================================================
    # PESTAÑA: GESTIÓN DE MESAS
    # =========================================================================
    def init_tab_mesas(self):
        frame_tabla = tk.Frame(self.tab_mesas, bg=self.bg_general)
        frame_tabla.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Columnas 
        self.tree_mesas = ttk.Treeview(frame_tabla, columns=("Numero", "Capacidad", "Estado"), show="headings")
        self.tree_mesas.heading("Numero", text="Número de Mesa")
        self.tree_mesas.heading("Capacidad", text="Capacidad")
        self.tree_mesas.heading("Estado", text="Estado Actual")

        # Ajuste de anchos
        self.tree_mesas.column("Numero", minwidth=120, anchor="center")
        self.tree_mesas.column("Capacidad", minwidth=80, anchor="center")
        self.tree_mesas.column("Estado", minwidth=100, anchor="center")

        self.tree_mesas.pack(fill="both", expand=True)

        frame_btns = tk.Frame(self.tab_mesas, bg=self.bg_general)
        frame_btns.pack(side="right", fill="y", padx=10, pady=10)

        #BOTONES AJUSTE MESAS
        tk.Button(frame_btns, text=" + AÑADIR MESA", bg="#4CAF50", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", command=self.anadir_mesa, cursor="hand2").pack(fill="x", pady=5)
        tk.Button(frame_btns, text=" CAMBIAR CAPACIDAD", bg="#F39C12", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", command=self.cambiar_capacidad_mesa, cursor="hand2").pack(fill="x", pady=5)
        tk.Button(frame_btns, text=" ELIMINAR MESA", bg="#E74C3C", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", command=self.eliminar_mesa, cursor="hand2").pack(fill="x", pady=5)

    def refrescar_tabla_mesas(self):
        for item in self.tree_mesas.get_children(): self.tree_mesas.delete(item)
        for m in self.controller.mesas.values():
            if m.numero == 0: continue
            self.tree_mesas.insert("", "end", iid=m.numero, values=(f"Mesa {m.numero}", m.capacidad, m.estado.upper()))

    #Cambiamos la capacidad de una mesa ya creada
    def cambiar_capacidad_mesa(self):
        selected = self.tree_mesas.selection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona qué mesa deseas modificar.")
            return
        
        num_mesa = int(selected[0])
        mesa = self.controller.mesas[num_mesa]
        
        nueva_capacidad = simpledialog.askinteger("Modificar Capacidad", f"Introduce la capacidad para la Mesa {mesa.numero}:", initialvalue=mesa.capacidad, minvalue=1)
        
        #se comprueba que la nueva capacidad sea correcta
        if nueva_capacidad is not None:
            capacidad_anterior = mesa.capacidad
            mesa.capacidad = nueva_capacidad
            try:
                bd.actualizar_mesa(mesa) 
                self.refrescar_tabla_mesas()
                messagebox.showinfo("Éxito", f"Capacidad de la Mesa {mesa.numero} cambiada a {nueva_capacidad} personas.")
            except Exception as e:
                mesa.capacidad = capacidad_anterior 
                messagebox.showerror("Error", f"No se pudo guardar la nueva capacidad: {e}")

    #se añade una nueva mesa
    def anadir_mesa(self):
        nueva_m = Mesa(numero=0, capacidad=4, estado="libre")
        try:
            bd.insertar_mesa(nueva_m)
            self.controller.mesas[nueva_m.numero] = nueva_m
            self.refrescar_tabla_mesas()
            messagebox.showinfo("Éxito", f"Se ha añadido la Mesa {nueva_m.numero} correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al crear la mesa: {e}")

    #se elimina la mesa seleccionada si hay alguna seleccionada
    def eliminar_mesa(self):
        selected = self.tree_mesas.selection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona qué mesa deseas eliminar.")
            return
        
        num_mesa = int(selected[0])
        mesa = self.controller.mesas[num_mesa]
        
        if mesa.estado.lower() != "libre":
            messagebox.showerror("Error", "No puedes eliminar una mesa que está ocupada o editándose.")
            return

        if messagebox.askyesno("Confirmar", f"¿Seguro que quieres eliminar definitivamente la Mesa {num_mesa}?"):
            try:
                bd.borrar_mesa(mesa)
                del self.controller.mesas[num_mesa]
                self.refrescar_tabla_mesas()
                messagebox.showinfo("Éxito", "Mesa eliminada correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la mesa: {e}")
                
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()