#print('Hello world!')
#from kernel import Kernel
#method_list = [func for func in dir(Kernel) if callable(getattr(Kernel, func)) and not func.startswith('__')]
#print(method_list)
import time
from machine import Pin
led = Pin(2, 2)

while True:
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.5)
