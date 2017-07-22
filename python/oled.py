import ssd1306
import machine
i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
oled.text('HAIL', 0, 0)
oled.text('BRAK', 0, 10)
oled.show()
