"""
Modelo de un restaurante
"""

from typing import Iterator

class Mesa:
    """Clase que define una mesa mediante su número 
        y el número de comensales que permite tener la mesa como capacidad"""


    def __init__(self,  capacidad: int, estado: str|None = 'libre', numero: int|None = None) -> None:
        self.numero = numero
        self.capacidad = capacidad
        self.estado = estado

    def __str__(self) -> str:
        return f'La mesa número {self.__numero} tiene capacidad para {self.capacidad} comensales, esta {self.estado}'

    @property
    def estado(self):
        return self.__estado

    @property
    def numero(self) -> int:
        return self.__numero
    
    @property
    def capacidad(self) -> int:
        return self.__capacidad
    
    @capacidad.setter
    def capacidad(self, comensales: int) -> None:
        self.__capacidad = comensales

    @numero.setter
    def numero(self, nuevo_numero: int):
        self.__numero = nuevo_numero
        
    @estado.setter
    def estado(self, nuevo_estado:str):
        self.__estado = nuevo_estado

        
    def liberar_mesa(self):
        self.__estado = 'libre'

    def ocupar_mesa(self):
        self.__estado = 'ocupada'


class Alergeno:

    """Clase que define el alergeno que tiene un producto"""

    def __init__(self, nombre: str, id: int|None = None) -> None:
        self.id = id
        self.nombre = nombre

    def __str__(self) -> str:
        return f'Alergeno {self.id}, {self.nombre}'
    
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @id.setter
    def id(self, nuevo_id: int):
        self.__id = nuevo_id
    
    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        self.__nombre = nuevo_nombre
    


class Producto:

    """Clase que define un producto y los alergenos que tiene"""

    def __init__(self, nombre:str, precio: float, alergenos:dict[Alergeno],  disponibilidad: str|None = 'Disponible',  codigo: int | None = None) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.__precio = precio
        self.__alergenos = alergenos
        self.__disponibilidad: str ['Disponible'|'Agotado'|'No disponible'] = disponibilidad

    def __str__(self) -> str:
        return f'El producto número {self.codigo} se llama {self.nombre}, tiene precio {self.precio} y los alergenos {self.alergenos}  '

    @property
    def disponibilidad(self) -> str:
        return self.__disponibilidad

    @disponibilidad.setter
    def disponibilidad(self, nueva_disponibilidad) -> str:
        self.__disponibilidad = nueva_disponibilidad 

    @property
    def codigo(self) -> int:
        return self.__codigo
    
    @codigo.setter
    def codigo(self, nuevo_codigo: int):
        self.__codigo = nuevo_codigo
    
    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre
    
    @property
    def precio(self) -> float:
        return self.__precio
    
    @precio.setter
    def precio(self, nuevo_precio:float):
        self.__precio = nuevo_precio

    @property
    def alergenos(self) -> dict[Alergeno]:
        return self.__alergenos
    
    @alergenos.setter
    def alergenos(self, nuevos_alergenos: list[Alergeno]):
        self.__alergenos = nuevos_alergenos
    
    def cambiar_disponibilidad(self, opt:str) -> None:
        self.__disponibilidad = opt
    
    

class Linea_pedido:

    """Clase que contiene una linea de pedido con su producto y su cantidad"""

    def __init__(self, codigo: int, producto: Producto, cantidad:int) -> None:
        self.__producto = producto
        self.__cantidad = cantidad
        self.__codigo = codigo

    def __str__(self) -> str:
        return f'Linea de pedido {self.codigo}, tiene {self.cantidad} unidades de ({self.producto})'
    
    def __repr__(self):
        return f'Linea de pedido {self.codigo}, tiene {self.cantidad} unidades de ({self.producto})'
    

    @property
    def producto(self) -> Producto:
        return self.__producto
    
    @producto.setter
    def producto(self, nuevo_producto: Producto):
        self.__producto = nuevo_producto
    
    @property
    def cantidad(self) -> int:
        return self.__cantidad
    
    @cantidad.setter
    def cantidad(self, nueva_cantidad: int) -> None:
        self.__cantidad = nueva_cantidad

    @property
    def codigo(self) -> int:
        return self.__codigo
    
    @codigo.setter
    def codigo(self, nuevo_codigo:int):
        self.__codigo = nuevo_codigo


class Pedido:

    """Clase que define un pedido con sus lineas de pedido, y contiene la mesa asociada al pedido"""

    def __init__(self, mesa: Mesa, propina = 0.0, numero_diario: int|None = None, fecha : str|None = None, estado: str = 'activo' , numero: int|None = None) -> None:
        self.numero = numero
        self.numero_diario = numero_diario
        self.mesa = mesa
        self.fecha = fecha
        self.__lineas_de_pedidos: list[Linea_pedido] = []
        self.estado : str ['activo'|'finalizado'] = estado
        self.propina = propina

    def __iter__(self) -> Iterator:
        return iter(self.__lineas_de_pedidos)

    def __str__(self) -> str:
        return f'Pedido número: {self.numero}, es el pedido {self.numero_diario} del dia, mesa: ({self.mesa}) Propina: {self.propina}'
    
    @property
    def estado(self):
        return self.__estado
    
    @estado.setter
    def estado(self, estado) -> None:
        self.__estado = estado

    @property
    def numero(self) -> int:
        return self.__numero
    
    @numero.setter
    def numero(self, nuevo_numero:int):
        self.__numero = nuevo_numero
    
    @property
    def numero_diario(self) -> int:
        return self.__numero_diario
    
    @numero_diario.setter
    def numero_diario(self, nuevo_numero_diario: int):
        self.__numero_diario = nuevo_numero_diario

    @property
    def fecha(self) -> str:
        return self.__fecha
    
    @fecha.setter
    def fecha(self, fecha) -> None:
        self.__fecha = fecha
    
    @property
    def mesa(self) -> Mesa:
        return self.__mesa
    
    @mesa.setter
    def mesa(self, nueva_mesa: Mesa):
        self.__mesa = nueva_mesa
    
    @property
    def lineas_de_pedidos(self) -> list[Linea_pedido]:
        return self.__lineas_de_pedidos
    
    @property
    def propina(self) -> float:
        return self.__propina
    
    @propina.setter
    def propina(self, nueva_propina) -> None:
        self.__propina = nueva_propina
    
    def agregar_linea_pedido(self, codigo:int , producto: Producto, cantidad:int) -> Linea_pedido:
        for linea_pedido in self.__lineas_de_pedidos:
            if linea_pedido.producto == producto:
                linea_pedido.cantidad += cantidad
                return linea_pedido

        linea_pedido = Linea_pedido(codigo, producto, cantidad)
        self.__lineas_de_pedidos.append(linea_pedido)
        return linea_pedido

    def finalizar_pedido(self):
        self.__estado = 'finalizado'


if __name__ == '__main__':
    m = Mesa(2)
    m3 = Mesa(3)
    m2 = Mesa(2)
    p = Producto(1,'prod',10.4,{1,2})
    p2 = Producto(2, 'gu', 34,{3,5})
    a = Alergeno('cancer', 1)
    l = Linea_pedido(1, p, 2)
    ped = Pedido(100, 1, m)
    ped.agregar_linea_pedido(1, p, 2)
    ped.agregar_linea_pedido(1, p, 2)
    ped.agregar_linea_pedido(3, p2, 2)
    ped.agregar_linea_pedido(3, p2, 18)
    print(ped.lineas_de_pedidos)
    print(ped)
    p5 = Producto('f',67,[9])
    print(p5)
    p5.nombre = 'hola'
    print(p5)
    print(m)
    print(a)