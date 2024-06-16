class Cliente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def __str__(self):
        return f"Cliente {self.nombre} con {len(self.productos)} productos"