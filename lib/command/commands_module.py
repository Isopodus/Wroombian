from command.command import Command

class CommandsModule:
    commands = []
    
    def __init__(self):
        for c in dir(self):
            attr = getattr(self, c, None)
            if isinstance(attr, type) and issubclass(attr, Command):
                self.commands.append(attr())