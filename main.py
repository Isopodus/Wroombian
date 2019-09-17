import time
from kernel import *
import json

# Read settings from file
file = open('/flash/settings.txt', 'r')
raw = ''
for line in file.readlines():
    raw += line
settings = json.loads(raw)
file.close()

machine_name = settings['machineName']
username = settings['user'][0]

# Start kernel
kernel = Kernel(machine_name, username)
try:
    while True:
        kernel.handleTerminal()
except KeyboardInterrupt as e:
    print()
    kernel.exit()

