from kernel import *

# Start the kernel
kernel = Kernel()

# Init wifi
kernel.execute('wifi -init')

# Run main loop
try:
    while True:
        kernel.handleTerminal()
except KeyboardInterrupt as e:
    print()
    kernel.execute('exit')

