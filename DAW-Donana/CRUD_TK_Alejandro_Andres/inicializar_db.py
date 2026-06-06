import TPV_base_datos as db
from TPV_modelo import Alergeno

db.abrir_db()

db.crear_tabla_mesa()
db.crear_tabla_alergeno()
db.crear_tabla_producto()
db.crear_tabla_alergeno_producto()
db.crear_tabla_pedido()
db.crear_tabla_detalle_pedido()

ALERGENOS_UE = [
    "Gluten", "Crustáceos", "Huevos", "Pescado", "Cacahuetes", 
    "Soja", "Lácteos", "Frutos de cáscara", "Apio", "Mostaza", 
    "Sésamo", "Sulfitos", "Altramuces", "Moluscos"
]

for alergeno in ALERGENOS_UE:
    db.insertar_alergeno(Alergeno(alergeno))


db.cur.execute('INSERT INTO mesa (numero, capacidad, estado) values(0, 0, "libre")')


db.con.commit()

db.cerrar_bd()