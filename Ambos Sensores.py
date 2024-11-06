from machine import Pin, time_pulse_us
import utime
import time

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

# Función para detectar el color y madurez del tomate
def detectar_madurez():
    rojo = get_rojo()
    verde = get_verde()
    azul = get_azul()
    
    print(f"Intensidad R: {rojo:.2f} -- Intensidad G: {verde:.2f} -- Intensidad B: {azul:.2f}")
    
    if 200 < rojo < 400 and rojo > azul > verde and azul < 150 and verde < 150:
        print("Estado: Tomate Maduro (Rojo Intenso)")
    elif 70 < rojo < 99 and 59 < verde < 90 and 60 < azul < 90:
        print("Estado: Negro (Muy Bajo Reflejo)")
    elif verde > rojo and verde > azul and verde > 20:
        print("Estado: Tomate Verde")
    elif rojo < 15 and verde < 20:
        print("Estado: Tomate en Maduración (Verde Claro)")
    elif 15 <= rojo <= 20 and verde < 15:
        print("Estado: Tomate a Medio Madurar (Amarillento)")
    elif 20 < rojo < 30 and verde < 10:
        print("Estado: Tomate Casi Maduro (Naranja)")
    else:
        print("Estado: Indeterminado o Color No Registrado")

# Bucle principal
while True:
    # Detectar madurez del tomate
    detectar_madurez()
    
    # Medir la distancia
    distancia = medir_distancia()
    tamano = (80 - distancia * 5) / 5
    print(f"Tamaño del Tomate : {tamano:.2f} cm")
    
    utime.sleep(1)
 