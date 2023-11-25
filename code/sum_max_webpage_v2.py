## present code v5


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

# Store past 60 seconds of data
data_history = []

def web_page():
    temp = str(round(bme.temperature, 2)) + ' C'
    hum = str(round(bme.humidity, 2)) + ' %'
    pres = str(round(bme.pressure, 2)) + ' hPa'
    gas = str(round(bme.gas / 1000, 2)) + ' KOhms'

    # Prepare the HTML for the past 60 seconds of data
    history_html = ""
    for entry in data_history:
        history_html += "<p>" + entry + "</p>"

    html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
            <script>function updateData() {
                var xhr = new XMLHttpRequest();
                xhr.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                        var data = JSON.parse(this.responseText);
                        document.getElementById('temperature').innerHTML =  data.temperature;
                        document.getElementById('humidity').innerHTML =  data.humidity;
                        document.getElementById('pressure').innerHTML =  data.pressure;
                        document.getElementById('gas').innerHTML =  data.gas;
                    }
                };
                xhr.open('GET', '/data', true);
                xhr.send();
            }
            setInterval(updateData, 1000);</script></head>
            <body>
            {
            "Temperature":<p id="temperature"> """ + temp + """ </p> ,
           "Humidity": <p id="humidity"> """ + hum + """  </p> ,
            "Pressure":<p id="pressure"> """ + pres + """ </p>,
            "Gas":<p id="gas"> """ + gas + """</p>
}
            <h2>Past 60 Seconds:</h2>
            """ + history_html + """
            </body></html>
         """
    return html


def ap_mode(ssid, password):
    global data_history
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

        # Update data history
        data_history.append('{"temperature":"' + str(round(bme.temperature, 2)) + ' C",' \
                            '"humidity":"' + str(round(bme.humidity, 2)) + ' %",' \
                            '"pressure":"' + str(round(bme.pressure, 2)) + ' hPa",' \
                            '"gas":"' + str(round(bme.gas / 1000, 2)) + ' KOhms"}')

        # Keep only the last 60 entries
        data_history = data_history[-60:]

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

