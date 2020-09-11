import pms5003
import machine
import uasyncio as asyncio

uart = machine.UART(1, tx=21, rx=22, baudrate=9600)
pm = pms5003.PMS5003(uart)
pm.registerCallback(pm.print)

loop=asyncio.get_event_loop()
loop.run_forever()
