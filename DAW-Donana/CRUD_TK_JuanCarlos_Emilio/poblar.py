"""
poblar_bd.py
============
Ejecuta este script para llenar la base de datos con datos de ejemplo.
Es seguro ejecutarlo varias veces: los duplicados se ignoran automáticamente.

Uso:
    python poblar_bd.py
"""

from modelo import Database, Departamento, Aula, Docente, Alumno, Modulo, Matricula

bd = Database("instituto.db")

# ─────────────────────────────────────────
# 1. DEPARTAMENTOS  (7)
# ─────────────────────────────────────────
departamentos = [
    "Informática y Comunicaciones",
    "Administración y Gestión",
    "Electricidad y Electrónica",
    "Sanidad",
    "Servicios Socioculturales",
    "Hostelería y Turismo",
    "Edificación y Obra Civil",
]

print("Insertando departamentos...")
for nombre in departamentos:
    try:
        Departamento.insertar(bd, nombre)
    except Exception as e:
        print(f"  [!] Departamento '{nombre}': {e}")

deptos = {fila["nombre"]: fila["id"] for fila in Departamento.obtener_todos(bd)}
print(f"  Departamentos en BD: {len(deptos)}\n")

# ─────────────────────────────────────────
# 2. AULAS  (18)
# ─────────────────────────────────────────
aulas = [
    ("Aula 101", 1), ("Aula 102", 1), ("Aula 103", 1),
    ("Aula 201", 2), ("Aula 202", 2), ("Aula 203", 2),
    ("Aula 301", 3), ("Aula 302", 3),
    ("Laboratorio Redes",      1),
    ("Laboratorio Hardware",   1),
    ("Laboratorio Química",    2),
    ("Laboratorio Idiomas",    2),
    ("Aula Polivalente A",     0),
    ("Aula Polivalente B",     0),
    ("Sala Servidores",        3),
    ("Taller Electricidad",    0),
    ("Cocina Escuela",         0),
    ("Aula de Dibujo Técnico", 3),
]

print("Insertando aulas...")
for nombre, planta in aulas:
    try:
        Aula.insertar(bd, nombre, planta)
    except Exception as e:
        print(f"  [!] Aula '{nombre}': {e}")

aulas_bd = {fila["nombre"]: fila["id"] for fila in Aula.obtener_todos(bd)}
print(f"  Aulas en BD: {len(aulas_bd)}\n")

# ─────────────────────────────────────────
# 3. DOCENTES  (16)
# ─────────────────────────────────────────
docentes = [
    # (nombre, apellidos, email, depto)
    ("Carlos",    "Martínez López",    "c.martinez@instituto.es",   "Informática y Comunicaciones"),
    ("Laura",     "García Sánchez",    "l.garcia@instituto.es",     "Informática y Comunicaciones"),
    ("Francisco", "Gómez Reyes",       "f.gomez@instituto.es",      "Informática y Comunicaciones"),
    ("Raúl",      "Cano Bermejo",      "r.cano@instituto.es",       "Informática y Comunicaciones"),
    ("Antonio",   "Fernández Ruiz",    "a.fernandez@instituto.es",  "Electricidad y Electrónica"),
    ("Beatriz",   "Palacios Vera",     "b.palacios@instituto.es",   "Electricidad y Electrónica"),
    ("María",     "Jiménez Morales",   "m.jimenez@instituto.es",    "Administración y Gestión"),
    ("Ana",       "Díaz Castillo",     "a.diaz@instituto.es",       "Administración y Gestión"),
    ("Roberto",   "Leal Montoya",      "r.leal@instituto.es",       "Administración y Gestión"),
    ("Pedro",     "Rodríguez Vega",    "p.rodriguez@instituto.es",  "Sanidad"),
    ("Carmen",    "Villanueva Salas",  "c.villanueva@instituto.es", "Sanidad"),
    ("Isabel",    "López Guerrero",    "i.lopez@instituto.es",      "Servicios Socioculturales"),
    ("Jorge",     "Medina Fuentes",    "j.medina@instituto.es",     "Servicios Socioculturales"),
    ("Pilar",     "Núñez Aranda",      "p.nunez@instituto.es",      "Hostelería y Turismo"),
    ("Tomás",     "Cabrera Ibáñez",    "t.cabrera@instituto.es",    "Hostelería y Turismo"),
    ("Silvia",    "Ramos Escribano",   "s.ramos@instituto.es",      "Edificación y Obra Civil"),
]

print("Insertando docentes...")
for nombre, apellidos, email, depto in docentes:
    try:
        Docente.insertar(bd, nombre, apellidos, deptos.get(depto), email)
    except Exception as e:
        print(f"  [!] Docente '{nombre} {apellidos}': {e}")

docentes_bd = {f"{fila['nombre']} {fila['apellidos']}": fila["id"]
               for fila in Docente.obtener_todos(bd)}
print(f"  Docentes en BD: {len(docentes_bd)}\n")

# ─────────────────────────────────────────
# 4. MÓDULOS  (24)
# ─────────────────────────────────────────
modulos = [
    # (nombre, codigo, horas, docente, aula)
    # — Informática —
    ("Programación",                         "INF01", 256, "Carlos Martínez López",   "Aula 101"),
    ("Bases de Datos",                       "INF02", 192, "Laura García Sánchez",    "Laboratorio Redes"),
    ("Sistemas Informáticos",                "INF03", 160, "Francisco Gómez Reyes",   "Laboratorio Hardware"),
    ("Redes Locales",                        "INF04", 128, "Raúl Cano Bermejo",       "Laboratorio Redes"),
    ("Lenguajes de Marcas",                  "INF05",  96, "Laura García Sánchez",    "Aula 102"),
    ("Desarrollo de Interfaces",             "INF06", 128, "Carlos Martínez López",   "Aula 103"),
    ("Seguridad Informática",                "INF07", 160, "Raúl Cano Bermejo",       "Sala Servidores"),
    # — Electricidad —
    ("Instalaciones Eléctricas",             "ELE01", 200, "Antonio Fernández Ruiz",  "Taller Electricidad"),
    ("Electrónica Básica",                   "ELE02", 160, "Antonio Fernández Ruiz",  "Aula 201"),
    ("Automatismos Industriales",            "ELE03", 192, "Beatriz Palacios Vera",   "Taller Electricidad"),
    ("Electrotecnia",                        "ELE04", 128, "Beatriz Palacios Vera",   "Aula 202"),
    # — Administración —
    ("Gestión Empresarial",                  "ADM01", 128, "María Jiménez Morales",   "Aula Polivalente A"),
    ("Contabilidad y Fiscalidad",            "ADM02", 192, "Ana Díaz Castillo",       "Aula Polivalente B"),
    ("Recursos Humanos",                     "ADM03", 128, "Roberto Leal Montoya",    "Aula Polivalente A"),
    ("Ofimática Avanzada",                   "ADM04",  96, "María Jiménez Morales",   "Aula 203"),
    # — Sanidad —
    ("Anatomía Aplicada",                    "SAN01", 128, "Pedro Rodríguez Vega",    "Aula 301"),
    ("Atención Sociosanitaria",              "SAN02", 160, "Carmen Villanueva Salas", "Aula 301"),
    ("Primeros Auxilios",                    "SAN03",  64, "Pedro Rodríguez Vega",    "Aula 302"),
    # — Servicios Socioculturales —
    ("Intervención Comunitaria",             "SOC01", 160, "Isabel López Guerrero",   "Aula 302"),
    ("Animación Sociocultural",              "SOC02", 128, "Jorge Medina Fuentes",    "Aula Polivalente B"),
    # — Hostelería —
    ("Técnicas Culinarias",                  "HOS01", 240, "Pilar Núñez Aranda",      "Cocina Escuela"),
    ("Gestión de Alojamientos",              "HOS02", 128, "Tomás Cabrera Ibáñez",    "Aula Polivalente A"),
    # — Edificación —
    ("Representación Gráfica en Construcción","EDI01",160, "Silvia Ramos Escribano",  "Aula de Dibujo Técnico"),
    # — Transversal —
    ("Formación y Orientación Laboral",      "FOL01",  96, "Ana Díaz Castillo",       "Aula Polivalente A"),
]

print("Insertando módulos...")
for nombre, codigo, horas, docente_nc, aula_nombre in modulos:
    try:
        id_docente = docentes_bd.get(docente_nc)
        id_aula    = aulas_bd.get(aula_nombre)
        Modulo.insertar(bd, nombre, codigo, horas, id_docente, id_aula)
    except Exception as e:
        print(f"  [!] Módulo '{nombre}': {e}")

modulos_bd = {fila["nombre"]: fila["id"] for fila in Modulo.obtener_todos(bd)}
print(f"  Módulos en BD: {len(modulos_bd)}\n")

# ─────────────────────────────────────────
# 5. ALUMNOS  (50)
# ─────────────────────────────────────────
alumnos = [
    # — Grupo Informática A —
    ("Sofía",      "Herrera Campos",    "11111111A", "sofia.herrera@alumnos.es"),
    ("Diego",      "Torres Blanco",     "22222222B", "diego.torres@alumnos.es"),
    ("Lucía",      "Navarro Gil",       "33333333C", "lucia.navarro@alumnos.es"),
    ("Alejandro",  "Moreno Fuentes",    "44444444D", "alejandro.moreno@alumnos.es"),
    ("Valentina",  "Romero Vidal",      "55555555E", "valentina.romero@alumnos.es"),
    ("Javier",     "Flores Aguilar",    "21212121W", "javier.flores@alumnos.es"),
    ("Elena",      "Domínguez Rojo",    "18181818S", "elena.dominguez@alumnos.es"),
    ("Rubén",      "Soto Pedraza",      "31313131X", "ruben.soto@alumnos.es"),
    # — Grupo Informática B —
    ("Irene",      "Crespo Palomino",   "32323232Y", "irene.crespo@alumnos.es"),
    ("Mario",      "Gallego Barrios",   "34343434Z", "mario.gallego@alumnos.es"),
    ("Patricia",   "Serrano Montiel",   "35353535A", "patricia.serrano@alumnos.es"),
    ("Guillermo",  "Vega Aparicio",     "36363636B", "guillermo.vega@alumnos.es"),
    ("Cristina",   "Mora Hidalgo",      "37373737C", "cristina.mora@alumnos.es"),
    ("Óscar",      "Pino Lozano",       "38383838D", "oscar.pino@alumnos.es"),
    # — Grupo Electricidad —
    ("Iván",       "Sánchez Pardo",     "66666666F", "ivan.sanchez@alumnos.es"),
    ("Nora",       "Pérez Alonso",      "77777777G", "nora.perez@alumnos.es"),
    ("Marcos",     "Ruiz Serrano",      "88888888H", "marcos.ruiz@alumnos.es"),
    ("Claudia",    "Álvarez Ibáñez",    "99999999J", "claudia.alvarez@alumnos.es"),
    ("Borja",      "Vargas Cano",       "39393939E", "borja.vargas@alumnos.es"),
    ("Natalia",    "Pons Guerrero",     "40404040F", "natalia.pons@alumnos.es"),
    ("Andrés",     "Fuentes Prieto",    "41414141G", "andres.fuentes@alumnos.es"),
    ("Rebeca",     "Ortiz Delgado",     "42424242H", "rebeca.ortiz@alumnos.es"),
    # — Grupo Administración —
    ("Hugo",       "Molina Espinosa",   "10101010K", "hugo.molina@alumnos.es"),
    ("Emma",       "Castro Delgado",    "12121212L", "emma.castro@alumnos.es"),
    ("Daniel",     "Ortega Vargas",     "13131313M", "daniel.ortega@alumnos.es"),
    ("Marta",      "Ramos Santana",     "14141414N", "marta.ramos@alumnos.es"),
    ("Gonzalo",    "Iglesias Blanco",   "43434343J", "gonzalo.iglesias@alumnos.es"),
    ("Lorena",     "Bravo Moya",        "44444445K", "lorena.bravo@alumnos.es"),
    ("Rafael",     "Durán Escribano",   "45454545L", "rafael.duran@alumnos.es"),
    ("Inés",       "Aguilar Serna",     "46464646M", "ines.aguilar@alumnos.es"),
    # — Grupo Sanidad —
    ("Adrián",     "Suárez Medina",     "15151515P", "adrian.suarez@alumnos.es"),
    ("Carla",      "Vázquez Montes",    "16161616Q", "carla.vazquez@alumnos.es"),
    ("Pablo",      "Guerrero Lara",     "17171717R", "pablo.guerrero@alumnos.es"),
    ("Sergio",     "Iglesias Mora",     "19191919T", "sergio.iglesias@alumnos.es"),
    ("Alba",       "Nieto Cabrera",     "20202020V", "alba.nieto@alumnos.es"),
    ("Miriam",     "Cabello Reina",     "47474747N", "miriam.cabello@alumnos.es"),
    ("Tomás",      "Campos Naranjo",    "48484848P", "tomas.campos@alumnos.es"),
    ("Verónica",   "Estévez Claro",     "49494949Q", "veronica.estevez@alumnos.es"),
    # — Grupo Servicios Socioculturales —
    ("Raquel",     "Mendoza Cortés",    "50505050R", "raquel.mendoza@alumnos.es"),
    ("Fátima",     "Benítez Reyes",     "51515151S", "fatima.benitez@alumnos.es"),
    ("Nicolás",    "Giménez Pastor",    "52525252T", "nicolas.gimenez@alumnos.es"),
    ("Amparo",     "Solís Arenas",      "53535353V", "amparo.solis@alumnos.es"),
    # — Grupo Hostelería —
    ("Kevin",      "Herrero Lara",      "54545454W", "kevin.herrero@alumnos.es"),
    ("Lidia",      "Prado Baena",       "55555556X", "lidia.prado@alumnos.es"),
    ("Jonás",      "Carmona Téllez",    "56565656Y", "jonas.carmona@alumnos.es"),
    ("Sandra",     "Moya Pascual",      "57575757Z", "sandra.moya@alumnos.es"),
    ("Alberto",    "Luque Expósito",    "58585858A", "alberto.luque@alumnos.es"),
    # — Grupo Edificación —
    ("Inmaculada", "Peña Bautista",     "59595959B", "inma.pena@alumnos.es"),
    ("Fermín",     "Gutiérrez Niño",    "60606060C", "fermin.gutierrez@alumnos.es"),
    ("Rocío",      "Arenas Montoro",    "61616161D", "rocio.arenas@alumnos.es"),
]

print("Insertando alumnos...")
for nombre, apellidos, dni, email in alumnos:
    try:
        Alumno.insertar(bd, nombre, apellidos, dni, email)
    except Exception as e:
        print(f"  [!] Alumno '{nombre} {apellidos}': {e}")

alumnos_bd = {f"{fila['nombre']} {fila['apellidos']}": fila["id"]
              for fila in Alumno.obtener_todos(bd)}
print(f"  Alumnos en BD: {len(alumnos_bd)} registros\n")

# ─────────────────────────────────────────
# 6. MATRÍCULAS
# ─────────────────────────────────────────
matriculas = [
    # ── Informática A ──
    ("Sofía Herrera Campos",      "Programación"),
    ("Sofía Herrera Campos",      "Bases de Datos"),
    ("Sofía Herrera Campos",      "Lenguajes de Marcas"),
    ("Sofía Herrera Campos",      "Formación y Orientación Laboral"),
    ("Diego Torres Blanco",       "Programación"),
    ("Diego Torres Blanco",       "Sistemas Informáticos"),
    ("Diego Torres Blanco",       "Redes Locales"),
    ("Diego Torres Blanco",       "Seguridad Informática"),
    ("Lucía Navarro Gil",         "Bases de Datos"),
    ("Lucía Navarro Gil",         "Lenguajes de Marcas"),
    ("Lucía Navarro Gil",         "Desarrollo de Interfaces"),
    ("Lucía Navarro Gil",         "Formación y Orientación Laboral"),
    ("Alejandro Moreno Fuentes",  "Programación"),
    ("Alejandro Moreno Fuentes",  "Redes Locales"),
    ("Alejandro Moreno Fuentes",  "Sistemas Informáticos"),
    ("Alejandro Moreno Fuentes",  "Seguridad Informática"),
    ("Valentina Romero Vidal",    "Bases de Datos"),
    ("Valentina Romero Vidal",    "Programación"),
    ("Valentina Romero Vidal",    "Desarrollo de Interfaces"),
    ("Valentina Romero Vidal",    "Formación y Orientación Laboral"),
    ("Javier Flores Aguilar",     "Programación"),
    ("Javier Flores Aguilar",     "Redes Locales"),
    ("Javier Flores Aguilar",     "Seguridad Informática"),
    ("Elena Domínguez Rojo",      "Bases de Datos"),
    ("Elena Domínguez Rojo",      "Lenguajes de Marcas"),
    ("Elena Domínguez Rojo",      "Formación y Orientación Laboral"),
    ("Rubén Soto Pedraza",        "Programación"),
    ("Rubén Soto Pedraza",        "Sistemas Informáticos"),
    ("Rubén Soto Pedraza",        "Redes Locales"),
    # ── Informática B ──
    ("Irene Crespo Palomino",     "Programación"),
    ("Irene Crespo Palomino",     "Bases de Datos"),
    ("Irene Crespo Palomino",     "Desarrollo de Interfaces"),
    ("Mario Gallego Barrios",     "Sistemas Informáticos"),
    ("Mario Gallego Barrios",     "Redes Locales"),
    ("Mario Gallego Barrios",     "Seguridad Informática"),
    ("Patricia Serrano Montiel",  "Programación"),
    ("Patricia Serrano Montiel",  "Lenguajes de Marcas"),
    ("Patricia Serrano Montiel",  "Formación y Orientación Laboral"),
    ("Guillermo Vega Aparicio",   "Redes Locales"),
    ("Guillermo Vega Aparicio",   "Seguridad Informática"),
    ("Guillermo Vega Aparicio",   "Sistemas Informáticos"),
    ("Cristina Mora Hidalgo",     "Bases de Datos"),
    ("Cristina Mora Hidalgo",     "Desarrollo de Interfaces"),
    ("Cristina Mora Hidalgo",     "Formación y Orientación Laboral"),
    ("Óscar Pino Lozano",         "Programación"),
    ("Óscar Pino Lozano",         "Sistemas Informáticos"),
    ("Óscar Pino Lozano",         "Seguridad Informática"),
    # ── Electricidad ──
    ("Iván Sánchez Pardo",        "Instalaciones Eléctricas"),
    ("Iván Sánchez Pardo",        "Electrónica Básica"),
    ("Iván Sánchez Pardo",        "Automatismos Industriales"),
    ("Nora Pérez Alonso",         "Instalaciones Eléctricas"),
    ("Nora Pérez Alonso",         "Electrotecnia"),
    ("Nora Pérez Alonso",         "Formación y Orientación Laboral"),
    ("Marcos Ruiz Serrano",       "Electrónica Básica"),
    ("Marcos Ruiz Serrano",       "Instalaciones Eléctricas"),
    ("Marcos Ruiz Serrano",       "Automatismos Industriales"),
    ("Claudia Álvarez Ibáñez",    "Electrónica Básica"),
    ("Claudia Álvarez Ibáñez",    "Electrotecnia"),
    ("Claudia Álvarez Ibáñez",    "Formación y Orientación Laboral"),
    ("Borja Vargas Cano",         "Instalaciones Eléctricas"),
    ("Borja Vargas Cano",         "Automatismos Industriales"),
    ("Borja Vargas Cano",         "Electrotecnia"),
    ("Natalia Pons Guerrero",     "Electrónica Básica"),
    ("Natalia Pons Guerrero",     "Formación y Orientación Laboral"),
    ("Andrés Fuentes Prieto",     "Instalaciones Eléctricas"),
    ("Andrés Fuentes Prieto",     "Electrotecnia"),
    ("Andrés Fuentes Prieto",     "Automatismos Industriales"),
    ("Rebeca Ortiz Delgado",      "Electrónica Básica"),
    ("Rebeca Ortiz Delgado",      "Formación y Orientación Laboral"),
    # ── Administración ──
    ("Hugo Molina Espinosa",      "Gestión Empresarial"),
    ("Hugo Molina Espinosa",      "Contabilidad y Fiscalidad"),
    ("Hugo Molina Espinosa",      "Recursos Humanos"),
    ("Emma Castro Delgado",       "Gestión Empresarial"),
    ("Emma Castro Delgado",       "Ofimática Avanzada"),
    ("Emma Castro Delgado",       "Formación y Orientación Laboral"),
    ("Daniel Ortega Vargas",      "Contabilidad y Fiscalidad"),
    ("Daniel Ortega Vargas",      "Gestión Empresarial"),
    ("Daniel Ortega Vargas",      "Recursos Humanos"),
    ("Marta Ramos Santana",       "Contabilidad y Fiscalidad"),
    ("Marta Ramos Santana",       "Ofimática Avanzada"),
    ("Marta Ramos Santana",       "Formación y Orientación Laboral"),
    ("Gonzalo Iglesias Blanco",   "Gestión Empresarial"),
    ("Gonzalo Iglesias Blanco",   "Recursos Humanos"),
    ("Lorena Bravo Moya",         "Contabilidad y Fiscalidad"),
    ("Lorena Bravo Moya",         "Ofimática Avanzada"),
    ("Lorena Bravo Moya",         "Formación y Orientación Laboral"),
    ("Rafael Durán Escribano",    "Gestión Empresarial"),
    ("Rafael Durán Escribano",    "Contabilidad y Fiscalidad"),
    ("Inés Aguilar Serna",        "Ofimática Avanzada"),
    ("Inés Aguilar Serna",        "Recursos Humanos"),
    ("Inés Aguilar Serna",        "Formación y Orientación Laboral"),
    # ── Sanidad ──
    ("Adrián Suárez Medina",      "Anatomía Aplicada"),
    ("Adrián Suárez Medina",      "Atención Sociosanitaria"),
    ("Adrián Suárez Medina",      "Primeros Auxilios"),
    ("Carla Vázquez Montes",      "Anatomía Aplicada"),
    ("Carla Vázquez Montes",      "Primeros Auxilios"),
    ("Carla Vázquez Montes",      "Formación y Orientación Laboral"),
    ("Pablo Guerrero Lara",       "Atención Sociosanitaria"),
    ("Pablo Guerrero Lara",       "Anatomía Aplicada"),
    ("Pablo Guerrero Lara",       "Primeros Auxilios"),
    ("Sergio Iglesias Mora",      "Anatomía Aplicada"),
    ("Sergio Iglesias Mora",      "Atención Sociosanitaria"),
    ("Sergio Iglesias Mora",      "Formación y Orientación Laboral"),
    ("Alba Nieto Cabrera",        "Atención Sociosanitaria"),
    ("Alba Nieto Cabrera",        "Primeros Auxilios"),
    ("Miriam Cabello Reina",      "Anatomía Aplicada"),
    ("Miriam Cabello Reina",      "Atención Sociosanitaria"),
    ("Miriam Cabello Reina",      "Formación y Orientación Laboral"),
    ("Tomás Campos Naranjo",      "Primeros Auxilios"),
    ("Tomás Campos Naranjo",      "Anatomía Aplicada"),
    ("Verónica Estévez Claro",    "Atención Sociosanitaria"),
    ("Verónica Estévez Claro",    "Primeros Auxilios"),
    ("Verónica Estévez Claro",    "Formación y Orientación Laboral"),
    # ── Servicios Socioculturales ──
    ("Raquel Mendoza Cortés",     "Intervención Comunitaria"),
    ("Raquel Mendoza Cortés",     "Animación Sociocultural"),
    ("Raquel Mendoza Cortés",     "Formación y Orientación Laboral"),
    ("Fátima Benítez Reyes",      "Intervención Comunitaria"),
    ("Fátima Benítez Reyes",      "Animación Sociocultural"),
    ("Nicolás Giménez Pastor",    "Intervención Comunitaria"),
    ("Nicolás Giménez Pastor",    "Formación y Orientación Laboral"),
    ("Amparo Solís Arenas",       "Animación Sociocultural"),
    ("Amparo Solís Arenas",       "Formación y Orientación Laboral"),
    # ── Hostelería ──
    ("Kevin Herrero Lara",        "Técnicas Culinarias"),
    ("Kevin Herrero Lara",        "Gestión de Alojamientos"),
    ("Kevin Herrero Lara",        "Formación y Orientación Laboral"),
    ("Lidia Prado Baena",         "Técnicas Culinarias"),
    ("Lidia Prado Baena",         "Formación y Orientación Laboral"),
    ("Jonás Carmona Téllez",      "Técnicas Culinarias"),
    ("Jonás Carmona Téllez",      "Gestión de Alojamientos"),
    ("Sandra Moya Pascual",       "Gestión de Alojamientos"),
    ("Sandra Moya Pascual",       "Formación y Orientación Laboral"),
    ("Alberto Luque Expósito",    "Técnicas Culinarias"),
    ("Alberto Luque Expósito",    "Gestión de Alojamientos"),
    # ── Edificación ──
    ("Inmaculada Peña Bautista",  "Representación Gráfica en Construcción"),
    ("Inmaculada Peña Bautista",  "Formación y Orientación Laboral"),
    ("Fermín Gutiérrez Niño",     "Representación Gráfica en Construcción"),
    ("Fermín Gutiérrez Niño",     "Gestión Empresarial"),
    ("Rocío Arenas Montoro",      "Representación Gráfica en Construcción"),
    ("Rocío Arenas Montoro",      "Formación y Orientación Laboral"),
]

print("Insertando matrículas...")
ok = 0
for alumno_nc, modulo_nombre in matriculas:
    id_alumno = alumnos_bd.get(alumno_nc)
    id_modulo  = modulos_bd.get(modulo_nombre)
    if id_alumno is None or id_modulo is None:
        print(f"  [!] No encontrado: alumno='{alumno_nc}' módulo='{modulo_nombre}'")
        continue
    try:
        Matricula.insertar(bd, id_alumno, id_modulo)
        ok += 1
    except Exception as e:
        print(f"  [!] Matrícula '{alumno_nc}' → '{modulo_nombre}': {e}")

print(f"  Matrículas insertadas: {ok}\n")

# ─────────────────────────────────────────
# RESUMEN FINAL
# ─────────────────────────────────────────
print("=" * 45)
print("RESUMEN DE LA BASE DE DATOS")
print("=" * 45)
print(f"  Departamentos : {len(Departamento.obtener_todos(bd))}")
print(f"  Aulas         : {len(Aula.obtener_todos(bd))}")
print(f"  Docentes      : {len(Docente.obtener_todos(bd))}")
print(f"  Módulos       : {len(Modulo.obtener_todos(bd))}")
print(f"  Alumnos       : {len(Alumno.obtener_todos(bd))}")
print(f"  Matrículas    : {len(Matricula.obtener_todos(bd))}")
print("=" * 45)
print("¡Base de datos lista! Ejecuta main.py para usar la app.")

bd.close()