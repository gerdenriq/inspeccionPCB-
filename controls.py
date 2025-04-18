import RPi.GPIO as GPIO
import time
import sys
import board
import busio
import adafruit_vl53l0x

# Pines en modo BCM
IN1 = 23
IN2 = 24

# Configuración inicial de GPIO
def configurar_gpio():
    GPIO.cleanup()
    time.sleep(0.1)
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)

# Configurar sensor VL53L0X
def configurar_sensor():
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_vl53l0x.VL53L0X(i2c)
    sensor.start_continuous()
    return sensor

# Parámetros de control
RANGO_MINIMO = 100  # mm
RANGO_MAXIMO = 237  # mm
histeresis = 5  # mm

# Función para establecer el setpoint asegurando que esté dentro del rango
def establecer_setpoint(setpoint):
    if setpoint < RANGO_MINIMO:
        setpoint = RANGO_MINIMO
    elif setpoint > RANGO_MAXIMO:
        setpoint = RANGO_MAXIMO
    return setpoint

# Funciones de control del actuador
def detener():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    print("Detenido")

def moverAdelante():
    detener()  # Detener el actuador antes de mover
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    print("Moviendo adelante")

def moverAtras():
    detener()  # Detener el actuador antes de mover
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    print("Moviendo atrás")

# Función para controlar el actuador según la distancia del sensor
def control_actuador(sensor, setpoint, histeresis):
    distance = sensor.range - 23  # Leer la distancia del sensor
    print(f"Distancia: {distance} mm")

    # Control por histéresis
    if distance < (setpoint - histeresis):
        moverAdelante()
    elif distance > (setpoint + histeresis):
        moverAtras()
    else:
        detener()

# Función principal
def main():
    configurar_gpio()  # Configuración de los pines GPIO
    sensor = configurar_sensor()  # Configuración del sensor VL53L0X
    setpoint = 100  # Valor inicial de distancia deseada en mm
    setpoint = establecer_setpoint(setpoint)  # Establecer el setpoint dentro del rango

    print("Controlando distancia...")

    try:
        while True:
            control_actuador(sensor, setpoint, histeresis)  # Controlar el actuador según la lectura del sensor
            time.sleep(0.7)

    except KeyboardInterrupt:
        print("\nInterrumpido con Ctrl+C. Saliendo...")

    finally:
        detener()
        GPIO.cleanup()

# Ejecutar el código
if __name__ == "__main__":
    main()
