from machine import Pin, time_pulse_us
import utime
import socket
import time
import network

# Pines para el sensor de color TCS3200
s0 = Pin(14, Pin.OUT)
s1 = Pin(15, Pin.OUT)
s2 = Pin(17, Pin.OUT)
s3 = Pin(16, Pin.OUT)
out = Pin(18, Pin.IN)

# Pines para el sensor de ultrasonido
trig_pin = Pin(21, Pin.OUT)  # Pin GP21
echo_pin = Pin(20, Pin.IN)   # Pin GP20

# Configuración inicial del sensor de color
s0.value(1)
s1.value(1)

# Velocidad del sonido en cm/us
SOUND_SPEED = 340  # en m/s, ajustado a cm/us

# Socket
host = '172.20.10.12' # Cambiar IP
port = 65432

# Setup Wi-Fi
ssid = "Sof" # Nombre del WIFI
password = "88888888" # Clave del WIFI

class WIFI:
    def conectarWIFI():
        try: 
            wlan = network.WLAN(network.STA_IF)
            wlan.active(False)  # Desactiva el Wi-Fi
            time.sleep(1)       # Pausa un segundo
            wlan.active(True)    # Reactiva el Wi-Fi
            wlan.connect(ssid, password)
            
            retry_count = 0
            while not wlan.isconnected() and retry_count < 10:
                print(f"[WLAN] Intentando conectar... intento {retry_count + 1}")
                time.sleep(1)
                retry_count += 1
            
            if wlan.isconnected():
                print("Conexión exitosa a Wi-Fi:", wlan.ifconfig())
            else:
                print("Error: No se pudo conectar a la red Wi-Fi.")
        except Exception as e:
            print(f"Error al intentar conectar Wi-Fi: {e}")

# Función para medir frecuencia de color
def get_pulse_count():
    start = utime.ticks_us()
    pulse_count = 0
    while pulse_count < 100:
        while out.value() == 1:
            pass
        while out.value() == 0:
            pass
        pulse_count += 1
    duration = utime.ticks_diff(utime.ticks_us(), start)
    return 1000000 / duration  # Frecuencia en Hz

# Funciones para leer cada color
def get_rojo():
    s2.value(0)
    s3.value(0)
    utime.sleep(0.1)
    return get_pulse_count()

def get_verde():
    s2.value(1)
    s3.value(1)
    utime.sleep(0.1)
    return get_pulse_count()

def get_azul():
    s2.value(0)
    s3.value(1)
    utime.sleep(0.1)
    return get_pulse_count()

# Función para medir la distancia usando el sensor de ultrasonido
def medir_distancia():
    trig_pin.value(0)
    time.sleep_us(5)
    trig_pin.value(1)
    time.sleep_us(10)
    trig_pin.value(0)
    
    ultrason_duration = time_pulse_us(echo_pin, 1, 30000)
    distance_cm = SOUND_SPEED * ultrason_duration / 20000  # Calcula la distancia en cm
    return distance_cm

def detectar_madurez():
    rojo = get_rojo()
    verde = get_verde()
    azul = get_azul()
    
    print(f"Intensidad R: {rojo:.2f} -- Intensidad G: {verde:.2f} -- Intensidad B: {azul:.2f}")
    
    if 200 < rojo < 400 and rojo > azul > verde and azul < 150 and verde < 150:
        print("Estado: Tomate Maduro (Rojo Intenso)")
        estado = "Maduro"
    elif 70 < rojo < 99 and 59 < verde < 90 and 60 < azul < 90:
        print("Estado: Tomate Malo")
        estado = "Malo"
    elif verde > rojo and verde > azul and verde > 20:
        print("Estado: Tomate Verde")
        estado = "Verde"
    else:
        print("Estado: Indeterminado o Color No Registrado")
        estado = "Indeterminado"
    return estado

# Función para manejar la comunicación con el servidor
def recibir_mensajes(client_socket):
    try:
        while True:
            respuesta = client_socket.recv(1024)
            if not respuesta:
                print("Conexión cerrada por el servidor.")
                break
            if respuesta.decode() == "color":
                # Detectar madurez del tomate
                estado = detectar_madurez()
    
                # Medir la distancia
                distancia = medir_distancia()
                tamano = (80 - distancia * 5) / 5
                
                print(f"Tamaño del Tomate : {tamano:.2f} cm")
                tamano = int(tamano)
                answer = f"{estado},{tamano}"
                print(f"{answer}")
                client_socket.send(f"{answer}".encode())
            print(f"Servidor: {respuesta.decode()}")
    except Exception as e:
        print(f"Error recibiendo datos: {e}")
    finally:
        client_socket.close()
        
def iniciar_cliente():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print("Conexión al servidor establecida.")
        
        # Recibir mensaje de bienvenida del servidor
        respuesta = client_socket.recv(1024)
        print("Respuesta del servidor:", respuesta.decode())
        
        # Entrar en un bucle para recibir y enviar mensajes de forma continua
        while True:
            recibir_mensajes(client_socket)
            time.sleep(1)  # Evita bucle rápido
            
    except OSError as e:
        print(f"Error en la conexión al socket: {e}")
    finally:
        if client_socket:
            client_socket.close()
            print("Conexión cerrada con el servidor.")

if __name__ == '__main__':
    # Intentar conectar al Wi-Fi
    WIFI.conectarWIFI()
    
    iniciar_cliente()
