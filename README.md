# Wroombian

<strong>Operating system for ESP32</strong>

*Made just for fun, but can be extended to something more useful.*
## Installation
Project is based on slightly modified <a href="https://micropython.org/">Micropython</a> and <a href="https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo">LoBo Micropython</a>. 
To prepare your ESP32 for work you need to erase board flash memory and upload the firmware with help of **flash.sh** script:

1. Install <a href="https://python.org">Python</a>

2. Install **esptool**
``` bash
pip install esptool
```
3. Flash your board
- Linux

  Download or clone repository folder, open `/firmware/flash.sh`, change `FLASH_COMPORT` value to your ESP32 port (e.g. /dev/ttyUSB0). Then in terminal type:
  ``` bash
  ./firmware/flash.sh
  ```
- Windows

  Install <a href="https://git-scm.com/download/win">Git for Windows</a>, download or clone repository folder, open `/firmware/flash.sh`, change `FLASH_COMPORT` value to your ESP32 port (e.g. COM1). Then in Git bash type:
  ``` bash
  ./firmware/flash.sh
  ```
  **OR**
  
  Go to firmware folder and run commands manually (will work for Linux too, do not forget to type valid COM port):
  ```
  esptool --port COM1 erase_flash
  esptool --chip esp32 --port COM1 --baud 460800 --before default_reset --after no_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 bootloader/bootloader.bin 0xf000 phy_init_data.bin 0x10000 MicroPython.bin 0x8000 partitions_mpy.bin
  ```

## Available commands: 
- `help` - show help message
- `ram` - get RAM load
- `rom` - get ROM load
- `ls` - list files and directories
- `cd` - go to directory
- `cat` - print file content
- `nano` - edit file
- `mkdir` - make directory
- `rmdir` - remove directory
- `touch` - create file
- `rm` - delete file
- `mv` - move or rename file
- `run` - run python script file
- `service` - manage detached processes
- `reboot` - restart the device
- `exit` - shutdown Wroombian
- `wifi` - set wifi settings
  
## Commands help
Simply add `--help` key to any command to view it's usage

## Bash files
You can also simply type the name of an existing file and the system will try to execute every line as a single bash command.

## Connection
To connect to device you can use any Telnet client soft, but for Windows I'd recommend <a href="https://www.putty.org/">PuTTY</a>. For Linux you can use standard `telnet <ip:port>` command. IP adress is shown in serial monitor at startup, port is 23. 

If WiFi is not connecting, you can connect to devices WiFi access point (after 10 seconds by default). Default SSID: Wroom32, password: wroomb1an. Than use mobile Telnet client (<a href="https://play.google.com/store/apps/details?id=com.sonelli.juicessh&hl=ru">JuiceSSH</a>) to connect (IP: 192.168.4.1, port: 23).

## Limitations: 
This is a work in progress version of an OS. If you have any offers or found a bug, feel free to ask in <a href="https://github.com/Isopodus/Wroombian/issues">Issues</a> section.

## Interesting things that can be addded (crossed out are done)
- A comand to enable/disable installed command modules 
- pip command (upip handler)
