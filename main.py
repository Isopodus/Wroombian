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

kernel = Kernel()
try:
    while True:
        kernel.handleTerminal()
except KeyboardInterrupt as e:
    print()
    sys.exit()