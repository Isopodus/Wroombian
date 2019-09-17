import os
import gc
import machine
import sys
from colors import *
from command import Command
from pye import pye

# get rom available - statvfs('') -> (a, b, c, d), a*c=total, a*d=left, total-left=used
# get file size - stat('file.txt') -> [6]

class Kernel:
    def __init__(self, machine_name, username):
        self.machine_name = machine_name
        self.username = username

    def defaultCommand(self, *args):
        if args[2] != "-1":
            print(red('No such command: {}'.format(args[2])))

    def printHeader(self):
        try:
            path = os.getcwd()
            print(green(self.username + '@' + self.machine_name) + ':' + blue(path) + '$ ', end='')
        except OSError as e:
            os.chdir('/flash')

    def execute(self, command:Command):
        commands = {
            "ram": self.ram,
            "rom": self.rom,
            "ls": self.ls,
            "cd": self.cd,
            "cat": self.cat,
            "nano": self.nano,
            "mkdir": self.mkdir,
            "rmdir": self.rmdir,
            "touch": self.touch,
            "rm": self.rm,
            "mv": self.mv,
            "help": self.help,
            "exec": self.exec,
            "exit": self.exit,
            "reboot": self.reboot
        }
        func = commands.get(command.command, self.defaultCommand)
        func(command.sudo, command.options, command.command)
        # TODO add --help keys for commands

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

    def cd(self, *args):
        if len(args[1]) > 0:
            path = args[1][0]
            try:
                os.chdir(path)

            except OSError as e:
                print(red('No such directory'))
        else:
            print(red('No directory provided'))

    def cat(self, *args):
        if len(args[1]) > 0:
            path = args[1][0]
            try:
                file = open(path, 'r')
                print()
                print(*file.readlines())
                file.close()
            except OSError as e:
                print(red('No such file'))
        else:
            print('No file name provided')

    def nano(self, *args):
        if len(args[1]) > 0:
            path = args[1][0]
            try:
                pye(path)
            except OSError as e:
                print(red('No such file'))
        else:
            print('No file name provided')
            
    def mkdir(self, *args):
        if len(args[1]) > 0:
            path = args[1][0]
            try:
                os.mkdir(path)
            except OSError as e:
                if 'EEXIST' in str(e):
                    print(red('Directory already exists'))
                else:
                    print(red('Not allowed'))
        else:
            print('No directory name provided')

    def rmdir(self, *args):
        if len(args[1]) > 0:
            path = args[1][0]
            try:
                os.rmdir(path)
            except OSError as e:
                if 'EPERM' in str(e):
                    print(red('Not allowed'))
                    
                else:
                    print(red('No such directory'))
        else:
            print('No directory name provided')
            
    def touch(self, *args):
        if len(args[1]) > 0:
            path = args[1][0]
            try:
                file = open(path, 'w')
                file.close()
            except OSError as e:
                print(red('Not allowed'))
        else:
            print('No file name provided')
            
    def rm(self, *args):
        if len(args[1]) > 0:
            path = args[1][0]
            try:
                os.remove(path)
            except OSError as e:
                if 'ENOENT' in str(e):
                    print(red('No such file'))
                    
                else:
                    print(red('Not allowed'))
        else:
            print('No file name provided')
            
    def mv(self, *args):
        if len(args[1]) > 1:
            path = args[1][0]
            newpath = args[1][1]
            try:
                os.rename(path, newpath)
            except OSError as e:
                if 'ENOENT' in str(e):
                    print(red('No such file'))
                    
                else:
                    print(red('Not allowed'))
        else:
            print('No file name provided')
            
    def exec(self, *args):
        if len(args[1]) > 0:
            path = args[1][0]
            try:
                if not 'main.py' in path:
                    execfile(path)
                else:
                   print(red('Do NOT try to run multiple instances of OS. This may cause to stack overflow and CPU halt!'))
            except Exception as e:
                if type(e) is OSError:
                    print(red('No such file'))
                else:
                    keepRed()
                    print('Unhandled exception in file {}:'.format(path))
                    sys.print_exception(e)
                    resetColor()
        else:
            print('No file name provided')
            
    def exit(self, *args):
        print(yellow('Shutting down Wroombian...'))
        gc.collect()
        sys.exit()
    
    def reboot(self, *args):
        print(yellow('Rebooting...'))
        machine.reset()
    
    def help(self, *args):
        print(green('Available standard commands:'))
        print('''
help - show this message
ram - get RAM load
rom - get ROM load
ls - list files and directories
cd <path> - go to directory
cat <path> - print file content
nano <path> - edit file
mkdir <path> - make directory
rmdir <path> - remove directory
touch <path> - create file
rm <path> - delete file
mv <path1> <path2> - move or rename file
exec <path> - run python script
exit - shutdown Wroombian
reboot - restart the device''')
        print(blue('Type command with --help (-h) key to show help for this command'))
            