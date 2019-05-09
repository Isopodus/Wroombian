#include <Arduino.h>
#include <WiFi.h>
#include "SPIFFS.h"
#include "FS.h"
#include <ArduinoJson.h>

class Core {
private:
    WiFiServer server;
    WiFiClient client;

    String username;
    String machineName = "Wroom";
    String password = "5866";
    String sudoPassword = "5866";
    String currentPath = "/";

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
    void cat(String filename);

    //edit file
    void nano(String filename);

    //create folder
    void mkdir(String path);

    //delete folder
    void rmdir(String path);

    //create file
    void touch(String filename);

    //delete file
    void rm(String filename);

    //rename file
    void mv(String filename, String newFilename);

    //close connection
    void exit();
    
    //execute some command
    void execute(String command);

    //wait for command from clients
    String getCommand();

    //colors
    String green(String text);
    String yellow(String text);
    String red(String text);
    String blue(String text);
};
