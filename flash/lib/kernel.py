import os
import gc
import machine
import sys
from colors import *
from command.command_string import CommandString
from command.command import Command
from command.commands_module import CommandsModule
from pye import pye
import json

from modules.standard_commands import StandardCommandsModule

class Kernel:
    def __init__(self):
        self.commands_modules =[]

        # Read settings from file
        file = open('/flash/etc/settings.txt', 'r')
        settings = json.loads(file.read())
        file.close()

        self.machine_name = settings['machineName']
        self.username = settings['user'][0]
        
        # Load standard commands
        self.loadCommandsModule(StandardCommandsModule())
        
        # Read command modules config and load all the enabled modules
        file = open('/flash/etc/modules.txt')
        modules = json.loads(file.read())
        file.close()
        
        for module_path in modules:
            if modules[module_path] != False:
                temp = __import__('modules.' + module_path, globals(), locals(), modules[module_path])
                for class_name in modules[module_path]:
                    self.loadCommandsModule(getattr(temp, class_name)())
        

    def loadCommandsModule(self, module:CommandsModule):
        self.commands_modules.append(module)

    def printHeader(self):
        try:
            path = os.getcwd()
            print(green(self.username + '@' + self.machine_name) + ':' + blue(path) + '$ ', end='')
        except OSError as e:
            os.chdir('/flash')

    def execute(self, raw_command:str):
        command_string = CommandString(raw_command)
        if command_string.command_name != None:

            # Check if such command exists
            for commands_module in self.commands_modules:
                for command in commands_module.commands:
                    if command.name == command_string.command_name:
                        if '-h' in command_string.keys or '--help' in command_string.keys:
                            print(command.help)
                            return True
                        else:
                            command(command_string.sudo, command_string.keys, command_string.command_name)
                            return True

            # Try to execute as bash script
            dirs = os.listdir(os.getcwd())
            if self.executeBashScript(command_string.command_name):
                return True
            print(red('No such command: {}'.format(command_string.command_name)))
            return False

    def executeBashScript(self, script:str):
        try:
            file = open(script)
            for line in file.readlines():
                if not self.execute(line[0:-1]):
                    print(red('-> ' + line))

            return True
        except OSError:
            return False

    def handleTerminal(self):
        self.printHeader()
        self.execute(input())

