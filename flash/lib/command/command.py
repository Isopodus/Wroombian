from command.command_help import CommandHelp

class Command:
    
    name = 'No name provided'
    help = CommandHelp()
    
    def __init__(self, description:str=None, keys:dict=None, kernel=None):
        self.name = self.__class__.__name__
        self.help = CommandHelp(self.name, description, keys)
        self.kernel = kernel
        
    def __call__(self, *args):
        raise NotImplementedError