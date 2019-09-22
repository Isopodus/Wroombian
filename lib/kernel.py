import os
import gc
import machine
import sys
from colors import *
from command.command_string import CommandString
from pye import pye
import json

import standard_commands as sc

class Kernel:
    def __init__(self, machine_name, username):
        self.commands =[
            sc.ram(),
            sc.rom(),
            sc.ls(),
            sc.cd(),
            sc.cat(),
            sc.nano(),
            sc.mkdir(),
            sc.rmdir(),
            sc.touch(),
            sc.rm(),
            sc.mv(),
            sc.help(),
            sc.run(),
            sc.exit(),
            sc.reboot(),
            sc.wifi()
        ]
        
        self.machine_name = machine_name
        self.username = username
        
    def printHeader(self):
        try:
            path = os.getcwd()
            print(green(self.username + '@' + self.machine_name) + ':' + blue(path) + '$ ', end='')
        except OSError as e:
            os.chdir('/flash')

    def execute(self, command_string:CommandString):
        if command_string.command_name != None:
            for command in self.commands:
                if command.name == command_string.command_name:
                    if '-h' in command_string.keys or '--help' in command_string.keys:
                        print(command.help)
                        return
                    else:
                        command(command_string.sudo, command_string.keys, command_string.command_name)
                        return
            print(red('No such command: {}'.format(command_string.command_name)))

    def handleTerminal(self):
        self.printHeader()
        self.execute(CommandString(input()))

