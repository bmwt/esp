import machine
import time

PINS = [13,14,12] # R, G, B
R = 13
G = 14
B = 12
red = machine.PWM(machine.Pin(13), freq=300)
green = machine.PWM(machine.Pin(14), freq=300)
blue = machine.PWM(machine.Pin(12), freq=300)

# initialize pins to white and set freq to 0 (off)
def initalize_pins():
    for i in PINS:
        pin = machine.Pin(i, machine.Pin.OUT)

def color_set(color):
    if color == "white":
        red = machine.PWM(machine.Pin(13), duty=100)
        green = machine.PWM(machine.Pin(14), duty=100)
        blue = machine.PWM(machine.Pin(12), duty=100)

    if color == "red":
        red = machine.PWM(machine.Pin(13), freq=300, duty=100)
        green = machine.PWM(machine.Pin(14), freq=300, duty=0)
        blue = machine.PWM(machine.Pin(12), freq=300, duty=0)

    if color == "green":
        red = machine.PWM(machine.Pin(13), freq=300, duty=0)
        green = machine.PWM(machine.Pin(14), freq=300, duty=100)
        blue = machine.PWM(machine.Pin(12), freq=300, duty=100)
    if color == "blue":
        red = machine.PWM(machine.Pin(13), freq=300, duty=0)
        green = machine.PWM(machine.Pin(14), freq=300, duty=0)
        blue = machine.PWM(machine.Pin(12), freq=300, duty=100)

    if color == "purple":
        red = machine.PWM(machine.Pin(13), freq=300, duty=100)
        green = machine.PWM(machine.Pin(14), freq=300, duty=0)
        blue = machine.PWM(machine.Pin(12), freq=300, duty=100)
                            
def color_pulse(speed, step):
        for dutyCycle in range(1, 101, step):
            if red.duty is not 0:
                red.duty(dutyCycle)
            if green.duty:
                green.duty(dutyCycle)
            if blue.duty is not 0:
                blue.duty(dutyCycle)
            time.sleep(speed)
        for dutyCycle in range(100, 0, -step):
            if red.duty is not 0:
                red.duty(dutyCycle)
            if green.duty:
                green.duty(dutyCycle)
            if blue.duty is not 0:
                blue.duty(dutyCycle)
            time.sleep(speed)

initalize_pins()
color_set("purple")
while True:
    color_pulse(0.02, 5)

#while True:
#    color_pulse("purple", 300, 0.02, 5) 
    
