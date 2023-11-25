#In this program we are creating our network called nischal. 
#and any client can connect to the network using WiFi and 
#access the website using the IP. and the data updates automatically 

import network
import time
import socket
from machine import Pin, I2C
from time import sleep
from bme680 import *

led_pin = machine.Pin('LED', machine.Pin.OUT)
led_pin.value(1)
# ESP32 - Pin assignment
i2c = I2C(0, scl=Pin(1), sda=Pin(0))

bme = BME680_I2C(i2c=i2c)

# Sleep duration for BME sensor (5 seconds)
SENSOR_SLEEP_DURATION = 1

# Sleep duration for main loop (1 second)
MAIN_LOOP_SLEEP_DURATION = 1

def web_page():
    temp = str(round(bme.temperature, 2)) + ' C'
    hum = str(round(bme.humidity, 2)) + ' %'
    pres = str(round(bme.pressure, 2)) + ' hPa'
    gas = str(round(bme.gas / 1000, 2)) + ' KOhms'

    html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
            <script>function updateData() {
                var xhr = new XMLHttpRequest();
                xhr.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                        var data = JSON.parse(this.responseText);
                        document.getElementById('temperature').innerHTML = 'Temperature: ' + data.temperature;
                        document.getElementById('humidity').innerHTML = 'Humidity: ' + data.humidity;
                        document.getElementById('pressure').innerHTML = 'Pressure: ' + data.pressure;
                        document.getElementById('gas').innerHTML = 'Gas: ' + data.gas;
                    }
                };
                xhr.open('GET', '/data', true);
                xhr.send();
            }
            setInterval(updateData, 1000);</script></head>
            <body><h1>Weather Station</h1>
            <p id="temperature">Temperature: """ + temp + """</p>
            <p id="humidity">Humidity: """ + hum + """</p>
            <p id="pressure">Pressure: """ + pres + """</p>
            <p id="gas">Gas: """ + gas + """</p>
            </body></html>
         """
    return html


def ap_mode(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    while ap.active() == False:
        pass
    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to:: ' + ap.ifconfig()[0])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        # Sleep for BME sensor data acquisition
        sleep(SENSOR_SLEEP_DURATION)

        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        print('Content = %s' % str(request))
        if request.find(b'/data') != -1:
            response = '{"temperature":"' + str(round(bme.temperature, 2)) + ' C",' \
                       '"humidity":"' + str(round(bme.humidity, 2)) + ' %",' \
                       '"pressure":"' + str(round(bme.pressure, 2)) + ' hPa",' \
                       '"gas":"' + str(round(bme.gas / 1000, 2)) + ' KOhms"}'
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: application/json\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
        else:
            response = web_page()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
        conn.close()
        
        # Sleep for the main loop
        sleep(MAIN_LOOP_SLEEP_DURATION)


ap_mode('nischal', 'password')
