import machine
import uasyncio as asyncio
import pms5003
import time
from umqtt.simple import MQTTClient
from metadata import client, pm1_topic, pm10_topic, pm25_topic, server

loop = asyncio.get_event_loop()
pm = None

async def senddata(client, pm1_topic, pm25_topic, pm10_topic, server):
    while True:
        await asyncio.sleep(60)
        c = MQTTClient(client, server)
        while True:
            try:
                c.connect()
                c.publish(pm1_topic, str(pm._pm10_standard)) #publish data MQTT broker
                c.publish(pm25_topic, str(pm._pm25_standard)) #publish data MQTT broker
                c.publish(pm10_topic, str(pm._pm100_standard)) #publish data MQTT broker
                c.disconnect() #Disconnects from server
            except: 
                print("Cant connect to MQTT server, trying again")
                time.sleep(2)
                continue
            else:
                break
        print("Concentration Units (standard)")
        print("PM 1.0: %d\tPM2.5: %d\tPM10: %d" % (pm._pm10_standard, pm._pm25_standard, pm._pm100_standard))
        print("Concentration Units (environmental)")
        print("PM 1.0: %d\tPM2.5: %d\tPM10: %d" % (pm._pm10_env, pm._pm25_env, pm._pm100_env))

def start():
    uart = machine.UART(1, tx=21, rx=22, baudrate=9600)
    global pm
    pm = pms5003.PMS5003(uart, active_mode=True)
    asyncio.create_task(senddata(client, pm1_topic, pm25_topic, pm10_topic, server))
    asyncio.get_event_loop().run_forever()

start()
