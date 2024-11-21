import threading
import importlib
import Interfaz
importlib.reload(Interfaz)
from Interfaz import ventana

from Logica import servidor


class controlador:
    def __init__(self, ip, port, tventana):
        self.servidor = servidor(ip, port, self)
        self.ventana = ventana(tventana, self)  # Pasar los parámetros correctamente
        self.Tresultado = False  # Variable para almacenar el estado actual
        print(f"Margenes cargados: {self.ventana.margenes}")


        # Inicializar márgenes desde la interfaz
        self.margenes = self.ventana.margenes

        # Pasar márgenes al servidor lógico
        self.actualizar_margenes()

    # Método para enviar márgenes actualizados al servidor lógico
    def actualizar_margenes(self):
        self.servidor.peq = self.margenes["peq"]
        self.servidor.mid = self.margenes["mid"]
        self.servidor.max = self.margenes["max"]

    def iniciarVentana(self): # Iniciar Interfaz
        self.ventana.mostrar()
        self.actualizar_margenes()  # Sincronizar márgenes al iniciar

    def mostrarArchivo(self, archivo):
        print("TXTC")
        self.ventana.mostrarResultado(archivo)

    def iniciarServidor(self):
        server_thread = threading.Thread(target=self.servidor.start_server)
        server_thread.daemon = True  # Para que el hilo se cierre con la aplicación
        server_thread.start()

    def ejecutar(self):
        # Ejecuta el servidor y la interfaz juntos
        self.iniciarServidor()
        self.iniciarVentana()

    def actualizar_Tresultado(self, valor):
        self.Tresultado = valor  # Actualiza el valor local de Tresultado

    def enviarmensaje(self, mensaje):
        self.servidor.mandaralcliente(mensaje)

    def mostrarTabla(self, Tresultado, Promedio, Tabla):
        self.ventana.actualizarTabla(Tresultado,Promedio,Tabla)

    def mostrar(self,estado,tamano):
        self.ventana.resultado(estado,tamano)

if __name__ == "__main__":
    Controlador = controlador("192.168.124.9", 65432,"1200x800") # Cambiar el IP
    Controlador.ejecutar()
