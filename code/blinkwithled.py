# This is just a sample programming that will turn on and off the led light

import machine
import utime

led_pin = machine.Pin('LED', machine.Pin.OUT)


while True:
        print("Enter")
        led_pin.value(1)
        utime.sleep(3)
        led_pin.value(0)
        utime.sleep(3)
        print("End")
