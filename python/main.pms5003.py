import machine
import uasyncio as asyncio
import pms5003
import time

loop = asyncio.get_event_loop()
pm = None

async def senddata():
    while True:
        await asyncio.sleep(60)
        print("Concentration Units (standard)")
        print("PM 1.0: %d\tPM2.5: %d\tPM10: %d" % (pm._pm10_standard, pm._pm25_standard, pm._pm100_standard))
        print("Concentration Units (environmental)")
        print("PM 1.0: %d\tPM2.5: %d\tPM10: %d" % (pm._pm10_env, pm._pm25_env, pm._pm100_env))

def start():
    uart = machine.UART(1, tx=21, rx=22, baudrate=9600)
    global pm
    pm = pms5003.PMS5003(uart, active_mode=True)
    asyncio.create_task(senddata())
    asyncio.get_event_loop().run_forever()

start()
