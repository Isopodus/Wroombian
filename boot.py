# This file is executed on every boot (including wake-boot from deepsleep)
import sys
sys.path[1] = '/flash/lib'

import network
from network import telnet, ftp

sta_if = network.WLAN(network.STA_IF)

if not sta_if.isconnected():
    print('Connecting to network...')
    sta_if.active(True)
    sta_if.connect('mandarinka', 'mandarinka2017')
    while not sta_if.isconnected():
            pass
        
print('Network config:', *sta_if.ifconfig())

if sta_if.isconnected():
    try:
        mdns = network.mDNS()
        mdns.start("mPy","MicroPython with mDNS")
        _ = mdns.addService('_ftp', '_tcp', 21, "MicroPython", {"board": "ESP32", "service": "mPy FTP File transfer", "passive": "True"})
        _ = mdns.addService('_telnet', '_tcp', 23, "MicroPython", {"board": "ESP32", "service": "mPy Telnet REPL"})
        _ = mdns.addService('_http', '_tcp', 80, "MicroPython", {"board": "ESP32", "service": "mPy Web server"})
    except:
        print("mDNS not started")
        
telnet.start(user="micro", password="python", timeout=300)
ftp.start(user="micro", password="python", buffsize=1024, timeout=300)