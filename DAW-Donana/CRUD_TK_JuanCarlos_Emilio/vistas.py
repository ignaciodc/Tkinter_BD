import tkinter as tk
from tkinter import ttk, messagebox
from modelo import Database, Departamento, Aula, Docente, Alumno, Modulo, Matricula

bd = Database()

#Función genérica de los Botones
def btn(padre, texto, comando):
    boton = tk.Button(padre, text=str(texto), command=comando, font=("Roboto", 20), activebackground="#797B76", activeforeground="#FFFFFF", bg="#444240", fg="#FFFFFF",
            padx=20, pady=10, relief="flat")
    return boton

#Función genérica de los Label
def lbl(padre, nombre, texto):
    nombre = tk.Label(padre, text=texto, font=("Roboto", 16), bg="#262323", fg="#FFFFFF").pack(padx=20, pady=20)
    return nombre


class PantallaPrincipal(tk.Frame):
    def __init__(self, contenedor):
        super().__init__(contenedor)
        self.configure(bg="#262323")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Roboto", 10))
        style.configure("TNotebook.Tab", font=("Roboto", 10), padding=[10, 4])
        
        style = ttk.Style()
        style.configure("TNotebook.Tab", 
            font=("Segoe UI", 10),
            background="#262323",
            foreground="#FFFFFF"
        )
       

        tk.Label(self, text="🏫 Instituto", 
            font=("Roboto", 20, "bold"), fg="#FFFFFF", bg="#262323").pack(pady=6)
        
        tk.Label(self, text='PANTALLA PRINCIPAL',font=("Roboto", 14), fg="#FEFAE3", bg="#262323").pack(pady=6)
        
        
        
        # Creación de Notebook
        # ----------------------------
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        # Crear Frames para cada clase 
        # ----------------------------

        style = ttk.Style()
        style.configure("MiFrame.TFrame", background="#262323")
        
        alumno       = ttk.Frame(notebook, style="MiFrame.TFrame")
        docente      = ttk.Frame(notebook, style="MiFrame.TFrame")
        departamento = ttk.Frame(notebook, style="MiFrame.TFrame")
        aula         = ttk.Frame(notebook, style="MiFrame.TFrame")
        modulo       = ttk.Frame(notebook, style="MiFrame.TFrame")
        matricula    = ttk.Frame(notebook, style="MiFrame.TFrame")
        
        # Añadir las pestañas al Notebook
        # -------------------------------
        notebook.add(alumno,       text="Alumnos")
        notebook.add(docente,      text="Docentes")
        notebook.add(departamento, text="Departamentos")
        notebook.add(aula,         text="Aula")
        notebook.add(modulo,       text="Módulo")
        notebook.add(matricula,    text="Matricula")
        

        # Labels de cada pestaña
        # ----------------------
        # ALUMNO
        lbl(alumno,'label_alumnos', "Lista de Alumnos")

        # DOCENTE
        lbl(docente,'label_docente', "Lista de Docentes")
        
        # DEPARTAMENTO
        lbl(departamento,'label_departamento', "Lista de Departamentos")

        # AULA
        lbl(aula, 'lista_aulas',"Lista de Aulas" )

        # MÓDULO
        lbl(modulo, 'label_modulo', 'Lista de Módulos')

        # MATRÍCULA
        lbl(matricula, 'label_matr', 'Lista de Matrículas')

        # Configuración pestañas 
        # ---------------------
        ESTILOS_LISTAS = {
        "font": ("Courier New", 13),   # ← cambia "sans-serif" por esto
        "selectbackground": "blue",
        "selectforeground": "#FEFAE3",
        "background": "#FEFAE3",
        "foreground": "black"
    }
        
        # ALUMNO   
        # Frame donde se guardan los botones de ALUMNOS
        botones_alumno = tk.Frame(alumno, bg="#262323")
        botones_alumno.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        # Botones ALUMNOS
        btn(botones_alumno, 'Insertar', self.insertar_alumno).pack(side=tk.LEFT, padx=10)
        btn(botones_alumno, 'Modificar',self.modificar_alumno).pack(side=tk.LEFT, padx=10)
        btn(botones_alumno, 'Eliminar', self.eliminar_alumno).pack(side=tk.LEFT, padx=10)
        btn(botones_alumno, 'Cargar', self.cargar_todo).pack(side=tk.RIGHT, padx=12, pady=10)
        btn(botones_alumno, "Cerrar Aplicación", self.quit).pack(side=tk.RIGHT , padx=12, pady=5)
        
        # Listbox y Scrollbar ALUMNOS 
        self.lista_alu = tk.Listbox(alumno, **ESTILOS_LISTAS)
        
        scroll = ttk.Scrollbar(alumno, orient=tk.VERTICAL, command=self.lista_alu.yview)
        self.lista_alu.config(yscrollcommand=scroll.set)
        
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_alu.pack(expand=True, fill='both', side=tk.LEFT)

        self.cargar_alumnos()
        
        # DOCENTE
        # Frame donde se guardan los botones de DOCENTE
        botones_docente = tk.Frame(docente, bg="#262323")
        botones_docente.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        # Botones de DOCENTE
        btn(botones_docente, 'Insertar', self.insertar_docente).pack(side=tk.LEFT, padx=10)
        btn(botones_docente, 'Modificar', self.modificar_docente).pack(side=tk.LEFT, padx=10)
        btn(botones_docente, 'Eliminar', self.eliminar_docente).pack(side=tk.LEFT, padx=10)
        btn(botones_docente, 'Cargar', self.cargar_todo).pack(side=tk.RIGHT, padx=12, pady=10)
        btn(botones_docente, "Cerrar Aplicación", self.quit).pack(side=tk.RIGHT , padx=12, pady=5)
        
        # Listbox y Scrollbar DOCENTE 
        self.lista_doc = tk.Listbox(docente, **ESTILOS_LISTAS)
        
        scroll_doc = ttk.Scrollbar(docente, orient=tk.VERTICAL, command=self.lista_doc.yview)
        self.lista_doc.config(yscrollcommand=scroll_doc.set)
        
        scroll_doc.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_doc.pack(expand=True, fill='both', side=tk.LEFT)

        self.cargar_docentes()

        # DEPARTAMENTO
        # Frame donde se guardan los botones de DEPA, bg="#636B3F", bg="#636B3F"RTAMENTO
        botones_departamento = tk.Frame(departamento , bg="#262323")
        botones_departamento.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        # Botones de DEPARTAMENTO
        btn(botones_departamento, 'Insertar', self.insertar_departamento).pack(side=tk.LEFT, padx=10)
        btn(botones_departamento, 'Modificar', self.modificar_departamento).pack(side=tk.LEFT, padx=10)
        btn(botones_departamento, 'Eliminar', self.eliminar_departamento).pack(side=tk.LEFT, padx=10)
        btn(botones_departamento, 'Cargar', self.cargar_todo).pack(side=tk.RIGHT, padx=12, pady=10)
        btn(botones_departamento, "Cerrar Aplicación", self.quit).pack(side=tk.RIGHT , padx=12, pady=5)
        
        # Listbox y Scrollbar DEPARTAMENTO
        self.lista_depto = tk.Listbox(departamento, **ESTILOS_LISTAS)
        
        scroll_depto = ttk.Scrollbar(departamento, orient=tk.VERTICAL, command=self.lista_depto.yview)
        self.lista_depto.config(yscrollcommand=scroll_depto.set)
        
        scroll_depto.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_depto.pack(expand=True, fill='both', side=tk.LEFT)

        self.cargar_departamentos()

        # AULA
         # Frame donde se guardan los, bg="#636B3F", bg="#636B3F" botones de AULA
        botones_aula = tk.Frame(aula , bg="#262323")
        botones_aula.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        # Botones de AULA
        btn(botones_aula, 'Insertar', self.insertar_aula).pack(side=tk.LEFT, padx=10)
        btn(botones_aula, 'Modificar', self.modificar_aula).pack(side=tk.LEFT, padx=10)
        btn(botones_aula, 'Cargar', self.cargar_todo).pack(side=tk.RIGHT, padx=12, pady=10)
        btn(botones_aula, "Cerrar Aplicación", self.quit).pack(side=tk.RIGHT , padx=12, pady=5)
        
        # Listbox y Scrollbar AULA
        self.lista_aula = tk.Listbox(aula, **ESTILOS_LISTAS)
        
        scroll_aula = ttk.Scrollbar(aula, orient=tk.VERTICAL, command=self.lista_aula.yview)
        self.lista_aula.config(yscrollcommand=scroll_aula.set)
        
        scroll_aula.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_aula.pack(expand=True, fill='both', side=tk.LEFT)

        self.cargar_aulas()
        
        # MÓDULO
        # Frame donde se guardan los bot, bg="#636B3F"ones de MÓDULO
        botones_modulo = tk.Frame(modulo, bg="#262323")
        botones_modulo.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        btn(botones_modulo, 'Insertar', self.insertar_modulo).pack(side=tk.LEFT, padx=10)
        btn(botones_modulo, 'Modificar', self.modificar_modulo).pack(side=tk.LEFT, padx=10)
        btn(botones_modulo, 'Eliminar', self.eliminar_modulo).pack(side=tk.LEFT, padx=10)
        btn(botones_modulo, 'Cargar', self.cargar_todo).pack(side=tk.RIGHT, padx=12, pady=10)
        btn(botones_modulo, "Cerrar Aplicación", self.quit).pack(side=tk.RIGHT , padx=12, pady=5)

        # Listbox y Scrollbar MÓDULO
        self.lista_modulo = tk.Listbox(modulo, **ESTILOS_LISTAS)
        
        scroll_modulo = ttk.Scrollbar(modulo, orient=tk.VERTICAL, command=self.lista_modulo.yview)
        self.lista_modulo.config(yscrollcommand=scroll_modulo.set)
        
        scroll_modulo.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_modulo.pack(expand=True, fill='both', side=tk.LEFT)

        self.cargar_modulos()


        # Frame donde se guardan los botones de MATRÍCULA     
        botones_matr = tk.Frame(matricula, bg='#262323')
        botones_matr.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        btn(botones_matr, 'Insertar', self.insertar_matricula).pack(side=tk.LEFT, padx=10)
        btn(botones_matr, 'Eliminar', self.eliminar_matricula).pack(side=tk.LEFT, padx=10)
        btn(botones_matr, 'Cargar', self.cargar_todo).pack(side=tk.RIGHT, padx=12, pady=10)
        btn(botones_matr, "Cerrar Aplicación", self.quit).pack(side=tk.RIGHT , padx=12, pady=5)

        self.lista_matr = tk.Listbox(matricula, **ESTILOS_LISTAS)
        
        scroll_matr = ttk.Scrollbar(matricula, orient=tk.VERTICAL, command=self.lista_matr.yview)
        self.lista_matr.config(yscrollcommand=scroll_matr.set)
        
        scroll_matr.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_matr.pack(expand=True, fill='both', side=tk.LEFT)

        self.cargar_matriculas()
        
           
#=============================#
#  CARGAR LAS BASES DE DATOS  #
#=============================#

    # ALUMNO
    def cargar_alumnos(self):
        self.lista_alu.delete(0, tk.END)
        for fila in Alumno.obtener_todos(bd):
            email = fila['email'] or "—"
            linea = (
                f"  #{fila['id']:<4} "
                f"{'👤 ' + fila['nombre'] + ' ' + fila['apellidos']:<36} "
                f"{'🪪 ' + fila['dni']:<16} "
                f"✉️  {email}"
            )
            self.lista_alu.insert(tk.END, linea)

    # DOCENTE
    def cargar_docentes(self):
        self.lista_doc.delete(0, tk.END)
        for fila in Docente.obtener_todos(bd):
            email  = fila['email'] or "—"
            depto  = f"Depto. {fila['id_depto']}" if fila['id_depto'] else "Sin depto."
            linea = (
                f"  #{fila['id']:<4} "
                f"{'🧑‍🏫 ' + fila['nombre'] + ' ' + fila['apellidos']:<36} "
                f"{'✉️  ' + email:<38} "
                f"🏢 {depto}"
            )
            self.lista_doc.insert(tk.END, linea)

    # DEPARTAMENTO
    def cargar_departamentos(self):
        self.lista_depto.delete(0, tk.END)
        for fila in Departamento.obtener_todos(bd):
            linea = (
                f"  #{fila['id']:<4} "
                f"🏢 {fila['nombre']}"
            )
            self.lista_depto.insert(tk.END, linea)

    # AULA
    def cargar_aulas(self):
        self.lista_aula.delete(0, tk.END)
        plantas = {0: "Planta baja", 1: "1ª planta", 2: "2ª planta", 3: "3ª planta"}
        for fila in Aula.obtener_todos(bd):
            planta_txt = plantas.get(fila['planta'], f"Planta {fila['planta']}")
            linea = (
                f"  #{fila['id']:<4} "
                f"{'🚪 ' + fila['nombre']:<32} "
                f"🏗️  {planta_txt}"
            )
            self.lista_aula.insert(tk.END, linea)

    # MÓDULO
    def cargar_modulos(self):
        self.lista_modulo.delete(0, tk.END)
        for fila in Modulo.obtener_todos(bd):
            docente = f"Doc.#{fila['id_docente']}" if fila['id_docente'] else "Sin docente"
            aula    = f"Aula #{fila['id_aula']}"   if fila['id_aula']    else "Sin aula"
            linea = (
                f"  #{fila['id']:<4} "
                f"{'📚 ' + fila['nombre']:<44} "
                f"{'🔖 ' + (fila['codigo'] or '—'):<12} "
                f"{fila['horas']:>3}h   "
                f"{docente:<14} "
                f"🚪 {aula}"
            )
            self.lista_modulo.insert(tk.END, linea)

    #MATRICULA
    def cargar_matriculas(self):
        self.lista_matr.delete(0, tk.END)
        for fila in Matricula.obtener_todos(bd):
            linea = (
                f"  {fila['id_alumno']:>3},{fila['id_modulo']:<4} "   # IDs ocultos al inicio
                f"{'👤 ' + fila['alumno']:<38} "
                f"📚 {fila['modulo']}"
            )
            self.lista_matr.insert(tk.END, linea)
    
        # TODOS
    
    def cargar_todo(self):
        self.cargar_alumnos
        self.cargar_aulas
        self.cargar_departamentos
        self.cargar_docentes
        self.cargar_matriculas
        self.cargar_modulos
    
#========================#
#  FUNCIONES   BOTONES   #
#========================#

# ESQUEMA PARA TODOS LOS INSERTAR, MODIFICAR, ELIMINAR:
# SE ENCARGA DE CREAR EL FORMULARIO CON LOS ENTRY NECESARIOS Y DE GUARDAR LA BASE DE DATOS CON LOS NUEVOS VALORES.
    def abrir_formulario(self, titulo, campos, callback, id_registro=None):
        """
        titulo       → string: título de la ventana emergente
        campos       → lista de tuplas: (label_texto, nombre_clave, obligatorio: bool)
        callback     → función que recibe un dict con los valores del formulario
        id_registro  → si se pasa, lo incluye en el dict (útil para modificar)
        """
        emergente = tk.Toplevel()
        emergente.title(titulo)
        emergente.resizable(False, False)
    
        entries = {}
    
        for label_texto, clave, _ in campos:
            tk.Label(emergente, text=label_texto).pack(pady=(8, 0))
            entry = tk.Entry(emergente, width=30)
            entry.pack(pady=(0, 4))
            entries[clave] = entry
    
        def guardar_y_cerrar():
            valores = {}
            for label_texto, clave, obligatorio in campos:
                val = entries[clave].get().strip()
                if obligatorio and not val:
                    messagebox.showerror("Error", f"El campo '{label_texto}' es obligatorio.")
                    return
                valores[clave] = val if val else None

            if id_registro is not None:
                valores["id"] = id_registro

            emergente.destroy()
            callback(valores)
    
        tk.Button(emergente, text="Guardar", command=guardar_y_cerrar).pack(pady=12)


# DEPARTAMENTO
    def insertar_departamento(self):
        campos = [
            ("Nombre",    "nombre",    True) 
        ]
        def callback(v):
            Departamento.insertar(bd, v["nombre"])
            self.cargar_departamentos()   
            messagebox.showinfo("OK", f"Departamento {v['nombre']} guardado   .")

        self.abrir_formulario("Insertar departamento", campos, callback)

    def modificar_departamento(self):
        indice = self.lista_depto.curselection()
        if not indice:
            return messagebox.showerror("Error", "Debes seleccionar un departamento.")

        texto = self.lista_depto.get(indice)
        id_departamento = int(texto.strip().split()[0].replace("#", ""))

        campos = [
            ("Nombre",    "nombre",    True)
        ]
        def callback(v):
            Departamento.modificar(bd, v["id"], v["nombre"])
            self.cargar_departamentos()
            messagebox.showinfo("OK", f"Departamento {v['nombre']} actualizado.")

        self.abrir_formulario("Modificar departamento", campos, callback, id_registro=id_departamento)

    def eliminar_departamento(self):
        indice = self.lista_depto.curselection()
        if not indice:
            return messagebox.showerror("Error", "Debes seleccionar un departamento.")

        texto = self.lista_depto.get(indice)
        id_departamento = int(texto.strip().split()[0].replace("#", ""))

        if messagebox.askyesno("Confirmar", f"¿Eliminar deapartamento con id {id_departamento}?"):
            Departamento.eliminar(bd, id_departamento)
            self.cargar_departamentos()
            messagebox.showinfo("OK", "Departamento eliminado.")

        
# AULA   
    def insertar_aula(self):
        campos = [
            ("Nombre",    "nombre",    True),
            ("Planta",    "planta",    True) 
        ]
        def callback(v):
            Aula.insertar(bd, v["nombre"], v["planta"])
            self.cargar_aulas()   
            messagebox.showinfo("OK", f"Aula {v['nombre']} guardada   .")

        self.abrir_formulario("Insertar aula", campos, callback)

    def modificar_aula(self):
        indice = self.lista_aula.curselection()
        if not indice:
            return messagebox.showerror("Error", "Debes seleccionar un aula.")

        texto = self.lista_aula.get(indice)
        id_aula = int(texto.strip().split()[0].replace("#", ""))

        campos = [
            ("Nombre",    "nombre",    True)
        ]
        def callback(v):
            Aula.modificar(bd, v["id"], v["nombre"])
            self.cargar_aulas()
            messagebox.showinfo("OK", f"Aula {v['nombre']} actualizada.")

        self.abrir_formulario("Modificar aula", campos, callback, id_registro=id_aula)


# ALUMNO
    def insertar_alumno(self):
        campos = [
            ("Nombre",    "nombre",    True),
            ("Apellidos", "apellidos", True),
            ("DNI",       "dni",       True),
            ("Email",     "email",     False),  # opcional
        ]
        def callback(v):
            Alumno.insertar(bd, v["nombre"], v["apellidos"], v["dni"], v["email"])
            self.cargar_alumnos()   
            messagebox.showinfo("OK", f"Alumno {v['nombre']} guardado   .")

        self.abrir_formulario("Insertar alumno", campos, callback)

    def modificar_alumno(self):
        indice = self.lista_alu.curselection()
        if not indice:
            return messagebox.showerror("Error", "Debes seleccionar un alumno.")

        texto = self.lista_alu.get(indice)
        id_alumno = int(texto.strip().split()[0].replace("#", ""))

        campos = [
            ("Nombre",    "nombre",    True),
            ("Apellidos", "apellidos", True),
            ("DNI",       "dni",       True),
            ("Email",     "email",     False),
        ]
        def callback(v):
            Alumno.modificar(bd, v["id"], v["nombre"], v["apellidos"], v["dni"], v["email"])
            self.cargar_alumnos()
            messagebox.showinfo("OK", f"Alumno {v['nombre']} actualizado.")

        self.abrir_formulario("Modificar alumno", campos, callback, id_registro=id_alumno)

    def eliminar_alumno(self):
        indice = self.lista_alu.curselection()
        if not indice:
            return messagebox.showerror("Error", "Debes seleccionar un alumno.")

        texto = self.lista_alu.get(indice)
        id_alumno = int(texto.strip().split()[0].replace("#", ""))

        if messagebox.askyesno("Confirmar", f"¿Eliminar alumno con id {id_alumno}?"):
            Alumno.eliminar(bd, id_alumno)
            self.cargar_alumnos()
            messagebox.showinfo("OK", "Alumno eliminado.")


# DOCENTE
    def insertar_docente(self):
        campos = [
            ("Nombre",    "nombre",    True),
            ("Apellidos", "apellidos", True),
            ("Email",     "email",     False),
            ("ID Depto",  "id_depto",  False),
        ]
        def callback(v):
            id_depto = int(v["id_depto"]) if v["id_depto"] else None  # ← conversión
            Docente.insertar(bd, v["nombre"], v["apellidos"], id_depto, v["email"])
            self.cargar_docentes()
            messagebox.showinfo("OK", f"Docente {v['nombre']} guardado  .")

        self.abrir_formulario("Insertar docente", campos, callback)
          
    def modificar_docente(self):
        indice = self.lista_doc.curselection()
        if not indice:
            return messagebox.showerror("Error", "Debes seleccionar un docente.")

        texto = self.lista_doc.get(indice)
        id_docente = int(texto.strip().split()[0].replace("#", ""))

        campos = [
            ("Nombre",    "nombre",    True),
            ("Apellidos", "apellidos", True),
            ("Email",     "email",     False),
            ("ID Depto",  "id_depto",  False),
        ]
        def callback(v):
            Docente.modificar(bd, v["id"], v["nombre"], v["apellidos"], v["email"], v["id_depto"])
            self.cargar_docentes()
            messagebox.showinfo("OK", f"Docente {v['nombre']} actualizado.")

        self.abrir_formulario("Modificar docente", campos, callback, id_registro=id_docente)
    
    def eliminar_docente(self):
        indice = self.lista_doc.curselection()
        if not indice:
            return messagebox.showerror("Error", "Debes seleccionar un docente.")

        texto = self.lista_doc.get(indice)
        id_docente = int(texto.strip().split()[0].replace("#", ""))

        if messagebox.askyesno("Confirmar", f"¿Eliminar docente con id {id_docente}?"):
            Docente.eliminar(bd, id_docente)
            self.cargar_docentes()
            messagebox.showinfo("OK", "Docente eliminado.")


# MÓDULO
    def insertar_modulo(self):
        campos = [
            ("Nombre",     "nombre",    True),
            ("Código",     "codigo",    True),
            ("Horas",      "horas",     True),
            ("ID Docente", "id_docente",  False),  # opcional
            ("ID Aula",    "id_aula",   False),  # opcional
        ]
        def callback(v):
            Modulo.insertar(bd, v["nombre"], v["codigo"], v["horas"], v["id_docente"], v["id_aula"])
            self.cargar_modulos()   
            messagebox.showinfo("OK", f"Modulo {v['nombre']} guardado.")

        self.abrir_formulario("Insertar modulo", campos, callback)
          
    def modificar_modulo(self):
        indice = self.lista_modulo.curselection()
        if not indice:
            return messagebox.showerror("Error", "Debes seleccionar un modulo.")

        texto = self.lista_modulo.get(indice)
        id_modulo = int(texto.strip().split()[0].replace("#", ""))

        campos = [
            ("Nombre",     "nombre",      True),
            ("Código",     "codigo",      True),
            ("Horas",      "horas",       True),
            ("ID Docente", "id_docente",  False),  # opcional
            ("ID Aula",    "id_aula",     False),  # opcional
        ]
        def callback(v):
            Modulo.modificar(bd,v["nombre"], v["codigo"], v["horas"], v["id_docente"], v["id_aula"])
            self.cargar_modulos()
            messagebox.showinfo("OK", f"modulo {v['nombre']} actualizado.")

        self.abrir_formulario("Modificar modulo", campos, callback, id_registro=id_modulo)
    
    def eliminar_modulo(self):
        indice = self.lista_modulo.curselection()
        if not indice:
            return messagebox.showerror("Error", "Debes seleccionar un modulo.")

        texto = self.lista_modulo.get(indice)
        id_modulo = int(texto.strip().split()[0].replace("#", ""))

        if messagebox.askyesno("Confirmar", f"¿Eliminar modulo con id {id_modulo}?"):
            Modulo.eliminar(bd, id_modulo)
            self.cargar_modulos()
            messagebox.showinfo("OK", "Modulo eliminado.")
           
            
# MATRÍCULA 
#--este está hecho de manera diferente al resto--#
    def insertar_matricula(self):
        
        emergente = tk.Toplevel()
        emergente.title("Insertar matrícula")  

        alumnos = {f"{f['nombre']} {f['apellidos']}": f['id'] for f in Alumno.obtener_todos(bd)}
        modulos = {f['nombre']: f['id']                      for f in Modulo.obtener_todos(bd)}

        tk.Label(emergente, text="Alumno:").pack(pady=(8,0))
        comb_alumnos = ttk.Combobox(emergente, values=list(alumnos.keys()), state="readonly",   width=30)
        comb_alumnos.pack(pady=(0,4))
        comb_alumnos.current(0)

        tk.Label(
        emergente, text="Módulo:").pack(pady=(8,0))
        comb_modulos = ttk.Combobox(emergente, values=list(modulos.keys()), state="readonly", width=30)
        comb_modulos.pack(pady=(0,4)) 
        comb_modulos.current(0)
        
        def guardar_cerrar():
            alumno_sel = comb_alumnos.get()
            modulo_sel = comb_modulos.get()
            
            if not alumno_sel or not modulo_sel:
                messagebox.showerror('Error', 'Debes seleccionar ambos campos')
            
            try: 
                Matricula.insertar(bd, alumnos[alumno_sel], modulos[modulo_sel])
            except Exception as e:
                messagebox.showerror("Error de base de datos", str(e))
                return 
            
            emergente.destroy()
            self.cargar_matriculas() 
            messagebox.showinfo("OK", f"{alumno_sel} matriculado en {modulo_sel}.")
                
        tk.Button(emergente, text="Guardar", command=guardar_cerrar).pack(pady=12)
            
    def eliminar_matricula(self):
        indice = self.lista_matr.curselection()
        if not indice:
            return messagebox.showerror("Error", "Debes seleccionar una matrícula.")

        texto = self.lista_matr.get(indice)
        ids = texto.strip().split()[0]          # extrae "3,7" (id_alumno,id_modulo)
        id_alumno, id_modulo = map(int, ids.split(","))

        if messagebox.askyesno("Confirmar", "¿Eliminar esta matrícula?"):
            m = Matricula(id_alumno, id_modulo)
            m.eliminar(bd)
            self.cargar_matriculas()
            messagebox.showinfo("OK", "Matrícula eliminada.")
