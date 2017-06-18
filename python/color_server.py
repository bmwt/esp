import socket
import machine
import time

# initialize pins for each color
redPWM = machine.PWM(machine.Pin(13, machine.Pin.OUT), freq=1000)
greenPWM = machine.PWM(machine.Pin(14, machine.Pin.OUT), freq=1000)
bluePWM = machine.PWM(machine.Pin(12, machine.Pin.OUT), freq=1000)

#HTML to send to browsers
html = """<!DOCTYPE html>
<html>
<head> <title>bmwt color server</title> </head>

<center><h2>A simple webserver for changing a light's color with Micropython</h2></center>
<center><h3>(All Hail Brak)</h3></center>

<a href="/red">Red</a><p>
<a href="/green">Green</a><p>
<a href="/blue">Blue</a><p>
<a href="/orange">Orange</a><p>
<a href="/yellow">Yellow</a><p>
<a href="/purple">Purple</a><p>
<a href="/magenta">Magenta</a><p>
<a href="/cycle">Cycle</a><p>

</html>
"""

hailbrak = """<!DOCTYPE html>
<html>
<head> <title>bmwt color server</title> </head>

<center><h2>ALL HAIL BRAK</h2></center>

</html>
"""


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

#Setup Socket WebServer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
while True:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    print("Content = %s" % str(request))
    request = str(request)
    print(request)
    response = html
    request = str(request).split()[1]
    print("Request:")
    print(request)
    if request == "/brak":
        conn.send(hailbrak)
        conn.close()
        continue
    elif request == "/red":
        color_set("red")
    elif request == "/green":
        color_set("green")
    elif request == "/blue":
        color_set("blue")
    elif request == "/orange":
        color_set("orange")
    elif request == "/yellow":
        color_set("yellow")
    elif request == "/purple":
        color_set("purple")
    elif request == "/magenta":
        color_set("magenta")
    elif request == "/cycle":
        color_cycle(500)
    conn.send(response)
    conn.close()

