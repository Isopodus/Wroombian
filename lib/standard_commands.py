from command.command import Command

class ram(Command):
    
    def __init__(self):
        super().__init__('Some description of ram command')
    
    def __call__(self, *args):
        print('yay, this works')