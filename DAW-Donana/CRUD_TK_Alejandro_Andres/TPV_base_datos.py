"""
La gestión de la base de datós de la aplicación de un restaurante.
"""

import sqlite3
from TPV_modelo import Mesa, Alergeno, Producto, Pedido, Linea_pedido
con = None
cur = None

def abrir_db() -> None:
    """
    Abre la base de datos, crea la conexión y el cursor.
    """
    # Conectamos la conexión global y el cursor global a la base de datos
    global con, cur
    con = sqlite3.connect('base_datos.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    # Activamos las comprobaciones de claves foráneas
    cur.execute("PRAGMA foreign_keys = ON;")

def crear_tabla_mesa() -> None:
    """
    Crea la tabla para almacenar las mesas
    """
    cur.execute("CREATE TABLE mesa(numero integer primary key, capacidad int not null, estado varchar(15) not null)")
    con.commit()

def insertar_mesa(mesa: Mesa) -> None:
    """
    Inserta una nueva mesa en la base de datos. 
    """
    cur.execute("INSERT INTO mesa(capacidad, estado) VALUES(?, ?)", (mesa.capacidad, mesa.estado))
    mesa.numero = cur.lastrowid
    con.commit()

def borrar_mesa(mesa: Mesa) -> None:
    """
    Borra la mesa de la base de datos.
    """
    cur.execute("DELETE FROM mesa WHERE numero = ?", (mesa.numero,))
    con.commit()

def actualizar_mesa(mesa: Mesa) -> None:
    """
    Actualiza la mesa en la base de datos con sus datos actuales.
    """
    cur.execute("UPDATE mesa SET capacidad = ?, estado = ? WHERE numero = ?", (mesa.capacidad, mesa.estado, mesa.numero))
    con.commit()

def obtener_mesas() -> dict[int, Mesa]:
    # Obtenemos todos los registros de mesa
    cur.execute("SELECT numero, capacidad, estado FROM mesa")
    filas = cur.fetchall()

    diccionario_mesas = {}

    # Vamos recorriendo todos los registros, instanciando las mesas y añadiendolas al diccionario
    for fila in filas:
        nueva_mesa = Mesa(numero = fila['numero'], capacidad = fila['capacidad'], estado = fila['estado'])
        diccionario_mesas[nueva_mesa.numero] = nueva_mesa
    return diccionario_mesas

def crear_tabla_alergeno() -> None:
    """
    Crea la tabla de los alérgenos
    """
    cur.execute("CREATE TABLE alergeno(id integer primary key, nombre varchar(25) not null)")
    con.commit()

def insertar_alergeno(alergeno: Alergeno) -> None:
    """
    Inserta un nuevo alergeno en la base de datos
    """
    cur.execute("INSERT INTO alergeno(nombre) VALUES(?)", (alergeno.nombre,))
    alergeno.id = cur.lastrowid
    con.commit()
    
def borrar_alergeno(alergeno: Alergeno) -> None:
    """
    Borra el alérgeno de la base de datos
    """
    cur.execute("DELETE FROM alergeno WHERE id = ?", (alergeno.id,))
    con.commit()

def obtener_alergenos() -> dict[int, Alergeno]:
    # Obtenemos todos los registros de alergeno
    cur.execute("SELECT id, nombre FROM alergeno")
    filas = cur.fetchall()

    diccionario_alergenos = {}

    # Recorremos los registros, instanciando los alergenos y lo vamos añadiendo al diccionario
    for fila in filas:
        nuevo_alergeno = Alergeno(id = fila['id'], nombre = fila['nombre'])
        diccionario_alergenos[nuevo_alergeno.id] = nuevo_alergeno
    return diccionario_alergenos

def crear_tabla_producto() -> None:
    """
    Crea la tabla de los productos
    """
    cur.execute("""
                CREATE TABLE producto(
                    codigo integer PRIMARY KEY, 
                    nombre varchar(25) NOT NULL UNIQUE,
                    precio numeric NOT NULL, 
                    disponibilidad varchar(15) NOT NULL
                )
                """)
    con.commit()

def insertar_producto(producto: Producto) -> None:
    """
    Inserta el producto en la base de datos.
    """
    cur.execute("INSERT INTO producto(nombre, precio, disponibilidad) VALUES(?, ?, ?)", (producto.nombre, producto.precio, producto.disponibilidad))
    producto.codigo = cur.lastrowid

def modificar_producto(producto: Producto) -> None:
    """
    Actualiza el producto en la base de datos con los datos actuales.
    """
    cur.execute("UPDATE producto SET nombre = ?, precio = ?, disponibilidad = ? WHERE codigo = ?", (producto.nombre, producto.precio, producto.disponibilidad, producto.codigo))

def borrar_producto(producto: Producto) -> None:
    """
    Borra el producto de la base de datos
    """
    cur.execute("DELETE FROM producto WHERE codigo = ?", (producto.codigo,))
    con.commit()

def obtener_productos() -> dict[int, Producto]:
    # Obtenemos todos los registros de producto
    cur.execute("SELECT codigo, nombre, precio, disponibilidad FROM producto")
    filas = cur.fetchall()

    diccionario_productos = {}

    # Recorremos todos los registros, instanciamos los productos y los añadimos al diccionario
    for fila in filas:
        alergenos_producto = obtener_alergenos_producto(fila['codigo'])
        nuevo_producto = Producto(codigo = fila['codigo'], 
                                  nombre = fila['nombre'], 
                                  precio = fila['precio'], 
                                  disponibilidad = fila['disponibilidad'], 
                                  alergenos = alergenos_producto)
        diccionario_productos[nuevo_producto.codigo] = nuevo_producto
    return diccionario_productos

def crear_tabla_alergeno_producto() -> None:
    """
    Crea la tabla alergeno_producto.
    """
    cur.execute("""
                CREATE TABLE alergeno_producto(
                    id_alergeno int REFERENCES alergeno(id) ON DELETE CASCADE, 
                    codigo_producto int REFERENCES producto(codigo) ON DELETE CASCADE,
                CONSTRAINT pk_alergeno_producto PRIMARY KEY(id_alergeno, codigo_producto)
                )
                """)
    con.commit()
    
def insertar_alergeno_producto(alergeno: Alergeno, producto: Producto) -> None:
    """
    Inserta el alergeno del producto en la base de datos.
    """
    cur.execute("INSERT INTO alergeno_producto(id_alergeno, codigo_producto) VALUES(?, ?)", (alergeno.id, producto.codigo))

def actualizar_todos_alergeno_producto(producto: Producto):
    """
    Actualiza todos los alergenos de un producto en la base de datos, si no hay ninguno los inserta.
    """
    try:
        # Borramos todos los alergenos de ese producto
        cur.execute("DELETE FROM alergeno_producto WHERE codigo_producto = ?", (producto.codigo,))

        # Si tiene alergenos se insertan los nuevos
        if producto.alergenos != {}:
            datos_a_insertar = [(alergeno.id, producto.codigo) for alergeno in producto.alergenos.values()]
            cur.executemany("INSERT INTO alergeno_producto(id_alergeno, codigo_producto) VALUES(?, ?)", datos_a_insertar)

    except sqlite3.Error as e:
        con.rollback()
        raise Exception(f"Error crítico al actualizar la receta en la BD: {e}")

def borrar_alergeno_producto(alergeno: Alergeno, producto: Producto) -> None:
    """ 
    Borra el alergeno de la base de datos
    """
    cur.execute("DELETE FROM alergeno_producto WHERE id_alergeno = ? AND codigo_producto = ?", (alergeno.id, producto.codigo))

def obtener_alergenos_producto(codigo_producto: int) -> dict[int, Alergeno]:
    """
    Devuelve todos los alergenos de ese producto en forma de diccionario
    """
    # Obtenemos todos los registros de alergeno que tenga ese producto
    cur.execute("""
                SELECT 
                    ap.id_alergeno, 
                    ap.codigo_producto, 
                    a.nombre 
                    FROM alergeno_producto ap JOIN alergeno a ON (ap.id_alergeno = a.id) 
                    WHERE ap.codigo_producto = ?
                """, (codigo_producto,))
    filas = cur.fetchall()

    diccionario_alergenos_producto = {}

    # Vamos recorriendo los registros, instanciando los alergenos y añadiendolos al diccionario
    for fila in filas:
        nuevo_alergeno_producto = Alergeno(id = fila['id_alergeno'], nombre = fila['nombre'])
        diccionario_alergenos_producto[nuevo_alergeno_producto.id] = nuevo_alergeno_producto
    return diccionario_alergenos_producto

def crear_tabla_pedido() -> None:
    """
    Crea la tabla pedido
    """
    cur.execute("""
                CREATE TABLE pedido(
                    numero integer primary key, 
                    numero_diario int not null,
                    num_mesa int NOT NULL REFERENCES mesa(numero), 
                    fecha date DEFAULT current_date,
                    propina numeric,
                    estado varchar(15) not null)""")
    con.commit()

def insertar_pedido(pedido: Pedido) -> None:
    """
    Inserta el pedido en la base de datos
    """
    # Calculamos el numero diario del pedido viendo el último pedido de hoy, si no hay resultado se asigna 1
    cur.execute("SELECT MAX(numero_diario) FROM pedido WHERE fecha = CURRENT_DATE")
    resultado = cur.fetchone()[0]
    if resultado is None:
        nuevo_numero_diario = 1
    else:
        nuevo_numero_diario = resultado + 1

    # Insertamos el pedido
    cur.execute("INSERT INTO pedido(numero_diario, num_mesa, estado) VALUES(?, ?, ?)", (nuevo_numero_diario, pedido.mesa.numero, pedido.estado))
    pedido.numero_diario, pedido.numero = nuevo_numero_diario, cur.lastrowid

def borrar_pedido(pedido: Pedido) -> None:
    """
    Borra el pedido de la base de datos
    """
    cur.execute("DELETE FROM pedido WHERE numero = ?", (pedido.numero,))

def obtener_pedidos() -> dict[int, Pedido]:
    """
    Recupera todos los pedidos de la base de datos, reconstruyendo 
    correctamente el objeto Mesa asociado a cada uno mediante un JOIN.
    """
    # Obtenemos los registros de pedido, y el registro de la mesa asignada a cada pedido.
    cur.execute("""
                SELECT 
                    p.numero AS ped_numero, 
                    p.numero_diario AS ped_diario, 
                    p.fecha AS ped_fecha, 
                    p.estado AS ped_estado,
                    m.numero AS mesa_numero, 
                    m.capacidad AS mesa_capacidad, 
                    m.estado AS mesa_estado
                FROM pedido p
                JOIN mesa m ON p.num_mesa = m.numero
                """)
    filas = cur.fetchall()

    diccionario_pedidos = {}

    # Vamos recorriendo los registros instanciando las mesas, instanciamos los pedidos
    # usando las mesas y vamos añadiendo los pedidos al diccionario.
    for fila in filas:
        mesa_real = Mesa(
            numero = fila['mesa_numero'], 
            capacidad = fila['mesa_capacidad'], 
            estado = fila['mesa_estado']
        )
        nuevo_pedido = Pedido(
            numero = fila['ped_numero'], 
            numero_diario = fila['ped_diario'], 
            mesa = mesa_real, 
            fecha = fila['ped_fecha'], 
            estado = fila['ped_estado']
        )
        cargar_lineas_en_pedido(nuevo_pedido)
        diccionario_pedidos[nuevo_pedido.numero] = nuevo_pedido
    return diccionario_pedidos

def obtener_pedidos_activos() -> dict[int, Pedido]:
    """
    Devuelve ÚNICAMENTE los pedidos que están activos en el restaurante.
    Ideal para pintar el mapa de mesas del TPV principal.
    """
    # Obtenemos todos los registros de pedido que tengan estado 'activo'
    cur.execute("""
                SELECT 
                    p.numero AS ped_numero, p.numero_diario AS ped_diario, 
                    p.fecha AS ped_fecha, p.estado AS ped_estado,
                    m.numero AS mesa_numero, m.capacidad AS mesa_capacidad, m.estado AS mesa_estado
                FROM pedido p
                JOIN mesa m ON p.num_mesa = m.numero
                WHERE p.estado = 'activo'
                """)
    filas = cur.fetchall()

    diccionario_pedidos = {}

    # Recorremos los registros instanciamos las mesas, instanciamos los pedidos
    # usando las mesas y los vamos añadiendo los pedidos al diccionario
    for fila in filas:
        mesa_real = Mesa(numero=fila['mesa_numero'], capacidad=fila['mesa_capacidad'], estado=fila['mesa_estado'])
        nuevo_pedido = Pedido(numero=fila['ped_numero'], numero_diario=fila['ped_diario'], 
                              mesa=mesa_real, fecha=fila['ped_fecha'], estado=fila['ped_estado'])
        cargar_lineas_en_pedido(nuevo_pedido)
        diccionario_pedidos[nuevo_pedido.numero] = nuevo_pedido
    return diccionario_pedidos

def crear_tabla_detalle_pedido() -> None:
    """
    Crea la tabla detalle_pedido
    """
    cur.execute("""
                CREATE TABLE detalle_pedido(
                    num_pedido int REFERENCES pedido(numero),
                    cod_producto int REFERENCES producto(codigo),
                    cantidad int NOT NULL,
                    precio_unidad numeric NOT NULL,
                CONSTRAINT pk_detalle_pedido PRIMARY KEY(num_pedido, cod_producto)
                )
                """)
    con.commit()

def insertar_todas_lineas_pedido(pedido: Pedido) -> None:
    """
    Inserta todas las líneas del pedido
    """
    # Si el pedido no tiene lineas, se acaba la función
    if not pedido.lineas_de_pedidos:
        return
    
    # Si tiene lineas se van recorriendo e insertando en la tabla detalle_pedido, si ya están en la tabla se actualiza la cantidad y el precio.
    datos = [(pedido.numero, linea.producto.codigo, linea.cantidad, linea.producto.precio) for linea in pedido.lineas_de_pedidos]  
    cur.executemany("""
                    INSERT INTO detalle_pedido(num_pedido, cod_producto, cantidad, precio_unidad)
                    VALUES(?, ?, ?, ?) 
                    ON CONFLICT(num_pedido, cod_producto)
                    DO UPDATE SET 
                        cantidad = excluded.cantidad,
                        precio_unidad = excluded.precio_unidad
                    """, datos)
    
def insertar_detalle_pedido(pedido: Pedido, linea_pedido: Linea_pedido) -> None:
    """
    Inserta la linea de pedido en la base de datos
    """
    cur.execute("""
                INSERT INTO detalle_pedido(num_pedido, cod_producto, cantidad, precio_unidad)
                VALUES(?, ?, ?, ?) 
                ON CONFLICT(num_pedido, cod_producto)
                DO UPDATE SET 
                cantidad = excluded.cantidad,
                precio_unidad = excluded.precio_unidad
                """, (pedido.numero, linea_pedido.producto.codigo, linea_pedido.cantidad, linea_pedido.producto.precio))

def borrar_detalle_pedido(pedido: Pedido, linea_pedido: Linea_pedido) -> None:
    cur.execute("DELETE FROM detalle_pedido WHERE num_pedido = ? AND cod_producto = ?", (pedido.numero, linea_pedido.producto.codigo))

def cargar_lineas_en_pedido(pedido: Pedido) -> None:
    """
    Busca en la BD las líneas de este pedido y las guarda 
    dentro del pedido usando tu método 'agregar_linea_pedido'.
    """
    # Buscamos en detalle_pedido todos los registros que pertenezcan a ese pedido
    cur.execute("""
                SELECT dp.cantidad, dp.precio_unidad, p.codigo, p.nombre, p.disponibilidad 
                FROM detalle_pedido dp
                JOIN producto p ON dp.cod_producto = p.codigo
                WHERE dp.num_pedido = ?
                """, (pedido.numero,))
    filas = cur.fetchall()

    # Vamos recorriendo los registros y los vamos añadiendo al pedido con agregar_linea_pedido
    for fila in filas:
        alergenos_producto = obtener_alergenos_producto(fila['codigo'])
        prod = Producto(
            codigo=fila['codigo'], 
            nombre=fila['nombre'], 
            precio=fila['precio_unidad'], 
            disponibilidad=fila['disponibilidad'],
            alergenos = alergenos_producto
        )
        pedido.agregar_linea_pedido(codigo=pedido.numero, producto=prod, cantidad=fila['cantidad'])

def transaccion_crear_producto_con_alergenos(producto: Producto) -> None:
    """
    Registra un nuevo producto en la carta junto con todos sus alérgenos asociados.
    """
    try:
        insertar_producto(producto)
        actualizar_todos_alergeno_producto(producto)
        con.commit()
    except sqlite3.Error as e:
        con.rollback()
        raise Exception(f"Error al crear el producto y sus alérgenos: {e}")
    
def transaccion_modificar_producto_con_alergenos(producto: Producto) -> None:
    """
    Actualiza los datos básicos de un producto y sincroniza sus alérgenos en la BD.
    """
    try:
        modificar_producto(producto)
        actualizar_todos_alergeno_producto(producto)
        con.commit()
    except sqlite3.Error as e:
        con.rollback()
        raise Exception(f"Error al modificar el producto: {e}")
    
def transaccion_abrir_pedido_nuevo(pedido: Pedido) -> None:
    """
    Crea un pedido, añade sus platos iniciales y cambia la mesa a 'ocupada'.
    """
    try:
        insertar_pedido(pedido)
        insertar_todas_lineas_pedido(pedido)
        # Cambia el estado de la mesa en la base de datos a ocupada
        cur.execute("UPDATE mesa SET estado = 'ocupada' WHERE numero = ?", (pedido.mesa.numero,))
        pedido.mesa.estado = "ocupada"
        con.commit()
    except sqlite3.Error as e:
        con.rollback()
        raise Exception(f"Error al abrir la comanda en la mesa {pedido.mesa.numero}: {e}")
    
def transaccion_actualizar_lineas_pedido(pedido: Pedido) -> None:
    """
    Actualiza o añade nuevos platos a un pedido que ya está abierto.
    """
    try:
        insertar_todas_lineas_pedido(pedido)
        con.commit()
    except sqlite3.Error as e:
        con.rollback()
        raise Exception(f"Error al añadir platos a la comanda: {e}")
    
def transaccion_finalizar_y_cobrar_pedido(pedido: Pedido) -> None:
    """
    Marca el pedido como finalizado, registra la propina y libera la mesa para nuevos clientes.
    """
    try:
        # Cambia el estado del pedido a finalizado Y guarda la propina
        cur.execute(
            "UPDATE pedido SET estado = 'finalizado', propina = ? WHERE numero = ?", 
            (pedido.propina, pedido.numero)
        )
        pedido.estado = "finalizado"
        
        # Cambia el estado de la mesa a libre
        cur.execute(
            "UPDATE mesa SET estado = 'libre' WHERE numero = ?", 
            (pedido.mesa.numero,)
        )
        pedido.mesa.estado = "libre"
        
        con.commit()
    except sqlite3.Error as e:
        con.rollback()
        raise Exception(f"Error al procesar el cobro de la mesa {pedido.mesa.numero}: {e}")

def transaccion_cambiar_de_mesa(pedido: Pedido, nueva_mesa: Mesa) -> None:
    """
    Mueve un pedido activo a una nueva mesa, liberando la antigua 
    y ocupando la nueva en un solo paso.
    """
    try:
        mesa_antigua_numero = pedido.mesa.numero
        # Cambia el pedido de mesa
        cur.execute("UPDATE pedido SET num_mesa = ? WHERE numero = ?", (nueva_mesa.numero, pedido.numero))
        # Pone el estado de la mesa anterior en libre
        cur.execute("UPDATE mesa SET estado = 'libre' WHERE numero = ?", (mesa_antigua_numero,))
        # Pone el estado de la mesa anterior en ocupado
        cur.execute("UPDATE mesa SET estado = 'ocupada' WHERE numero = ?", (nueva_mesa.numero,))
        # Se le asigna la mesa nueva al pedido
        pedido.mesa = nueva_mesa
        con.commit()
    except sqlite3.Error as e:
        con.rollback()
        raise Exception(f"No se pudo realizar el cambio de mesa: {e}")

def transaccion_crear_producto_con_alergenos(producto: Producto):
    """
    Inserta un producto y sus alérgenos asociados en una sola transacción.
    """
    try:
        # 1. Insertamos el producto base
        insertar_producto(producto) 
        
        # 2. Si el objeto producto trae alérgenos, los insertamos en la tabla intermedia
        if producto.alergenos:
            datos_a_insertar = [(id_al, producto.codigo) for id_al in producto.alergenos.keys()]
            cur.executemany("INSERT INTO alergeno_producto(id_alergeno, codigo_producto) VALUES(?, ?)", datos_a_insertar)
        
        con.commit()
        return producto.codigo
    except sqlite3.Error as e:
        con.rollback()
        raise Exception(f"Error al guardar producto y alérgenos: {e}")

def cerrar_bd():
    global con
    if con:
        con.close()

if __name__ == '__main__':
    abrir_db()

    """
    alergeno_gluten = Alergeno(id=1, nombre="Gluten")
    alergeno_lacteos = Alergeno(id=2, nombre="Lácteos")

    tarta_queso = Producto(
        codigo=1,
        nombre="Tarta de Queso Casera",
        precio=5.50,
        alergenos={
            alergeno_lacteos.id: alergeno_lacteos, 
            alergeno_gluten.id: alergeno_gluten
        }
    )

    ensalada_mixta = Producto(
        nombre="Ensalada Mixta",
        precio=7.00,
        alergenos={}  # Diccionario vacío, sin alérgenos
    )

    id_buscar = 4

    if id_buscar in tarta_queso.alergenos:
        print(f"¡Cuidado! {tarta_queso.nombre} contiene Gluten.")
    else:
        print(f"{tarta_queso.nombre} es apto para celíacos.")

    actualizar_todos_alergeno_producto(tarta_queso)

    for producto in obtener_productos().values():
        print(producto)

    for mesa in obtener_mesas().values():
        print(mesa)
    
    for alergeno in obtener_alergenos().values():
        print(alergeno)

    print(obtener_alergenos_producto(1))
    """

    p = Pedido(mesa = 5)

    for pedido in obtener_pedidos().values():
        print(pedido.estado)

    for mesa in obtener_mesas().values():
        print(mesa)

    cerrar_bd()