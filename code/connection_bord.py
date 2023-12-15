import urequests
import machine
import network
import usocket as socket
from machine import Pin

led_pin = machine.Pin('LED', machine.Pin.OUT)

# Set the IP address of the first Pico (replace with the actual IP address)
url = "http://192.168.98.211/"

# Function to make a request to the sensor API
def get_sensor_data(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]

    s = socket.socket()
    s.connect(addr)

    s.send(bytes(f"GET /{path} HTTP/1.0\r\nHost: {host}\r\n\r\n", 'utf-8'))

    response = b""
    while True:
        data = s.recv(1024)
        if data:
            response += data
        else:
            break

    s.close()

    return response

def connect_to_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    while not station.isconnected():
        pass

    print('Connection successful')
    led_pin.value(1)
    print(station.ifconfig())

# Function to start the API server on the second Pico
def start_api_server():
    led_pin = machine.Pin('LED', machine.Pin.OUT)
    led_pin.value(1)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 8080))  # Use a different port, for example, 8080
    s.listen(5)

    print('API server started')

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))

        try:
            sensor_data = get_sensor_data(url)

            sensor_data_arr = sensor_data.split(b'close\n\n')
            sensor_data = sensor_data_arr[1]

            if sensor_data:
                conn.send(b'HTTP/1.1 200 OK\n')
                conn.send(b'Content-Type: application/json\n')
                conn.send(b'Access-Control-Allow-Origin: *\n')
                conn.send(b'Connection: close\n\n')
                conn.sendall(sensor_data)
            else:
                response = b'{"error": "Unable to retrieve sensor data"}'
                conn.send(b'HTTP/1.1 200 OK\n')
                conn.send(b'Content-Type: application/json\n')
                conn.send(b'Access-Control-Allow-Origin: *\n')
                conn.send(b'Connection: close\n\n')
                conn.sendall(response)

        except Exception as e:
            print('Error processing request:', e)

        finally:
            try:
                conn.close()
            except Exception as e:
                print('Error closing connection:', e)

# Connect to the existing Wi-Fi network and start the API server
connect_to_wifi('sensor1', '123456789')
start_api_server()
