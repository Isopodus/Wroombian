import os
import gc
import machine
import sys
from colors import *
from command import Command
from pye import pye
from wifi import Wifi
import json

def makeTab(line:str, size=25):
    return ' ' * (size - len(line))

class Kernel:
    def __init__(self, machine_name, username):
        self.commands = {
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
            "run": self.run,
            "exit": self.exit,
            "reboot": self.reboot,
            "wifi": self.wifi_setup
        }
        
        self.machine_name = machine_name
        self.username = username
        
        self.wifi_handler = Wifi()

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
        func = self.commands.get(command.command, self.defaultCommand)
        func(command.sudo, command.options, command.command)
        # TODO add --help keys for self.commands

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
            print(yellow('Name         ---         Size         ---         Type'))
            for dir in dirs:
                stat = os.stat(dir)
                sizeB = str(stat[6])+' B'
                sizeKB = str(round(stat[6]/1024, 2))+' KB'
                print(dir, makeTab(dir),
                      sizeB + makeTab(sizeB) if stat[6] < 1024 else sizeKB + makeTab(sizeKB),
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
            
    def run(self, *args):
        if len(args[1]) > 0:
            path = args[1][0]
            try:
                if 'main.py' in path:
                    print(purple('Be careful when running multiple instances of OS. This may cause to stack overflow and CPU halt!'))
                execfile(path)
            except OSError:
                print(red('No such file'))
            except (Exception, KeyboardInterrupt) as e:
                keepRed()
                print('Unhandled exception in file {}:'.format(path))
                sys.print_exception(e)
                resetColor()
            except SystemExit:
                pass
        else:
            print('No file name provided')
            
    def exit(self, *args):
        print(yellow('Shutting down Wroombian...'))
        gc.collect()
        sys.exit()
        #raise SystemExit()
    
    def reboot(self, *args):
        print(yellow('Rebooting...'))
        machine.reset()
    
    def help(self, *args):
        print(green('Available standard self.commands:'))
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
run <path> - run python script
exit - shutdown Wroombian
reboot - restart the device
wifi <key> <arg1> <arg2> - control wifi
''')
        print(blue('Type command with --help (-h) key to show help for this command'))
    
    def wifi_setup(self, *args):
        if len(args[1]) > 0:
            key = args[1][0]
            file = open('/flash/settings.txt')
            settings = json.loads(file.read())
            file.close()
            if key in ['-sta', '--station']:
                self.wifi_handler.connect()
            elif key in ['-ap', '--startAP']:
                self.wifi_handler.startAP()
            elif key in ['-i', '--info']:
                sta_ssid = self.wifi_handler.current_ssid
                sta_ip = self.wifi_handler.sta.ifconfig()[0]
                ap_ssid = self.wifi_handler.ap.config('essid') if self.wifi_handler.ap.active() else 'N/A'
                ap_ip = self.wifi_handler.ap.ifconfig()[0]
                print('STA:', sta_ssid, makeTab(sta_ssid, 15),
                      sta_ip + makeTab(sta_ip, 15),
                      green('Connected') if self.wifi_handler.sta.isconnected() else red('Not connected'))
                print('AP: ', ap_ssid, makeTab(ap_ssid, 15),
                      ap_ip + makeTab(ap_ip, 15),
                      green('Active') if self.wifi_handler.ap.active() else red('Inactive'))
            elif key in ['-s', '--scan']:
                self.wifi_handler.scan()
                print(*[i[0] + makeTab(i[0], 20) + str(i[1]) + ' dBm \t' + i[2] for i in self.wifi_handler.scanned], sep ='\n')
            elif key in ['-cap', '--changeAP'] and len(args[1]) > 1:
                settings['network']['ap'][0] = args[1][1]
                if len(args[1]) > 2:
                    settings['network']['ap'][1] = args[1][2]
                else:
                    settings['network']['ap'][1] = ''
            elif key in ['-a', '--add'] and len(args[1]) > 1:
                if len(args[1]) > 2:
                    settings['network']['wifi'][args[1][1]] = args[1][2]
                else:
                    settings['network']['wifi'][args[1][1]] = ''
            elif key in ['-d', '--delete'] and len(args[1]) > 1:
                res = settings['network']['wifi'].pop(args[1][1], -1)
                if res == -1:
                    print(red('No such SSID found'))
            else:
                print(red('No valid key provided or arguments are missing'))
            file = open('/flash/settings.txt', 'w')
            file.write(json.dumps(settings))
            file.close()
            
            