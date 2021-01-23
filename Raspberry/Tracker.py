import serial
import time
import string
import pynmea2
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException

pnChannel = "raspi-tracker"; 
pnconfig = PNConfiguration() 
pnconfig.subscribe_key = "sub-c-e24667a8-5075-11eb-9d3f-7e8713e36938" 
pnconfig.publish_key = "pub-c-48dfeb3e-84f8-4bc1-8713-1733cc958705"
pnconfig.ssl = False   

pubnub = PubNub(pnconfig) 
pubnub.subscribe().channels(pnChannel).execute() 

while True:
    port="/dev/ttyAMA1" 
    ser=serial.Serial(port, baudrate=9600, timeout=0.5) 
    dataout = pynmea2.NMEAStreamReader()
    newdata=ser.readline() 

    if newdata[0:6] == "$GPRMC":
        newmsg=pynmea2.parse(newdata)
        lat=newmsg.latitude
        lng=newmsg.longitude
        try:
            envelope = pubnub.publish().channel(pnChannel).message({
            'lat':lat,
            'lng':lng
            }).sync()
            gps = "Latitud = " + str(lat) + "	Longitud = " + str(lng)
            print(gps)
        except PubNubException as e:
            handle_exception(e)
