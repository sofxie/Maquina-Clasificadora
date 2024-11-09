import socket

class servidor:
    def __init__(self, IP, port, controlador):
        self.host = IP
        self.port = port
        self.conn = None
        self.controlador = controlador
        self.peq = 10
        self.mid = 20
    def start_server(self):
        # Crear un socket de tipo TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Vincular el socket a la dirección y puerto especificados
            server_socket.bind((self.host, self.port))
            # Escuchar conexiones entrantes
            server_socket.listen()

            print(f'Servidor escuchando en {self.host} : {self.port}')

            while True:
                # Aceptar una nueva conexión
                self.conn, self.addr = server_socket.accept()
                print(f'Conexión establecida por {self.addr}')

                # Iniciar comunicación continua con el cliente
                self.handle_client()

    def handle_client(self):
        try:
            # Enviar mensaje de bienvenida
            self.conn.sendall(b'Hola, cliente! Has conectado al servidor.\n')
            while True:
                # Recibir datos del cliente
                data = self.conn.recv(1024)
                self.proyectar_respuesta(data.decode().strip())
                if not data:
                    print("Cliente desconectado.")
                    self.conn.close()  # Cerrar conexión
                    self.conn = None  # Restablecer a None
                    break
                print(f'Datos recibidos: {data.decode()}')

        except Exception as e:
            print(f"Error en la conexión: {e}")
            if self.conn:
                self.conn.close()
            self.conn = None  # Restablecer conexión a None si hay error

    def mandaralcliente(self, m):
        if self.conn:
            try:
                # Enviar mensaje al cliente
                self.conn.sendall(m.encode())
                print("Mensaje enviado al cliente.")
            except Exception as e:
                print(f"Error al enviar mensaje: {e}")
        else:
            print("No hay conexión activa con el cliente.")

    def proyectar_respuesta(self,data):
        m, t = data.split(",")  # Separar por coma
        print(f"Comando: {m} Valor: {t}")
        if m == "Maduro":
            estado = "Tomate Maduro"
        elif m == "Verde":
            estado = "Tomate Verde"
        elif m == "Malo":
            estado = "Producto Malo"
        else:
            estado = "Indeterminado"

        if self.peq > int(t):
            tamano = "Pequeño"
        elif self.mid > int(t) > self.peq:
            tamano = "Mediano"
        else:
            tamano = "Grande"
        return self.controlador.mostrar(estado,tamano)