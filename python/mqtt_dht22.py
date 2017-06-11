import time
import machine
import dht
from umqtt.simple import MQTTClient

##### VARIABLES ####

#MQTT variables
server = "10.1.0.42"
topic = "home/test/temperature"
client = "test"

def get_temp():
    d = dht.DHT22(machine.Pin(5))
    while True:
        try:
            d.measure()
        except:
            continue
        else:
            results = [d.temperature(), d.humidity()]
            break
    return results
    
def pub_temp(temp):
    c = MQTTClient(client, server)
    c.connect()
    c.publish(topic, str(temp)) #publish data MQTT broker
    c.disconnect() #Disconnects from server

while True:
    results = get_temp()
    tempf = int(1.8*results[0]+32)
    print(results)
#    print("temp %s") % results[0]
    pub_temp(tempf) 
    time.sleep(5)
    