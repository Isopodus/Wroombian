import time
from kernel import *
import json

from standard_commands import *

# Read settings from file
file = open('/flash/settings.txt', 'r')
settings = json.loads(file.read())
file.close()

machine_name = settings['machineName']
username = settings['user'][0]

ram_c = ram()
ram_c()
print(ram_c.help)

# Start kernel
kernel = Kernel(machine_name, username)
try:
    while True:
        kernel.handleTerminal()
except KeyboardInterrupt as e:
    print()
    kernel.exit()

