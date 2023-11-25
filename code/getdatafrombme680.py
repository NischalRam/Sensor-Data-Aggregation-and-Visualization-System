from machine import Pin, I2C
from time import sleep
from bme680 import *

# ESP32 - Pin assignment
i2c = I2C(0,scl=Pin(1), sda=Pin(0))
# ESP8266 - Pin assignment
#i2c = I2C(scl=Pin(5), sda=Pin(4))

bme = BME680_I2C(i2c=i2c)

while True:
  try:
    temp = str(round(bme.temperature, 2)) + ' C'
    hum = str(round(bme.humidity, 2)) + ' %'
    pres = str(round(bme.pressure, 2)) + ' hPa'
    gas = str(round(bme.gas/1000, 2)) + ' KOhms'

    print('Temperature:', temp)
    print('Humidity:', hum)
    print('Pressure:', pres)
    print('Gas:', gas)
    print('-------')
  except OSError as e:
    print('Failed to read sensor.')
 
  sleep(5)