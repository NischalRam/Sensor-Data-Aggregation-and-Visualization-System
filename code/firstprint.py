## this code is working good and printing all the data we need

from machine import Pin, I2C
from time import sleep
from bme680 import *

# ESP32 - Pin assignment
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
# ESP8266 - Pin assignment
# i2c = I2C(scl=Pin(5), sda=Pin(4))

bme = BME680_I2C(i2c=i2c)

history_stack = []

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

        print('-------')
        print('Temperature:', temp)
        print('Humidity:', hum)
        print('Pressure:', pres)
        print('Gas:', gas)

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

            print('Max Temperature:', max_temp)
            print('Max Humidity:', max_hum)
            print('Max Pressure:', max_pres)
            print('Max Gas:', max_gas)
         
            print('Mean Temperature:', mean_temp)
            print('Mean Humidity:', mean_hum)
            print('Mean Pressure:', mean_pres)
            print('Mean Gas:', mean_gas)
            print('-------')

    except OSError as e:
        print('Failed to read sensor.')
    sleep(1)  # Sleep for one second
