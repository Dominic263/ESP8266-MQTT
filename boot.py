from umqtt.simple import MQTTClient
import machine
import ubinascii
import network

#Your wifi configurations go here
ssid = ''
password = ''

def connect():
    station = network.WLAN(network.STA_IF)
    if not station.isconnected():
        print("Connecting to network ...")
        station.active(True)
        station.connect(ssid, password)
        while not station.isconnected():
            pass
    if(station.isconnected() == True):
        print("Connected to "+ ssid)
        print('network config:', station.ifconfig())

connect()
