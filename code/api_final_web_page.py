from machine import Pin, I2C
from time import sleep
from bme680 import *
import network
import socket
import ujson
import urequests


led_pin = machine.Pin('LED', machine.Pin.OUT)
led_pin.value(1)

# ESP32 - Pin assignment
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
# ESP8266 - Pin assignment
# i2c = I2C(scl=Pin(5), sda=Pin(4))

bme = BME680_I2C(i2c=i2c)

history_stack = []

def api_response(temp, hum, pres, gas, max_temp, max_hum, max_pres, max_gas, mean_temp, mean_hum, mean_pres, mean_gas):
    data = {
        "temperature": temp,
        "humidity": hum,
        "pressure": pres,
        "gas": gas,
        "max_values": {
            "max_temperature": max_temp,
            "max_humidity": max_hum,
            "max_pressure": max_pres,
            "max_gas": max_gas,
        },
        "mean_values": {
            "mean_temperature": mean_temp,
            "mean_humidity": mean_hum,
            "mean_pressure": mean_pres,
            "mean_gas": mean_gas,
        }
    }
    return ujson.dumps(data)

def ap_mode(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    
    while ap.active() == False:
        pass
    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to: ' + ap.ifconfig()[0])
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        try:
            temp = round(bme.temperature, 2)
            hum = round(bme.humidity, 2)
            pres = round(bme.pressure, 2)
            gas = round(bme.gas / 1000, 2)

            temp_history = {'temperature': temp, 'humidity': hum, 'pressure': pres, 'gas': gas}
            history_stack.append(temp_history)

            # Limit the stack size to the last 30 entries
            if len(history_stack) > 30:
                history_stack.pop(0)  # Remove the oldest entry (FIFO)

            # Find and print the maximum values every second
            if len(history_stack) > 0:
                max_temp = max(entry['temperature'] for entry in history_stack)
                max_hum = max(entry['humidity'] for entry in history_stack)
                max_pres = max(entry['pressure'] for entry in history_stack)
                max_gas = max(entry['gas'] for entry in history_stack)

                mean_temp = sum(entry['temperature'] for entry in history_stack) / len(history_stack)
                mean_hum = sum(entry['humidity'] for entry in history_stack) / len(history_stack)
                mean_pres = sum(entry['pressure'] for entry in history_stack) / len(history_stack)
                mean_gas = sum(entry['gas'] for entry in history_stack) / len(history_stack)

                response = api_response(temp, hum, pres, gas, max_temp, max_hum, max_pres, max_gas, mean_temp, mean_hum, mean_pres, mean_gas)
            else:
                response = api_response(temp, hum, pres, gas, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A')

            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            print('Content = %s' % str(request))

            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: application/json\n')
            conn.send('Access-Control-Allow-Origin: *\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
        except OSError as e:
            print('Failed to read sensor.')
        sleep(1)  # Sleep for one second

# Start the web server in AP mode
ap_mode('sensor', 'password')
