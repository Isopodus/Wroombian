import os
import gc
from colors import *
from command import Command

# get rom available - statvfs('') -> (a, b, c, d), a*c=total, a*d=left, total-left=used
# get file size - stat('file.txt') -> [6]

class Kernel:
    def __init__(self):
        pass
    
    def defaultCommand(self, *args):
        if args[2] != "-1":
            print(red('No such command: {}'.format(args[2])))
    
    def printHeader(self):
        path = os.getcwd()
        print(green('username' + '@' + 'machine_name') + ':' + blue(path) + '$ ', end='')
    
    def execute(self, command:Command):
        commands = {
            "ram": self.ram,
            "rom": self.rom,
            "ls": self.ls,
            #"cd": self.cd,
            #"cat": self.cat,
            #"nano": self.nano,
            #"mkdir": self.mkdir,
            #"rmdir": self.rmdir,
            #"touch": self.touch,
            #"rm": self.rm,
            #"mv": self.mv,
            #"help": self.help,
            #"run": self.run,
            #"reboot": self.reboot
        }
        func = commands.get(command.command, self.defaultCommand)
        func(command.sudo, command.options, command.command)
    
    def handleTerminal(self):
        self.printHeader()
        self.execute(Command(input()))
        
    def rom(self, *args):
        fs_data = os.statvfs('')
        mem_total = fs_data[0] * fs_data[2]
        mem_free = fs_data[0] * fs_data[3]
        mem_alloc = mem_total - mem_free
        print(yellow(" --- ROM usage --- "))
        print(" Free: {}".format(str(mem_free) + ' B' if mem_free < 1024 else str(round(mem_free/1024, 2)) + ' KB'))
        print(" Used: {}".format(str(mem_alloc) + ' B' if mem_alloc < 1024 else str(round(mem_alloc/1024, 2)) + ' KB'))
        print(" Total: {}".format(str(mem_total) + ' B' if mem_total < 1024 else str(round(mem_total/1024, 2)) + ' KB'))
    
    def ram(self, *args):
        gc.collect()
        mem_free = gc.mem_free()
        mem_alloc = gc.mem_alloc()
        mem_total = mem_free + mem_alloc
        print(yellow(" --- RAM usage --- "))
        print(" Free: {}".format(str(mem_free) + ' B' if mem_free < 1024 else str(round(mem_free/1024, 2)) + ' KB'))
        print(" Used: {}".format(str(mem_alloc) + ' B' if mem_alloc < 1024 else str(round(mem_alloc/1024, 2)) + ' KB'))
        print(" Total: {}".format(str(mem_total) + ' B' if mem_total < 1024 else str(round(mem_total/1024, 2)) + ' KB'))
    
    def ls(self, *args):
        c_path = os.getcwd()
        try:
            if len(args[1]) > 0:
                path = args[1][0]
            else:
                path = c_path
                
            dirs = os.listdir(path)
            os.chdir(path)
            print(yellow('Name\t\t---\t\tSize\t\t---\t\tType'))
            for dir in dirs:
                stat = os.stat(dir)
                print(dir, '\t\t\t\t',
                      str(stat[6])+' B' if stat[6] < 1024 else str(round(stat[6]/1024, 2))+' KB', '\t\t\t\t',
                      green('FILE') if stat[0] == 33279 else blue('DIR'), sep='')
        except OSError as e:
            print(red('No such directory'))
        os.chdir(c_path)
            
        
    