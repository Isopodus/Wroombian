import time
import sys
sys.path[1] = '/flash/lib'

# Read settings from file
import json
file = open('/flash/settings.txt', 'r')
raw = ''
for line in file.readlines():
    raw += line
settings = json.loads(raw)
file.close()

# Init wifi
import network
from network import telnet, ftp

sta = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

# Connect to wifi
print('Connecting to network...')
network_settings = settings['network']
ap.active(False)
sta.active(True)
for key in network_settings['wifi']:
    connection_start = time.time()
    sta.connect(key, network_settings['wifi'][key])
    while not sta.isconnected() and time.time() - connection_start < network_settings['wifiConnectionTimeout']:
        pass
    
# Start AP
if not sta.isconnected():
    print("Connection failed, starting AP")
    sta.active(False)
    ap.active(True)
    ap.config(essid=network_settings['ap'][0], authmode=3, password=network_settings['ap'][1])
    print('AP config:', *ap.ifconfig())
else:
    print('Wifi connected, network config is:', *sta.ifconfig())

# Init telnet server
telnet.start(user=settings['user'][0], password=settings['user'][1], timeout=300)
#ftp.start(user="micro", password="python", buffsize=1024, timeout=300)