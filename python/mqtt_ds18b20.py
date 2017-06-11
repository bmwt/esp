import time
import machine
import onewire
import ds18x20

from umqtt.simple import MQTTClient
##### per client variables ####
from metadata import client, topic, server

def get_temp():
    ow = onewire.OneWire(machine.Pin(0))
    ds = ds18x20.DS18X20(ow)
    roms = ds.scan()
    ds.convert_temp()
    time.sleep_ms(750)
    for rom in roms:
        return ds.read_temp(rom)
    
def pub_temp(temp):
    c = MQTTClient(client, server)
    while True:
        try:
            c.connect()
            c.publish(topic, str(temp)) #publish data MQTT broker
            c.disconnect() #Disconnects from server
        except: 
            print("Cant connect to MQTT server, trying again")
            time.sleep(2)
            continue
        else:
            break
                    
while True:
    results = get_temp()
    tempf = int(1.8*results+32)
    print(results)
    pub_temp(tempf) 
    time.sleep(30)
    
