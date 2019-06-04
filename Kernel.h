#include <Arduino.h>
#include <WiFi.h>
#include <WiFiMulti.h>
#include "Command.h"
#include <ArduinoJson.h>
#include "Filesystem.h"
#include "PyInterpreter.h"

#define AP_SSID "Wroom"
#define AP_PASS "wroomb1an"

class Kernel {
private:
    WiFiServer server;
    WiFiClient client;
    WiFiMulti wifi;

    Filesystem fs;
    PyInterpreter pyInterpreter;

    String username;
    String machineName = "Wroom32";
    String password = "";
    String sudoPassword = "";

    static const int commandsCount = 14;
    String commands[commandsCount] = {
        "ram",
        "rom",
        "ls",
        "cd",
        "cat",
        "nano",
        "mkdir",
        "rmdir",
        "touch",
        "rm",
        "mv",
        "help",
        "exit",
        "python"
    };

public :

    //initialize server
    void init();

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
    
    //run python code
    void python(String filename, String *options, bool sudo);

    //execute some command
    void execute(Command command);

    //check sudo password
    bool checkSudo(String filename, bool sudo);

    //wait till client enters a string
    String waitString();

    void handleInput();

    void printCurrentText();

    //wait for command from clients
    Command getCommand();

    //colors
    String green(String text);
    String yellow(String text);
    String red(String text);
    String blue(String text);

};
