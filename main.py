import keyboard
from firebase_config import firebase
import random
import serial, time

arduino = serial.Serial('COM5', 9600)

# Inicializa la luminosidad
last_luminosidad = 100

def aumentar_luminosidad(e):
    global last_luminosidad
    last_luminosidad += 10
    print("Luminosidad aumentada a: {}mW".format(last_luminosidad))

def disminuir_luminosidad(e):
    global last_luminosidad
    last_luminosidad -= 10
    print("Luminosidad disminuida a: {}mW".format(last_luminosidad))

# Asigna las funciones a las teclas de flecha
keyboard.on_press_key("up", aumentar_luminosidad)
keyboard.on_press_key("down", disminuir_luminosidad)

def on_message():
    if arduino.inWaiting() > 0:
        arduinoData = arduino.readline().decode('utf-8').strip()  # Lee los datos del puerto serial
        data = arduinoData.split('\t')  # Divide los datos en una lista

        # Verifica que los datos están en el formato esperado antes de procesarlos
        if len(data[0].split(': ')) >= 2:
            humedad = float(data[0].split(': ')[1].strip('%'))
            temperatura = float(data[1].split(': ')[1].strip('°C'))

            arduinoData2 = arduino.readline().decode('utf-8').strip()  # Lee los datos del puerto serial
            data2 = arduinoData2.split(': ')
            distancia = float(data2[1].strip(' cm'))
            last_kilowats = random.uniform(5,6)  # Genera un número aleatorio entre 0 y 10

            datos = {
                "humedad": humedad,
                "temperatura": temperatura,
                "distancia": distancia,
                "kilowats": last_kilowats,
                "luminosity": last_luminosidad
            }

            print("Humedad: {}%   Temperatura: {}°C  Distancia: {}cm Kilowatts: {}KhW  Luminosiad: {}mW".format(humedad, temperatura, distancia,last_kilowats, last_luminosidad))

            #firebase.post('/datos_sensores', datos)

while True:
    on_message()
    time.sleep(1)
