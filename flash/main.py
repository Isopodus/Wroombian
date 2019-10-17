import time
from kernel import *
import json
from standard_commands import StandardCommandsModule

# Start kernel
kernel = Kernel()

# Load commands
kernel.loadCommandsModule(StandardCommandsModule())
kernel.execute('wifi -init')

try:
    while True:
        kernel.handleTerminal()
except KeyboardInterrupt as e:
    print()
    kernel.execute('exit')

