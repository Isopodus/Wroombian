from colors import *
from kernel import makeTab

class CommandHelp:
    
    name = 'No name provided'
    description = 'No description provided'
    keys = {} # pairs of {key: [args, key_description]} e.g. {'--cool': ['<path>', Add cool word into file]}
    
    def __init__(self, name:str=None, description:str=None, keys:dict=None):
        if name != None:
            self.name = name
        if description != None:
            self.description = description
        if keys != None:
            self.keys = keys
    
    def __str__(self):
        result = blue(self.name) + '\n'
        result += purple(self.description) + '\n'
        for key in self.keys:
            result += '    ' + yellow(key) + '  '
            tab = ''
            for arg in self.keys[key][0:-1]: 
                result += yellow(arg) + ' '
                tab += arg + ' '
            result += makeTab(tab) + self.keys[key][-1] + '\n'
            
        return result