import network
import time
from network import telnet, ftp
import json

class Wifi:
    def __init__(self):
        self.current_ssid = 'N/A'
        file = open('/flash/settings.txt', 'r')
        self.settings = json.loads(file.read())
        file.close()

        self.sta = network.WLAN(network.STA_IF)
        self.ap = network.WLAN(network.AP_IF)
        
        self.connect()
            
        telnet.start(user=self.settings['user'][0], password=self.settings['user'][1], timeout=5000)
        #ftp.start(user=self.settings['user'][0], password=self.settings['user'][1], buffsize=1024, timeout=300)
        
            
    # Connect to wifi
    def connect(self):
        file = open('/flash/settings.txt', 'r')
        self.settings = json.loads(file.read())
        file.close()
        
        print('Scanning networks...')
        self.network_settings = self.settings['network']
        self.ap.active(False)
        self.sta.active(True)
        self.scan()
        ssids = [net[0] for net in self.scanned]
        for key in self.network_settings['wifi']:
            if key in ssids:
                print('Connecting to', key + '...')
                connection_start = time.time()
                self.sta.connect(key, self.network_settings['wifi'][key])
                self.current_ssid = key
                while not self.sta.isconnected() and time.time() - connection_start < self.network_settings['wifiConnectionTimeout']:
                    pass
        if not self.sta.isconnected():
            self.current_ssid = 'N/A'
            self.startAP()
        else:
            print('Connected to {}, network config:'.format(self.current_ssid), *self.sta.ifconfig())

    # start AP
    def startAP(self):
        file = open('/flash/settings.txt', 'r')
        self.settings = json.loads(file.read())
        file.close()
        
        print("Starting AP")
        self.sta.active(False)
        self.current_ssid = 'N/A'
        self.ap.active(True)
        self.ap.config(essid=self.network_settings['ap'][0], authmode=3, password=self.network_settings['ap'][1])
        print('AP config:', *self.ap.ifconfig())
        
    def scan(self):
        nets = self.sta.scan()
        self.scanned = [(net[0].decode('utf-8'), net[3], net[5]) for net in nets]
