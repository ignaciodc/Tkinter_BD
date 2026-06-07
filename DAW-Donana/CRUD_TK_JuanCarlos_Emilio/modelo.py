import sqlite3

#==============#
#  BASE DATOS  #
#==============#
class Database:
    def __init__(self, path_bd="instituto.db"):
        self.con = sqlite3.connect(path_bd)
        self.con.row_factory = sqlite3.Row
        self.con.execute("PRAGMA foreign_keys = ON")
        self.create_table()

    def execute(self, consulta, parametros=()):
        cur = self.con.execute(consulta, parametros)
        self.con.commit()
        return cur

    def fetchall(self, consulta, parametros=()):
        return self.con.execute(consulta, parametros).fetchall() 

    def fetchone(self, consulta, parametros=()):
        return self.con.execute(consulta, parametros).fetchone()

    def close(self):
        self.con.close()

    
    # CREACIÓN DE TABLAS:
    
    def create_table(self):
        self.execute("""
            CREATE TABLE IF NOT EXISTS Departamento (
                id      INTEGER  PRIMARY KEY AUTOINCREMENT,
                nombre  TEXT     NOT NULL UNIQUE
            )""")
        self.execute("""
            CREATE TABLE IF NOT EXISTS Aula (
                id      INTEGER  PRIMARY KEY AUTOINCREMENT,
                nombre  TEXT     NOT NULL UNIQUE,
                planta  INTEGER  DEFAULT 0
            )""")
        self.execute("""
            CREATE TABLE IF NOT EXISTS Docente (
                id        INTEGER  PRIMARY KEY AUTOINCREMENT,
                nombre    TEXT     NOT NULL,
                apellidos TEXT     NOT NULL,
                email     TEXT     UNIQUE,
                id_depto  INTEGER  REFERENCES Departamento(id) ON DELETE SET NULL
            )""")
        self.execute("""
            CREATE TABLE IF NOT EXISTS Modulo (
                id         INTEGER  PRIMARY KEY AUTOINCREMENT,
                nombre     TEXT     NOT NULL,
                codigo     TEXT     UNIQUE,
                horas      INTEGER  DEFAULT 0,
                id_docente INTEGER  REFERENCES Docente(id) ON DELETE SET NULL,
                id_aula    INTEGER  REFERENCES Aula(id)    ON DELETE SET NULL
            )""")
        self.execute("""
            CREATE TABLE IF NOT EXISTS Alumno (
                id        INTEGER  PRIMARY KEY AUTOINCREMENT,
                nombre    TEXT     NOT NULL,
                apellidos TEXT     NOT NULL,
                dni       TEXT     UNIQUE NOT NULL,
                email     TEXT
            )""")
        self.execute("""
            CREATE TABLE IF NOT EXISTS Matricula (
                id_alumno INTEGER  REFERENCES Alumno(id) ON DELETE CASCADE,
                id_modulo INTEGER  REFERENCES Modulo(id) ON DELETE CASCADE,
                PRIMARY KEY (id_alumno, id_modulo)
            )""")

#==================#
#  CLASES OBJETOS  #
#==================#

class Departamento:
    """Crea un Departamento del instituto"""

    def __init__(self, id, nombre=""):
        self.id     = id
        self.nombre = nombre

    def __str__(self):
        return self.nombre

    @staticmethod
    def insertar(bd, nombre):                          
        bd.execute("INSERT INTO Departamento(nombre) VALUES (?)", (nombre,))

    @staticmethod
    def modificar(bd, id ,nombre=None):
        if nombre is None:
            return
        bd.execute("UPDATE Departamento SET nombre = ? WHERE id = ?", (nombre, id))
        
    @staticmethod
    def eliminar(bd, id):
        bd.execute("DELETE FROM Departamento WHERE id = ?", (id,))  

    @staticmethod
    def obtener_todos(bd):
        return bd.fetchall("SELECT * FROM Departamento")

#---------------------------------------------

class Aula:
    """Crea un aula del instituto"""

    def __init__(self, id, nombre="", planta=0):
        self.id     = id
        self.nombre = nombre
        self.planta = planta

    def __str__(self):
        return f"{self.nombre} (planta {self.planta})"

    @staticmethod
    def insertar(bd, nombre, planta=None):
        bd.execute("INSERT INTO Aula(nombre, planta) VALUES(?, ?)", (nombre, planta))

    @staticmethod
    def modificar(bd, id, nombre=None):
        campos, valores = [], []
        if nombre is not None: campos.append("nombre = ?"); valores.append(nombre)
        if not campos:
            return
        valores.append(id)
        bd.execute(f"UPDATE Aula SET {', '.join(campos)} WHERE id = ?", valores) 
    
    @staticmethod
    def obtener_todos(bd):
        return bd.fetchall("SELECT * FROM Aula")

#---------------------------------------------

class Docente:
    """Crea un docente del centro"""

    def __init__(self, id, nombre="", apellidos="", email=None, id_depto=None, departamento=""):
        self.id           = id
        self.nombre       = nombre
        self.apellidos    = apellidos
        self.email        = email
        self.id_depto     = id_depto
        self.departamento = departamento

    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}"

    def __str__(self):
        return self.nombre_completo()

    @staticmethod
    def insertar(bd, nombre, apellidos, id_depto=None, email=None):
        bd.execute("""
            INSERT INTO Docente(nombre, apellidos, email, id_depto)
            VALUES(?, ?, ?, ?)
        """, (nombre, apellidos, email, id_depto))

    @staticmethod
    def modificar(bd, id, nombre=None, apellidos=None, email=None, id_depto=None):  
        campos, valores = [], []
        if nombre    is not None: campos.append("nombre = ?");    valores.append(nombre)
        if apellidos is not None: campos.append("apellidos = ?"); valores.append(apellidos)
        if email     is not None: campos.append("email = ?");     valores.append(email)
        if id_depto  is not None: campos.append("id_depto = ?");  valores.append(id_depto)
        if not campos:
            return
        valores.append(id)
        bd.execute(f"UPDATE Docente SET {', '.join(campos)} WHERE id = ?", valores)

    @staticmethod
    def eliminar(bd, id):
        bd.execute("DELETE FROM Docente WHERE id = ?", (id,))
    
    @staticmethod
    def obtener_todos(bd):
        return bd.fetchall("SELECT * FROM Docente ")

#---------------------------------------------

class Alumno:
    def __init__(self, id, nombre="", apellidos="", dni="", email=None):
        self.id        = id
        self.nombre    = nombre
        self.apellidos = apellidos
        self.dni       = dni
        self.email     = email

    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}"

    def __str__(self):
        return self.nombre_completo()

    @staticmethod
    def insertar(bd, nombre, apellidos, dni, email=None):
        bd.execute("""
            INSERT INTO Alumno(nombre, apellidos, dni, email)
            VALUES (?, ?, ?, ?)
        """, (nombre, apellidos, dni, email))

    @staticmethod
    def modificar(bd, id, nombre=None, apellidos=None, dni=None, email=None):
        campos, valores = [], []
        if nombre    is not None: campos.append("nombre = ?");    valores.append(nombre)
        if apellidos is not None: campos.append("apellidos = ?"); valores.append(apellidos)
        if dni       is not None: campos.append("dni = ?");       valores.append(dni)
        if email     is not None: campos.append("email = ?");     valores.append(email)
        if not campos:
            return
        valores.append(id)
        bd.execute(f"UPDATE Alumno SET {', '.join(campos)} WHERE id = ?", valores)

    @staticmethod
    def eliminar(bd, id):
        bd.execute("DELETE FROM Alumno WHERE id = ?", (id,))
    
    @staticmethod
    def obtener_todos(bd):
        return bd.fetchall("SELECT * FROM Alumno")

#---------------------------------------------

class Modulo:
    def __init__(self, id=None, nombre="", codigo=None, horas=0,
                 id_docente=None, id_aula=None, docente="", aula="", num_alumnos=0):
        self.id          = id
        self.nombre      = nombre
        self.codigo      = codigo
        self.horas       = horas
        self.id_docente  = id_docente
        self.id_aula     = id_aula
        self.docente     = docente       # solo para mostrar (JOIN)
        self.aula        = aula          # solo para mostrar (JOIN)
        self.num_alumnos = num_alumnos   # solo para mostrar (JOIN)

    def __str__(self):
        return f"{self.codigo}"

    @staticmethod
    def insertar(bd, nombre, codigo=None, horas=None, id_docente=None, id_aula=None):  
        bd.execute("""
            INSERT INTO Modulo(nombre, codigo, horas, id_docente, id_aula)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, codigo, horas, id_docente, id_aula))
    @staticmethod
    def modificar(bd, id, nombre=None, codigo=None, horas=None, id_docente=None, id_aula=None): 
        campos, valores = [], []
        if nombre     is not None: campos.append("nombre = ?");     valores.append(nombre)
        if codigo     is not None: campos.append("codigo = ?");     valores.append(codigo)
        if horas      is not None: campos.append("horas = ?");      valores.append(horas)
        if id_docente is not None: campos.append("id_docente = ?"); valores.append(id_docente)
        if id_aula    is not None: campos.append("id_aula = ?");    valores.append(id_aula)
        if not campos:
            return
        valores.append(id)
        bd.execute(f"UPDATE Modulo SET {', '.join(campos)} WHERE id = ?", valores)

    @staticmethod
    def eliminar(bd, id):
        bd.execute("DELETE FROM Modulo WHERE id = ?", (id,))  

    @staticmethod
    def obtener_todos(bd):
        return bd.fetchall("SELECT * FROM Modulo")

#---------------------------------------------

class Matricula:
    """Matricula un alumno a un módulo"""

    def __init__(self, id_alumno, id_modulo):
        self.id_alumno = id_alumno
        self.id_modulo = id_modulo

    @staticmethod
    def insertar(bd, id_alumno, id_modulo):
        bd.execute("""
            INSERT INTO Matricula(id_alumno, id_modulo) VALUES (?, ?)
        """, (id_alumno, id_modulo))          

    def eliminar(self, bd):
        bd.execute("""
            DELETE FROM Matricula WHERE id_alumno = ? AND id_modulo = ?
        """, (self.id_alumno, self.id_modulo))
    
    @staticmethod
    def obtener_todos(bd):
        return bd.fetchall("""  SELECT 
                                    m.id_alumno,  
                                    m.id_modulo,  
                                    concat_ws(' ',a.nombre, a.apellidos) AS alumno, 
                                    mod.nombre AS modulo
                                FROM Alumno a JOIN Matricula m ON id_alumno = a.id
                                              JOIN Modulo mod ON id_modulo = mod.id""")    
#---------------------------------------------
