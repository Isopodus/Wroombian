from command.command import Command
from command.commands_module import CommandsModule
from colors import *

def makeTab(line:str, size=25):
    return ' ' * (size - len(line))

class PipCommandModule(CommandsModule):
    def __init__(self):
        
        # Add all commands
        self.commands.append(pip())
        
class pip(Command):
    
    def __init__(self):
        super().__init__('Install micropython packages',
                         {'install': ['<package_name>', '<path>',
                                      'Try to download and install new package, path is optional (packages will be installed to /lib by default)']})
    
    def __call__(self, *args):
        if len(args[1]) > 0:
            if 'install' in args[1] and len(args[1]) > 1:
                path = None
                if (len(args[1]) == 3):
                    path = args[1][2]
                upip = __import__('upip')
                upip.install(args[1][1], path)
            else:
                print(red('No valid parameters provided'))
                print(self.help)
        else:
            print(red('No parameters provided'))
            print(self.help)
