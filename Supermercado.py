import queue
from Producto import Producto
from Cliente import Cliente
from Cajera import Cajera

class Supermercado:
    def __init__(self, numero_cajeras):
        self.cola_clientes = queue.Queue()
        self.cajeras = [Cajera(f"Cajera {i+1}", self.cola_clientes) for i in range(numero_cajeras)]

    def agregar_cliente(self, cliente):
        self.cola_clientes.put(cliente)

    def iniciar_cobro(self):
        for cajera in self.cajeras:
            cajera.start()

    def finalizar_cobro(self):
        # Esperar a que todos los clientes sean procesados
        self.cola_clientes.join()
        # Detener las cajeras
        for _ in self.cajeras:
            self.cola_clientes.put(None)
        for cajera in self.cajeras:
            cajera.join()

# Ejemplo de uso
if __name__ == "__main__":
    supermercado = Supermercado(numero_cajeras=2)

    cliente1 = Cliente("Juan")
    cliente1.agregar_producto(Producto("Leche", 3.50))
    cliente1.agregar_producto(Producto("Pan", 2.00))

    cliente2 = Cliente("María")
    cliente2.agregar_producto(Producto("Arroz", 1.50))
    cliente2.agregar_producto(Producto("Huevos", 2.50))

    cliente3 = Cliente("Carlos")
    cliente3.agregar_producto(Producto("Carne", 10.00))

    supermercado.agregar_cliente(cliente1)
    supermercado.agregar_cliente(cliente2)
    supermercado.agregar_cliente(cliente3)

    supermercado.iniciar_cobro()
    supermercado.finalizar_cobro()
