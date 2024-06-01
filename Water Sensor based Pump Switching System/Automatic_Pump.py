# Import

from machine import Pin
import time

#Setting for Pins
relay_pin=1
sensor_pin=2
relay=Pin(relay_pin, Pin.OUT)
sensor=Pin(sensor_pin, Pin.IN)

while True:
    value=sensor.value()
    if value==1: 
        relay.off()
        print("Water Pump: OFF")
    elif value==0:
        print("Water Pump: ON")
        relay.on()
    else:
        print("Check For Error")
        time.sleep(1000)