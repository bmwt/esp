import time
import machine
import onewire
import ds18x20

from umqtt.simple import MQTTClient
##### per client variables ####
from metadata import client, topic, server

def get_temp():
    # declare the onewire bus
    ow = onewire.OneWire(machine.Pin(0))
    # declare the ds18b20 instanfe
    ds = ds18x20.DS18X20(ow)
    # find the sensor and get an address
    roms = ds.scan()
    # trigger a reading.  need to wait 750 ms before getting result
    ds.convert_temp()
    time.sleep_ms(750)
    # grab the value from the address
    for rom in roms:
        return ds.read_temp(rom)
    
def pub_temp(temp):
    # make an mqtt client instance
    c = MQTTClient(client, server)
    # keep trying to connect until we do
    while True:
        try:
            # connect to the mqtt server
            c.connect()
            # publish our message
            c.publish(topic, str(temp))
            # disconnect
            c.disconnect()
        except: 
            # if we get an exception, error and try again
            print("Cant connect to MQTT server, trying again")
            time.sleep(2)
            continue
        else:
            # if it worked we can leave our infinite loop
            break
                    
# main loop
while True:
    # get the temp
    results = get_temp()
    # convert c -> f, and make it an int
    tempf = int(1.8*results+32)
    # print value to console
    print(results)
    # publish mqtt message
    pub_temp(tempf) 
    # sleep
    time.sleep(30)
