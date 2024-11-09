import threading
from Interfaz import ventana
from Logica import servidor

class controlador:
    def __init__(self, ip, port, tventana):
        self.servidor = servidor(ip, port, self)
        self.ventana = ventana(tventana, self)

    def iniciarVentana(self):
        self.ventana.mostrar()

    def iniciarServidor(self):
        server_thread = threading.Thread(target=self.servidor.start_server)
        server_thread.daemon = True  # Para que el hilo se cierre con la aplicación
        server_thread.start()

    def ejecutar(self):
        # Ejecuta el servidor y la interfaz juntos
        self.iniciarServidor()
        self.iniciarVentana()

    def enviarmensaje(self, mensaje):
        self.servidor.mandaralcliente(mensaje)

    def mostrar(self,estado,tamano):
        self.ventana.resultado(estado,tamano)

if __name__ == "__main__":
    Controlador = controlador("192.168.124.6", 65432,"1200x800") # Cambiar el IP
    Controlador.ejecutar()

