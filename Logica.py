import socket

class servidor:
    def __init__(self, IP, port, controlador):
        self.host = IP
        self.port = port
        self.conn = None
        self.controlador = controlador
        self.peq = 2
        self.mid = 6
        self.Total = 0
        self.TamanoT = 0
        self.PromedioT = 0
        self.PromedioP = 0
        self.TablaPapa = [0, 0, 0, 0]  # [Bueno Grande, Defectuoso Grande, Bueno Pequeño, Defectuoso Pequeño]
        self.TablaTomate = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
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
                self.proyectar_respuesta(data.decode().strip(), self.controlador.Tresultado)
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

    def proyectar_respuesta(self, data, Tresultado): # Toma el dato de la raspy
        try:
            print(Tresultado)
            m, t = data.split(",")  # Separar por coma
            print(f"Estado: {m} Valor: {t}")
            if Tresultado == True:
                if m == "Maduro":
                    estado = "Tomate Maduro"
                elif m == "Verde":
                    estado = "Tomate Verde"
                elif m == "Malo":
                    estado = "Producto Defectuoso"
                else:
                    estado = "Indeterminado"

                if self.peq > int(t):
                    tamano = "Pequeño"
                elif self.mid > int(t) > self.peq:
                    tamano = "Mediano"
                else:
                    tamano = "Grande"
            else:
                if m == "Malo":
                    estado = "Producto Defectuoso"
                else:
                    estado = "Papa Bueno"

                if self.peq > int(t):
                    tamano = "Pequeño"
                else:
                    tamano = "Grande"

            self.controlador.mostrar(estado, tamano)
            self.AnalisisResultado(Tresultado,estado, tamano,t)

        except ValueError:
            print("Error: formato de datos incorrecto. Se esperaba 'comando,valor'.")
            if self.conn:
                self.conn.sendall(b"Formato incorrecto, se esperaba 'comando,valor'.\n")

    def AnalisisResultado(self, Tresultado, estado, tamano, t):
        if Tresultado == True:
            if estado == "Tomate Maduro":
                if tamano == "Pequeño":
                    self.TablaTomate[0][0] += 1
                elif tamano == "Mediano":
                    self.TablaTomate[0][1] += 1
                elif tamano == "Grande":
                    self.TablaTomate[0][2] += 1
            elif estado == "Tomate Verde":
                if tamano == "Pequeño":
                    self.TablaTomate[1][0] += 1
                elif tamano == "Mediano":
                    self.TablaTomate[1][1] += 1
                elif tamano == "Grande":
                    self.TablaTomate[1][2] += 1
            elif estado == "Producto Defectuoso":
                if tamano == "Pequeño":
                    self.TablaTomate[2][0] += 1
                elif tamano == "Mediano":
                    self.TablaTomate[2][1] += 1
                elif tamano == "Grande":
                    self.TablaTomate[2][2] += 1
            self.Total = sum(sum(row) for row in self.TablaTomate)
            self.TamanoT += int(t)
            self.PromedioT = self.TamanoT / self.Total
            self.controlador.mostrarTabla(Tresultado, self.PromedioT, self.TablaTomate)
        else:
            if estado == "Papa Bueno" and tamano == "Grande":
                self.TablaPapa[0] = self.TablaPapa[0] +  1
                self.Total = self.Total + 1
            elif estado == "Producto Defectuoso" and tamano == "Grande":
                self.TablaPapa[1] = self.TablaPapa[1] +  1
                self.Total = self.Total + 1
            elif estado == "Papa Bueno" and tamano == "Pequeño":
                self.TablaPapa[2] = self.TablaPapa[2] +  1
                self.Total = self.Total + 1
            else:
                self.TablaPapa[3] = self.TablaPapa[3] +  1
                self.Total = self.Total + 1
            self.TamanoT += int(t)
            print(self.TamanoT)
            self.PromedioP = self.TamanoT / self.Total
            self.controlador.mostrarTabla(Tresultado, self.PromedioP, self.TablaPapa)