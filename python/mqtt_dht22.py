import time
import machine
import dht
from umqtt.simple import MQTTClient
from metadata import client, topic, server


##### VARIABLES ####

def get_temp():
    d = dht.DHT22(machine.Pin(5))
    while True:
        try:
            d.measure()
        except:
            print("Can't initialize DHT22, trying again")
            continue
        else:
            results = [d.temperature(), d.humidity()]
            break
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
    tempf = int(1.8*results[0]+32)
    print(results)
#    print("temp %s") % results[0]
    pub_temp(tempf) 
    time.sleep(5)
    