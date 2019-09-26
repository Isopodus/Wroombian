import os
import gc
import machine
import sys
from colors import *
from command.command_string import CommandString
from command.command import Command
from pye import pye
import json

class Kernel:
    def __init__(self):
        self.commands =[]
        
        # Read settings from file
        file = open('/flash/etc/settings.txt', 'r')
        settings = json.loads(file.read())
        file.close()
        
        self.machine_name = settings['machineName']
        self.username = settings['user'][0]
        
    def loadCommandModule(self, *args):
        if len(args) > 1:
            if type(args[0]) is list:
                are_commands = True
                for i in args[0]:
                    if not issubclass(i, Command):
                        are_commands = False
                        break
                if are_commands:
                    self.commands.extend(args[0])
            elif issubclass(args[0], Command):
                self.commands.append(args[0])
                
                
    
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
            for command in self.commands:
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

