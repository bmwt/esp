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

def duty_translate(n):
    # translate values from 0-255 to 0-1023
    return int((float(n) / 255) * 1023)
    
def setPixelColor(n, red, green, blue):
    red = machine.PWM(machine.Pin(13), freq=300, duty=duty_translate(red))
    green = machine.PWM(machine.Pin(14), freq=300, duty=duty_translate(green))
    blue = machine.PWM(machine.Pin(12), freq=300, duty=duty_translate(blue))
    
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

def color_cycle(sleep):
    setPixelColor(0, 0, 0, 0)
    time.sleep_ms(sleep)
    setPixelColor(0, 255, 255, 255)
    time.sleep_ms(sleep)
    setPixelColor(0, 255, 0, 0)
    time.sleep_ms(sleep)
    setPixelColor(0, 0, 255, 0)
    time.sleep_ms(sleep)
    setPixelColor(0, 0, 0, 255)
    time.sleep_ms(sleep)
    setPixelColor(0, 255, 255, 0)
    time.sleep_ms(sleep)
    setPixelColor(0, 0, 255, 255)
    time.sleep_ms(sleep)
    setPixelColor(0, 255, 0, 255)
    time.sleep_ms(sleep)
    setPixelColor(0, 192, 192, 192)
    time.sleep_ms(sleep)
    setPixelColor(0, 128, 128, 128)
    time.sleep_ms(sleep)
    setPixelColor(0, 128, 128, 0)
    time.sleep_ms(sleep)
    setPixelColor(0, 0, 128, 0)
    time.sleep_ms(sleep)
    setPixelColor(0, 128, 0, 128)
    time.sleep_ms(sleep)
    setPixelColor(0, 0, 128, 128)
    time.sleep_ms(sleep)
    setPixelColor(0, 0, 0, 128)
    time.sleep_ms(sleep)
    
initalize_pins()
while True:
    color_cycle(500)
 