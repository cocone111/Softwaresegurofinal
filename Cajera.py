import time
import threading

class Cajera(threading.Thread):
    def __init__(self, nombre, cola_clientes):
        threading.Thread.__init__(self)
        self.nombre = nombre
        self.cola_clientes = cola_clientes

    def run(self):
        while True:
            cliente = self.cola_clientes.get()
            if cliente is None:
                break
            self.procesar_compra(cliente)
            self.cola_clientes.task_done()

    def procesar_compra(self, cliente):
        print(f"{self.nombre} está procesando la compra de {cliente.nombre}")
        total = 0
        for producto in cliente.productos:
            print(f"{self.nombre} está escaneando {producto}")
            time.sleep(1)  # Simulando el tiempo de escaneo
            total += producto.precio
        print(f"{self.nombre} ha terminado de procesar la compra de {cliente.nombre}. Total: ${total:.2f}")