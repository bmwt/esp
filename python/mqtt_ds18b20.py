import time
import machine
import onewire
from umqtt.simple import MQTTClient
##### per client variables ####
from metadata import client, topic, server

def get_temp():
    ds = onewire.DS18B20(onewire.Onewire(machine.Pin(1)))
    roms = ds.scan()
    print('found devices:', roms)
    ds.convert_temp()
    time.sleep_ms(750)
    for rom in roms:
        print(ds.read_temp(rom), end=' ')
    print()
    return results
    
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
#    print("temp %s") % results[0]
    pub_temp(tempf) 
    time.sleep(5)
    