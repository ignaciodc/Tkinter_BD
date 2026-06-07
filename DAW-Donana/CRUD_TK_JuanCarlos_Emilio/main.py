import tkinter as tk
from tkinter import ttk
from vistas import PantallaPrincipal

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.attributes('-fullscreen', True)
        self.title('APP')
        self.geometry('800x600')

        contenedor = tk.Frame(self)
        contenedor.pack(expand=True, fill='both')
        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)

        # Pantalla de inicio
        self.inicio = tk.Frame(contenedor, background="#262323")
        self.inicio.grid(row=0, column=0, sticky="nsew")

        # Frame interior que contiene todo el contenido centrado
        centro = tk.Frame(self.inicio, background="#262323")
        centro.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(centro, text="🏫 Instituto",
            font=("Roboto", 56, "bold"), fg="#FFFFFF", background="#262323").pack(pady=20)

        tk.Label(centro, text="Gestión de alumnos, docentes y módulos",
            font=("Roboto", 16), fg="#FFFFFF", background="#262323").pack(pady=10)

        tk.Label(centro, text='Bienvenido a la base de datos del instituto',
            font=("Roboto", 20, "bold"), fg="#FFFFFF", background="#262323").pack(pady=10)

        tk.Button(centro, text="Entrar", command=self.mostrar,
            font=("Roboto", 20), activebackground="#797B76", activeforeground="#FFFFFF", bg="#444240", fg="#FFFFFF",
            padx=20, pady=8, relief="flat").pack(pady=20)
        
        tk.Button(self.inicio, text="Cerrar Aplicación", command=self.quit,font=("Roboto", 15), activebackground="#797B76", activeforeground="#FEFAE3", bg="#444240", fg="#FFFFFF",
            padx=20, pady=8, relief="flat").pack(pady=20, side=tk.BOTTOM)

        # Pantalla principal
        self.pantalla_principal = PantallaPrincipal(contenedor)
        self.pantalla_principal.grid(row=0, column=0, sticky="nsew")

        self.inicio.tkraise()

    def mostrar(self):
        self.pantalla_principal.tkraise()
    

app = Aplicacion()
app.mainloop()