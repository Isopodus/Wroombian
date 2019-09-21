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

  Download or clone repository folder, than in terminal type:
  ``` bash
  ./firmware/flash.sh
  ```
- Windows

  Install <a href="https://git-scm.com/download/win">Git for Windows</a>, download or clone repository folder, than in Git bash type:
  ``` bash
  ./firmware/flash.sh
  ```
  **OR**
  
  Go to firmware folder and run commands manually (will work for Linux too, do not forget to type valid COM port):
  ```
  esptool --port YOURCOMPORT erase_flash
  esptool --chip esp32 --port YOURCOMPORT --baud 460800 --before default_reset --after no_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 bootloader/bootloader.bin 0xf000 phy_init_data.bin 0x10000 MicroPython.bin 0x8000 partitions_mpy.bin
  ```

## Available commands: 
- `help` - show help message
- `ram` - get RAM load
- `rom` - get ROM load
- `ls` - list files and directories
- `cd <path>` - go to directory
- `cat <path>` - print file content
- `nano <path>` - edit file
- `mkdir <path>` - make directory
- `rmdir <path>` - remove directory
- `touch <path>` - create file
- `rm <path>` - delete file
- `mv <path1> <path2>` - move or rename file
- `run` - run python script
- `reboot` - restart the device
- `exit` - shutdown Wroombian
- `wifi <key> <arg1> <arg2>` - set wifi settings
  
**Wifi command usage**
  <table>
    <tr><td>Key</td>                 <td>arg1</td>            <td>arg2</td>              <td>Description</td></tr>
    <tr><td>-sta, --station</td>     <td>SSID/None</td>       <td>None</td>              <td>Load password of given network from settings and connect/Try to connect to any of known networks</td></tr>
    <tr><td>-ap, --startAP</td>      <td>None</td>            <td>None</td>              <td>Shutdown STA mode and start access point</td></tr>  
    <tr><td>-i, --info</td>          <td>None</td>            <td>None</td>              <td>Get info about curent STA and AP state</td></tr>  
    <tr><td>-s, --scan</td>          <td>None</td>            <td>None</td>              <td>Scan and list available wifi networks</td></tr>  
    <tr><td>-cap, --changeAP</td>    <td>AP SSID</td>         <td>AP password</td>       <td>Change AP SSID adn password</td></tr>  
    <tr><td>-a, --add</td>           <td>STA SSID</td>        <td>STA password</td>      <td>Add new network as known/ Edit existing network password</td></tr>  
    <tr><td>-d, --delete</td>        <td>STA SSID</td>        <td>None</td>              <td>Delete network from list of existing networks</td></tr>  
  </table>

## Connection
To connect to device you can use any Telnet client soft, but for Windows I'd recommend <a href="https://www.putty.org/">PuTTY</a>. For Linux you can use standard `telnet <ip:port>` command. IP adress is shown in serial monitor at startup, port is 23. 

If WiFi is not connecting you can connect to devices WiFi access point with mobile Telnet client after wifi connection timeout happens (10 seconds by default). Default SSID: Wroom32, password: wroomb1an. Mobile Telnet: I'd recommend <a href="https://play.google.com/store/apps/details?id=com.sonelli.juicessh&hl=ru">JuiceSSH</a>. IP is 192.168.4.1, port 23.

## Limitations: 
This is a work in progress version of an OS. If you have any offers or found a bug, feel free to ask in <a href="https://github.com/Isopodus/Wroombian/issues">Issues</a> section.

## Interesting things that can be addded (crossed out are done)
- ~~Changing wifi settings from terminal rather than through file~~
- Changing settings from terminal rather than through file
- --help key for any command
- Installing additional commands
- Simple web browser
