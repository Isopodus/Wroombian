#include <Arduino.h>
#include <WiFi.h>
#include <WiFiMulti.h>
#include "SPIFFS.h"
#include "FS.h"
#include "Command.h"
#include <ArduinoJson.h>

class Kernel {
private:
    WiFiServer server;
    WiFiClient client;
    WiFiMulti wifi;

    String username;
    String machineName = "Wroom";
    String password = "5866";
    String sudoPassword = "5866";
    String currentPath = "/";

    const int commandsCount = 13;
    String *commands;
    
    String currentText = " ";
    String buffer = "   ";
    unsigned int cursor = 0;
    bool cursorState = false;//cursor is shown or not

    void pushBuffer(char c);

public :

    //start telnet server
    void
    init();

    //deal with clients
    void handleClients();

    //send message to clients
    void reply(String message);

    //print path
    void printPath();

    //reference help
    void help();

    //print ram available
    void RAM();

    //print rom available
    void ROM();

    //list files in current directory
    void ls();

    //go to directory
    void cd(String path);

    //show file content
    void cat(String filename, bool sudo = false);

    //edit file
    void nano(String filename, String *options, bool sudo = false);

    //create folder
    void mkdir(String path);

    //delete folder
    void rmdir(String path);

    //create file
    void touch(String filename);

    //delete file
    void rm(String filename, bool sudo = false);

    //rename file
    void mv(String filename, String newFilename, bool sudo = false);

    //close connection
    void exit();
    
    //execute some command
    void execute(Command command);

    //check sudo password
    bool checkSudo(String filename, bool sudo);

    //wait till client enters a string
    String waitString();

    void handleInput();

    //wait for command from clients
    Command getCommand();

    //colors
    String green(String text);
    String yellow(String text);
    String red(String text);
    String blue(String text);
};
