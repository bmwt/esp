import machine
import time
blue = machine.Pin(12, machine.Pin.OUT)
red = machine.Pin(13, machine.Pin.OUT)
green = machine.Pin(14, machine.Pin.OUT)
while True:
    red.on()
    blue.on()
    time.sleep(2)
    red.off()
    blue.off()
    time.sleep(2)
    