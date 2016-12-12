-- Thingspeak connect script with deep sleep
-- Remember to connect GPIO16 (D0) and RST to enable deep sleep
-- TODO: Log error codes to server

--############
--# Settings #
--############

-- set global variables, re-set them in secrets.lua
wifi_SSID = "blah"
wifi_password = "blah"
mqtt_name = "blah"
require "secrets"

--- MQTT ---
mqtt_broker_ip = "10.1.0.40"
mqtt_broker_port = 1883
mqtt_username = ""
mqtt_password = ""
mqtt_client_id = ""


--- WIFI ---
-- wifi.PHYMODE_B 802.11b, More range, Low Transfer rate, More current draw
-- wifi.PHYMODE_G 802.11g, Medium range, Medium transfer rate, Medium current draw
-- wifi.PHYMODE_N 802.11n, Least range, Fast transfer rate, Least current draw 
wifi_signal_mode = wifi.PHYMODE_N
-- If the settings below are filled out then the module connects 
-- using a static ip address which is faster than DHCP and 
-- better for battery life. Blank "" will use DHCP.
-- My own tests show around 1-2 seconds with static ip
-- and 4+ seconds for DHCP
client_ip=""
client_netmask=""
client_gateway=""

--- INTERVAL ---
-- In milliseconds. Remember that the sensor reading, 
-- reboot and wifi reconnect takes a few seconds
time_between_sensor_readings = 120000

--################
--# END settings #
--################

-- Setup MQTT clients and events

m = mqtt.Client(client_id, 120, username, password)
temperature = 0
humidity = 0

-- Connect to the wifi network
wifi.setmode(wifi.STATION) 
wifi.setphymode(wifi_signal_mode)
wifi.sta.config(wifi_SSID, wifi_password) 
wifi.sta.connect()
if client_ip ~= "" then
    wifi.sta.setip({ip=client_ip,netmask=client_netmask,gateway=client_gateway})
end

-- init sensor
pin = 3
ow.setup(pin)
counter=0
lasttemp=-999

-- support function

function bxor(a,b)
   local r = 0
   for i = 0, 31 do
      if ( a % 2 + b % 2 == 1 ) then
         r = r + 2^i
      end
      a = a / 2
      b = b / 2
   end
   return r
end

-- DS18B20 sensor logic
function get_sensor_Data()
      addr = ow.reset_search(pin)
      repeat
        tmr.wdclr()
      
      if (addr ~= nil) then
        crc = ow.crc8(string.sub(addr,1,7))
        if (crc == addr:byte(8)) then
          if ((addr:byte(1) == 0x10) or (addr:byte(1) == 0x28)) then
                ow.reset(pin)
                ow.select(pin, addr)
                ow.write(pin, 0x44, 1)
                tmr.delay(1000000)
                present = ow.reset(pin)
                ow.select(pin, addr)
                ow.write(pin,0xBE, 1)
                data = nil
                data = string.char(ow.read(pin))
                for i = 1, 8 do
                  data = data .. string.char(ow.read(pin))
                end
                crc = ow.crc8(string.sub(data,1,8))
                if (crc == data:byte(9)) then
                   t = (data:byte(1) + data:byte(2) * 256)
         if (t > 32768) then
                    t = (bxor(t, 0xffff)) + 1
                    t = (-1) * t
                   end
         t = t * 625
         t = t * 18 + 3200000
         t = t / 10
                   temperature =  t
         print("Sensor reading: " .. temperature)
                end                   
                tmr.wdclr()
          end
        end
      end
      addr = ow.search(pin)
      until(addr == nil)
end

function loop() 
    if wifi.sta.status() == 5 then
        -- Stop the loop
        tmr.stop(0)

        m:connect( mqtt_broker_ip , mqtt_broker_port, 0, function(conn)
            print("Connected to MQTT")
            print("  IP: ".. mqtt_broker_ip)
            print("  Port: ".. mqtt_broker_port)
            print("  Client ID: ".. mqtt_client_id)
            print("  Username: ".. mqtt_username)
            -- Get sensor data
            get_sensor_Data() 
            m:publish("ESP8266/"..mqtt_name.."/temperature",(temperature / 10000).."."..(temperature % 10000), 0, 0, function(conn)
--                m:publish("ESP8266/humidity",(humidity / 10).."."..(humidity % 10), 0, 0, function(conn)
                    print("Going to deep sleep for "..(time_between_sensor_readings/1000).." seconds")
                    node.dsleep(time_between_sensor_readings*1000)             
                end)          
--            end)
        end )
    else
        print("Connecting...")
    end
end
            

        
tmr.alarm(0, 100, 1, function() loop() end)
