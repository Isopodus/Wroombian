from kernel import *
import sys
from colors import *

# Start the kernel
kernel = Kernel()

# Init wifi
kernel.execute('wifi -init')

# Run main loop
while True:
    try:
        kernel.handleTerminal()
    except KeyboardInterrupt as e:
        print()
        kernel.execute('exit')
    except Exception as e:
        keepRed()
        print('Unhandled exception while running Wroombian:')
        sys.print_exception(e)
        resetColor()
