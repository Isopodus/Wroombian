# Wroombian
<strong>ESP32 Telnet linux emulator</strong>

*Made just for fun, but can be extended to something more useful with your help.*
## Installation
Project uses internal SPIFFS of ESP32 as filesystem. In order to make it work you need to install <a href="https://github.com/me-no-dev/arduino-esp32fs-plugin">Arduino ESP32 filesystem uploader</a> to upload "data" folder contents to ESP. You should also change the default settings in "config.json" file, before uploading it to SPIFFS. Set Partition scheme of board to "No OTA 2MB APP/2MB SPIFFS" (optional but recommended) and than upload code with regular Arduino IDE.

## Available commands: 
- help - show help message
- ram - get RAM load
- rom - get ROM load
- ls - list files and directories
- cd <path> - go to directory
- cat <path> - print file content
- nano <path> - rewrite file
- nano -a <path> - append to file
- mkdir <path> - make directory
- rmdir <path> - remove directory
- touch <path> - create file
- rm <path> - delete file
- mv <path1> <path2> - move or rename file
- exit - close connection and exit
  
You can use cat and nano with sudo to see or edit config file (e.g. sudo cat config.json).
Be carefull when editing config.json from terminal, wrong changes may cause system malfunction!

## Limitations: 
SPIFFS on ESP32 does not fully support folders, so to "simulate" them i'm creating ".empty" file in every folder created.

## Connection
To connect to device you can use Telnet client soft, but I'd recommend <a href="https://www.putty.org/">PuTTY</a> (e.g. standard Windows 7 Telnet client works badly because is sends any printed letter immidiately). IP adress is shown in serial monitor at startup, port is 23. 

If WiFi is not connecting you can connect to devices WiFi access point (SSID: Wroom (can be changed in Kernel.h), Password: wroomb1an) and connect with mobile Telnet (I'd recommend <a href="https://play.google.com/store/apps/details?id=com.sonelli.juicessh&hl=ru">JuiceSSH</a> for same reason as for desktop PC's). IP is 192.168.4.1, port 23.

## Interesting things that can be addded
- ~~Folders support~~
- Changing settings from terminal rather than through file
- External SD card support
- Web python interpreter (see <a href="https://rextester.com/main">Rextester</a>)
- Simple web browser

#### Additional info
This can also be ported to ESP8266, but you need to use SPIFFS functions of ESP8266 SPIFFS class.
