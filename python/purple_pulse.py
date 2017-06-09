import machine
import time
import math
blue = machine.Pin(12)
red = machine.Pin(13)
green = machine.Pin(14)
pwm_red = machine.PWM(red, freq=500)
pwm_blue = machine.PWM(blue, freq=500)
pwm_green = machine.PWM(green, freq=500)

def purple_pulse(t):
    for i in range(20):
        pwm_red.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
        pwm_blue.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
        time.sleep_ms(t)

while True:
    purple_pulse(20)
    