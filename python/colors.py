import machine
import time

# initialize pins for each color
redPWM = machine.PWM(machine.Pin(13, machine.Pin.OUT), freq=1000)
greenPWM = machine.PWM(machine.Pin(14, machine.Pin.OUT), freq=1000)
bluePWM = machine.PWM(machine.Pin(12, machine.Pin.OUT), freq=1000)

# function to turn 0-255 color into 0-1023 PWM value 
def duty_translate(n):
    return int((float(n) / 255) * 1023)
    
# set pixel color according to RGB value.  n for multiple bulbs
def setPixelColor(n, redvalue, greenvalue, bluevalue):
    redPWM.duty(duty_translate(redvalue))
    greenPWM.duty(duty_translate(greenvalue))
    bluePWM.duty(duty_translate(bluevalue))
    
    
# set bulb to a color
def color_set(color):
    if color == 'black':
        setPixelColor(0, 0, 0, 0)
    elif color == 'white':
        setPixelColor(0, 255, 255, 255)
    elif color == 'red':
        setPixelColor(0, 255, 0, 0)
    elif color == 'lime':
        setPixelColor(0, 0, 255, 0)
    elif color == 'blue':
        setPixelColor(0, 0, 0, 255)
    elif color == 'yellow':
        setPixelColor(0, 255, 255, 0)
    elif color == 'aqua':
        setPixelColor(0, 0, 255, 255)
    elif color == 'magenta':
        setPixelColor(0, 255, 0, 255)
    elif color == 'silver':
        setPixelColor(0, 192, 192, 192)
    elif color == 'grey':
        setPixelColor(0, 128, 128, 128)
    elif color == 'olive':
        setPixelColor(0, 128, 128, 0)
    elif color == 'green':
        setPixelColor(0, 0, 128, 0)
    elif color == 'purple':   
        setPixelColor(0, 128, 0, 255)
    elif color == 'teal':
        setPixelColor(0, 0, 128, 128)
    elif color == 'navy':
        setPixelColor(0, 0, 0, 128)
    elif color == 'orange':
        setPixelColor(0, 255, 128, 0)

# cycle through a list of colors
def color_cycle(sleep):
    cycle_colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    for color in cycle_colors:
        color_set(color)
        time.sleep_ms(sleep)

while True:
    color_cycle(500)
