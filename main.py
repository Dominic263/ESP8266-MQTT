#In this program messages will be exchanged between the broker and mqtt to turn on , off or blink an led 
from machine import Pin
import time
import json

# Setup a GPIO Pin for output
led = Pin(0, Pin.OUT)

# Modify below section as required
CONFIG = {
    # Configuration details of the MQTT broker
    "MQTT_BROKER": "",
    "USER": "",
    "PASSWORD": "",
    "PORT": 1883,
    "TOPIC": b"ledstate",
    # unique identifier of the chip
    "CLIENT_ID": b"esp8266_" + ubinascii.hexlify(machine.unique_id())
}

#GLOBAL VARIABLES IN SCOPE
client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'], port=CONFIG['PORT'])
prevResult = ""
res1 = ""

def StateChanged():
    global res1
    global prevResult
    if(res1 != prevResult):
        return true
    return false
    
def GetString(msg):
    import json
    print(msg)
    jstring = msg.decode('utf-8')
    jstring = jstring.split('}')[0] + '}'
    jstring = jstring.replace("'" , "\"")
    print(jstring)
    jobj = json.loads(jstring)
    res1 = jobj['msg']
    return res1
    
    
def blink():
    for i in range(10):    
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)
        led.on()
        
def Logic(string):
    if string == "on":
        time.sleep(0.5)
        client.publish("notification", "I have been turned on")
        led.on()
    elif string == "off":
        client.publish("notification", "I have been turned off")
        time.sleep(0.5)
        led.off()
    elif string == "blink":
        client.publish("notification","I am blinking")
        blink()
       
# Method to act based on message received   
def onMessage(topic, msg):
    import time
    global prevResult
    global res1
    print("Topic: %s, Message: %s" % (topic, msg))
    res1 = GetString(msg)
    print(res1)
    while res1 != prevResult: 
        prevResult = res1
        Logic(res1)
        client.wait_msg()
         
def listen():
    client.set_callback(onMessage)
    client.connect()
    client.publish("test", "ESP8266 is Connected")
    client.subscribe(CONFIG['TOPIC'])
    print("ESP8266 is Connected to %s and subscribed to %s topic" % (CONFIG['MQTT_BROKER'], CONFIG['TOPIC']))

    try:
        while True:
            msg = client.wait_msg()
            print("The return message: ")
            print(msg)
            
    finally:
        client.disconnect()  

listen()
