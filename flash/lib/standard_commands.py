import os
import gc
import machine
import sys
from pye import pye
from wifi import Wifi
import json
import _thread as thread

from command.command import Command
from command.commands_module import CommandsModule
from colors import *
from wifi import Wifi

def makeTab(line:str, size=25):
    return ' ' * (size - len(line))

class StandardCommandsModule(CommandsModule):
    
    class ram(Command):
        
        def __init__(self):
            super().__init__('Show free, used and total RAM of the device')
        
        def __call__(self, *args):
            gc.collect()
            mem_free = gc.mem_free()
            mem_alloc = gc.mem_alloc()
            mem_total = mem_free + mem_alloc
            print(yellow(" --- RAM usage --- "))
            print(" Free: {}".format(str(mem_free) + ' B' if mem_free < 1024 else str(round(mem_free/1024, 2)) + ' KB'))
            print(" Used: {}".format(str(mem_alloc) + ' B' if mem_alloc < 1024 else str(round(mem_alloc/1024, 2)) + ' KB'))
            print(" Total: {}".format(str(mem_total) + ' B' if mem_total < 1024 else str(round(mem_total/1024, 2)) + ' KB'))

    class rom(Command):
        
        def __init__(self):
            super().__init__('Show free, used and total ROM of the device')
        
        def __call__(self, *args):
            fs_data = os.statvfs('')
            mem_total = fs_data[0] * fs_data[2]
            mem_free = fs_data[0] * fs_data[3]
            mem_alloc = mem_total - mem_free
            print(yellow(" --- ROM usage --- "))
            print(" Free: {}".format(str(mem_free) + ' B' if mem_free < 1024 else str(round(mem_free/1024, 2)) + ' KB'))
            print(" Used: {}".format(str(mem_alloc) + ' B' if mem_alloc < 1024 else str(round(mem_alloc/1024, 2)) + ' KB'))
            print(" Total: {}".format(str(mem_total) + ' B' if mem_total < 1024 else str(round(mem_total/1024, 2)) + ' KB'))

    class ls(Command):
        
        def __init__(self):
            super().__init__('List files and/or directories in current/given derectory')
        
        def __call__(self, *args):
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
             
    class cd(Command):
        
        def __init__(self):
            super().__init__('Change directory to given path')
        
        def __call__(self, *args):
            if len(args[1]) > 0:
                path = args[1][0]
                try:
                    os.chdir(path)

                except OSError as e:
                    print(red('No such directory'))
            else:
                print(red('No directory provided'))
                
    class cat(Command):
        
        def __init__(self):
            super().__init__('Show file content')
        
        def __call__(self, *args):
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
                
    class nano(Command):
        
        def __init__(self):
            super().__init__('Edit file')
        
        def __call__(self, *args):
            if len(args[1]) > 0:
                path = args[1][0]
                try:
                    pye(path)
                except OSError as e:
                    print(red('No such file'))
            else:
                print('No file name provided')
                
    class mkdir(Command):
        
        def __init__(self):
            super().__init__('Create new directory')
        
        def __call__(self, *args):
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
                
    class rmdir(Command):
        
        def __init__(self):
            super().__init__('Remove directory')
        
        def __call__(self, *args):
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
                
    class touch(Command):
        
        def __init__(self):
            super().__init__('Create new file')
        
        def __call__(self, *args):
            if len(args[1]) > 0:
                path = args[1][0]
                try:
                    file = open(path, 'w')
                    file.close()
                except OSError as e:
                    print(red('Not allowed'))
            else:
                print('No file name provided')
                
    class rm(Command):
        
        def __init__(self):
            super().__init__('Remove file')
        
        def __call__(self, *args):
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
                
    class mv(Command):
        
        def __init__(self):
            super().__init__('Move or rename file')
        
        def __call__(self, *args):
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
                
    class run(Command):
        
        def __init__(self):
            super().__init__('Execute python script', {'-d. --detached': ['<path>', 'Run script in separate thread']})
        
        def __call__(self, *args):
            if len(args[1]) > 0:
                path = args[1][0]
                try:
                    if 'main.py' in path:
                        print(purple('Be careful when running multiple instances of OS. This may cause to stack overflow and CPU halt!'))
                    if '-d' in args[1] or '--detached' in args[1]:
                        def run_script_threaded(filename):
                            try:
                                thread.allowsuspend(True)
                                while True:
                                    ntf = thread.getnotification()
                                    if ntf:
                                        if ntf == thread.EXIT:
                                            return
                                        elif ntf == thread.SUSPEND:
                                            while thread.wait() != thread.RESUME:
                                                pass
                                    execfile(filename)
                            except Exception as e:
                                print(red(e))
                                
                        thread.start_new_thread(path, run_script_threaded, (path,))
                        return
                    
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
               
    class service(Command):
        def __init__(self):
            super().__init__('Configure system services',
                             {'-th': ['List threads running'],
                              '-rth': ['<thread_id>', 'Resume thread'],
                              '-pth': ['<thread_id>', 'Pause thread'],
                              '-sth': ['<thread_id>', 'Stop thread'],
                             })
        
        def __call__(self, *args):
            if len(args[1]) > 0:
                if '-th' in args[1]:
                    threads = thread.list(False)
                    states = {0: green('Running'), 1: yellow('Suspended'), 2: yellow('Waiting'), 3: red('Terminated')}
                    types = {1: purple('MAIN'), 2: lPurple('PYTHON'), 3: cyan('SERVICE')}
                    print(yellow('ID               Name               State          Stack      Max stack used       Type'))
                    for t in threads:
                        print(str(t[0]) + makeTab(str(t[0]), 17) + t[2] + makeTab(t[2], 19) + states[t[3]] + makeTab('Terminated', 18) + str(t[4]) + makeTab(str(t[4]), 11) + str(t[5]) + makeTab(str(t[5]), 21) + types[t[1]])
                elif '-rth' in args[1] and len(args[1]) > 1:
                    thread.resume(int(args[1][1]))
                    #thread.notify(int(args[1][1]), thread.RESUME)
                elif '-pth' in args[1] and len(args[1]) > 1:
                    thread.suspend(int(args[1][1]))
                elif '-sth' in args[1] and len(args[1]) > 1:
                    thread.stop(int(args[1][1]))
                    
    
    class exit(Command):
        
        def __init__(self):
            super().__init__('Shutdown Wroombian')
        
        def __call__(self, *args):
            print(yellow('Shutting down Wroombian...'))
            gc.collect()
            sys.exit()
            
    class reboot(Command):
        
        def __init__(self):
            super().__init__('Restart the device')
        
        def __call__(self, *args):
            print(yellow('Rebooting...'))
            machine.reset()
            
    class help(Command):
        
        def __init__(self):
            super().__init__('Show available commands')
            self.helps = []
            
            # Get commands from this module
            for c in dir(StandardCommandsModule):
                attr = getattr(StandardCommandsModule, c, None)
                if isinstance(attr, type) and issubclass(attr, Command) and attr != self.__class__:
                    self.helps.append(attr().help)
            gc.collect()
        
        def __call__(self, *args):
            print(green('Available commands:'))
            for c_help in self.helps:
                print(c_help)
                
            print(blue('Type command with --help (-h) key to show help for this command'))
            
    class wifi(Command):
        
        def __init__(self):
            super().__init__('Handle Wifi connection and settings',
                             {'-init': ['Run initialize sequence'],
                              '-sta, --station': ['<ssid>', '<pass>', 'Disadle AP and try to connect to Wifi network. Uses knowns list if no SSID provided, if no connection estabilished - enables AP. If network has no password, type in only SSID argument'],
                              '-ap, --startAP': ['Disadle STA and activate AP'],
                              '-i, --info': ['Show STA and AP state and IP\'s'],
                              '-s, --scan': ['Show available Wifi networks'],
                              '-cap, --changeAP': ['<ssid>', '<password>', 'Change AP SSID and password'],
                              '-a, --add': ['<ssid>', '<password>', 'Add new Wifi network to knowns list'],
                              '-d, --delete': ['<ssid>', 'Delete Wifi network from knowns list'],
                              '-t, --timeout': ['<timeout>', 'Get or set Wifi connection timeout (10 seconds by default)'],})
        
        def __call__(self, *args):
            if len(args[1]) > 0:
                key = args[1][0]
                file = open('/flash/etc/settings.txt')
                settings = json.loads(file.read())
                file.close()
                if key == '-init':
                    self.wifi_handler = Wifi()
                elif key in ['-sta', '--station']:
                    if len(args[1]) > 1:
                        password = ''
                        ssid = args[1][1]
                        if len(args[1])> 2:
                            password = args[1][2]
                        self.wifi_handler.connect_given(ssid, password)
                    else:
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
                elif key in ['-t', '--timeout']:
                    if len(args[1]) > 1 and args[1][1].isdigit():
                        timeout = int(args[1][1])
                        if timeout != 0:
                            settings['network']['wifiConnectionTimeout'] = timeout
                    print('Timeout:', settings['network']['wifiConnectionTimeout'])
                else:
                    print(red('No valid key provided or arguments are missing'))
                file = open('/flash/etc/settings.txt', 'w')
                file.write(json.dumps(settings))
                file.close()
