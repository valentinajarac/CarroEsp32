import machine
import time
import network
import umail

miRed = None  # Declarar miRed fuera de la función conectaWifi

def conectaWifi(red, password):
    global miRed  # Utilizar la variable global miRed
    miRed = network.WLAN(network.STA_IF)
    if not miRed.isconnected():
        miRed.active(True)
        miRed.connect(red, password)
        print('Conectando a la red', red + '...')
        timeout = time.time()
        while not miRed.isconnected():
            if time.ticks_diff(time.time(), timeout) > 10:
                return False
    return True

# Valores a reemplazar
wifiSSID = 'MOVISTAR WIFI1910'
wifiPass = 'vhkt0974'
sender_email = 'espvalentina00@gmail.com'
sender_name = 'ESP32' #sender name
sender_app_password = 'xpokjlierotuguwf'
recipient_email = 'jakelin_bedoya82181@elpoli.edu.co'
email_subject = 'Carro a menos de 3 metros de distancia'

# Configurar los pines GPIO del sensor
TRIG_PIN = machine.Pin(5, machine.Pin.OUT)
ECHO_PIN = machine.Pin(18, machine.Pin.IN)

if conectaWifi(wifiSSID, wifiPass):
    print('Conexión exitosa!')
    if miRed is not None and miRed.isconnected():
        print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    else:
        print('Error: No se pudo establecer la conexión Wi-Fi.')
        sys.exit(1)

    try:
        while True:
            # Generar un pulso corto en el pin TRIG para iniciar la medición
            TRIG_PIN.on()
            time.sleep_us(10)
            TRIG_PIN.off()

            # Esperar hasta que el pin ECHO se active
            while not ECHO_PIN.value():
                pulse_start = time.ticks_us()

            # Esperar hasta que el pin ECHO se desactive
            while ECHO_PIN.value():
                pulse_end = time.ticks_us()

            # Calcular la duración del pulso en microsegundos
            pulse_duration = pulse_end - pulse_start

            # Calcular la distancia utilizando la velocidad del sonido
            speed_of_sound = 34300  # cm/s (velocidad del sonido en cm/s)
            distance = (pulse_duration * speed_of_sound) / (2 * 1000000)  # Convertir a segundos

            # Imprimir la distancia medida en centímetros
            print('Distancia: {} centímetros'.format(distance))

            if distance < 3:
                # Enviar correo electrónico de alerta
                smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True) # Gmail's SSL port
                smtp.login(sender_email, sender_app_password)
                smtp.to(recipient_email)
                smtp.write('From:' + sender_name + '<' + sender_email + '>\n')
                smtp.write('Subject:' + email_subject + '\n')
                smtp.write('Alert: Object detected within 3 meters')
                smtp.send()
                smtp.quit()

            time.sleep(10)  # Esperar 10 segundos entre las mediciones

    except KeyboardInterrupt:
        # Manejar la interrupción de teclado (Ctrl+C) para finalizar el programa
        pass
