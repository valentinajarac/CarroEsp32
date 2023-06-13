from dcmotor import DCMotor       
from machine import Pin, PWM   
from time import sleep
import umail
import network
from hcsr04 import HCSR04
from time import sleep

sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)

try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'MOVISTAR WIFI1910'     # WIFI login
password = 'vhkt0974' # WIFI password 

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

#led = Pin(2, Pin.OUT)

frequency = 15000       
pin1 = Pin(5, Pin.OUT)    
pin2 = Pin(4, Pin.OUT)  
pin3 = Pin(23, Pin.OUT)    
pin4 = Pin(22, Pin.OUT) 
enable = PWM(Pin(18), frequency)  
enable1 = PWM(Pin(21), frequency)
dc_motor = DCMotor(pin1, pin2, enable)      
dc_motor = DCMotor(pin1, pin2, enable, 350, 1023)
dc_motor1 = DCMotor(pin3, pin4, enable1)      
dc_motor1 = DCMotor(pin3, pin4, enable1, 350, 1023)

          



