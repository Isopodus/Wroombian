import upip as pip
import os
from machine import Pin
import time

startup = time.time()

print('Hello world!')

led = Pin(2, Pin.OUT)
while True:
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.5)
    print('Working for', time.time() - startup, 'seconds')