-- Thingspeak connect script with deep sleep
-- Remember to connect GPIO16 and RST to enable deep sleep
-- TODO: Log error codes to server

--############
--# Settings #
--############

-- set global variables, re-set them in secrets.lua
wifi_SSID = "blah"
wifi_password = "blah"
thingspeak_channel_api_write_key = "blah"
require "secrets"

--- Thingspeak ---
thingspeak_temperature_field_name = "field1"
thingspeak_humidity_field_name = "field2"

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
time_between_sensor_readings = 60000

--################
--# END settings #
--################

-- init sensor
temperature = 0
-- GPIO0
pin = 3
ow.setup(pin)
counter=0
lasttemp=-999
print("wifissid " .. wifi_SSID )
-- Connect to the wifi network
wifi.setmode(wifi.STATION) 
wifi.setphymode(wifi_signal_mode)
wifi.sta.config(wifi_SSID, wifi_password) 
wifi.sta.connect()
if client_ip ~= "" then
    wifi.sta.setip({ip=client_ip,netmask=client_netmask,gateway=client_gateway})
end

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
function getTemp()
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
                   lasttemp =  t
         print("Last temp: " .. lasttemp)
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

        con = nil
        con = net.createConnection(net.TCP, 0)
 
        con:on("receive", function(con, payloadout)
            if (string.find(payloadout, "Status: 200 OK") ~= nil) then
                print("Posted OK to ThingSpeak");
            end
        end)
 
        con:on("connection", function(con, payloadout)
 
        -- Get sensor data
        getTemp() 
	t1 = lasttemp / 10000
	t2 = (lasttemp >= 0 and lasttemp % 10000) or (10000 - lasttemp % 10000)
	print("Temp:"..t1 .. "."..string.format("%04d", t2).." F\n")

        -- Post data to Thingspeak
        con:send(
            "POST /update?api_key=" .. thingspeak_channel_api_write_key .. 
            "&field1=" .. t1 .. 
--            "&field2=" .. humidity .. 
            " HTTP/1.1\r\n" .. 
            "Host: api.thingspeak.com\r\n" .. 
            "Connection: close\r\n" .. 
            "Accept: */*\r\n" .. 
            "User-Agent: Mozilla/4.0 (compatible; esp8266 Lua; Windows NT 5.1)\r\n" .. 
            "\r\n")
        end)
 
        con:on("disconnection", function(con, payloadout)
            con:close();
            collectgarbage();
            print("Going to deep sleep for "..(time_between_sensor_readings/1000).." seconds")
            node.dsleep(time_between_sensor_readings*1000) 
        end)

        -- Connect to Thingspeak
        con:connect(80,'api.thingspeak.com')
    else
        print("Connecting...")
    end
end
        
tmr.alarm(0, 100, 1, function() loop() end)

-- Watchdog loop, will force deep sleep the operation somehow takes to long
tmr.alarm(1,4000,1,function() node.dsleep(time_between_sensor_readings*1000) end)
