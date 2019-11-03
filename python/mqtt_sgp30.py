import time
import machine
import adafruit_sgp30
from umqtt.simple import MQTTClient
from metadata import client, tvoc_topic, co2eq_topic, server


##### VARIABLES ####
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
i2c.init(scl=machine.Pin(22), sda=machine.Pin(21))
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

def pub_co2eq(co2eq):
    c = MQTTClient(client, server)
    while True:
        try:
            c.connect()
            c.publish(co2eq_topic, str(co2eq)) #publish data MQTT broker
            c.disconnect() #Disconnects from server
        except: 
            print("Cant connect to MQTT server, trying again")
            time.sleep(2)
            continue
        else:
            break

def pub_tvoc(tvoc):
    c = MQTTClient(client, server)
    while True:
        try:
            c.connect()
            c.publish(tvoc_topic, str(tvoc)) #publish data MQTT broker
            c.disconnect() #Disconnects from server
        except: 
            print("Cant connect to MQTT server, trying again")
            time.sleep(2)
            continue
        else:
            break
                    
while True:
    co2eq, tvoc = sgp30.iaq_measure()    
    pub_co2eq(co2eq)
    print("co2eq: ",co2eq)
    pub_tvoc(tvoc)
    print("tvoc: ",tvoc)
    time.sleep(30)
    