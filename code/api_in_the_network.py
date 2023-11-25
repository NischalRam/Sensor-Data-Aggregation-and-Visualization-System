#In this program we are creating our network called nischal. 
#if we hit the rooturl it will display the json data

import network
import socket
from machine import Pin, I2C
from time import sleep
from bme680 import *
import json

# ESP32 - Pin assignment
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
bme = BME680_I2C(i2c=i2c)

# Sleep duration for BME sensor (5 seconds)
SENSOR_SLEEP_DURATION = 3

# Sleep duration for main loop (1 second)
MAIN_LOOP_SLEEP_DURATION = 1

def generate_json_data():
    return {
        "temperature": round(bme.temperature, 2),
        "humidity": round(bme.humidity, 2),
        "pressure": round(bme.pressure, 2),
        "gas": round(bme.gas / 1000, 2)
    }

def ap_mode(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    while not ap.active():
        pass

    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to:', ap.ifconfig()[0])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        # Sleep for BME sensor data acquisition
        sleep(SENSOR_SLEEP_DURATION)

        conn, addr = s.accept()
        print('Got a connection from', addr)
        request = conn.recv(1024)
        print('Content =', request)

        response = 'HTTP/1.1 200 OK\n'
        response += 'Content-Type: application/json\n'
        response += 'Connection: close\n\n'
        response += json.dumps(generate_json_data())
        conn.send(response)

        conn.close()

        # Sleep for the main loop
        sleep(MAIN_LOOP_SLEEP_DURATION)

ap_mode('nischal', 'password')

