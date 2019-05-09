#include "Core.h"

void Core::init()
{
    SPIFFS.begin();

    StaticJsonBuffer<1024> jsonBuffer;
    File configFile = SPIFFS.open("/config.json");
    if (configFile)
    {
        JsonObject &config = jsonBuffer.parseObject(configFile);

        //set config
        WiFi.mode(WIFI_AP_STA);
        WiFi.begin(config["ssid"].as<char *>(), config["wifiPassword"].as<char *>());

        machineName = config["machineName"].as<String>();
        password = config["password"].as<String>();
        sudoPassword = config["sudoPassword"].as<String>();

        WiFi.softAP(machineName.c_str(), "wroomb1an");
    }

    Serial.begin(115200);
    Serial.print("Connecting");
    int tries = 0;
    while (WiFi.status() != WL_CONNECTED && tries < 10)
    {
        Serial.print(".");
        delay(500);
        tries++;
    }
    Serial.println();
    Serial.print("Ready! Local IP is ");
    Serial.print(WiFi.localIP());
    Serial.println();

    server.begin(23);
    server.setNoDelay(true);
}

void Core::handleClients()
{
    //check if there are any new client
    if (server.hasClient())
    {
        if (!client || !client.connected())
        {
            if (client)
                client.stop();
            client = server.available();
            Serial.print((String) "Someone connected! IP: ");
            Serial.println(client.remoteIP());

            client.readString();
            //welcome!
            reply(yellow("Welcome to Wroombian!\r\n"));
            RAM();
            ROM();
            reply("Please, enter your credentials:");

            //authenticate
            reply("\r\nUsername: ");
            username = getCommand();
            reply("Password: ");
            String password = getCommand();
            if(password != this->password)
            {
                reply(red("\r\nPassword incorrect! Bye!"));
                client.stop();
            }
            else
                printPath();
        }
    }

    //check client for data
    if (client && client.connected())
    {
        if (client.available())
        {
            //get command from the client and tyr to execute it
            String command = getCommand();
            execute(command);
            printPath();
        }
    }
    else
    {
        if (client)
        {
            client.stop();
        }
    }
}

void Core::reply(String message)
{
    Serial.print(message);
    client.print(message);
}

void Core::printPath()
{
    reply((String) green(username + "@" + machineName) + ":" + blue(currentPath) + "$ ");
}

void Core::help()
{
    reply((String)
            green("Available commands:\r\n") +
            blue("help - show this message\r\n") +
            blue("ram - get RAM load\r\n") +
            blue("rom - get ROM load\r\n") +
            blue("ls - list files\r\n") +
            blue("cd <path> - go to file\r\n") +
            blue("cat <path> - print file content\r\n") +
            blue("nano <path> - rewrite file\r\n") +
            blue("nano -a <path> - append to file\r\n") +
            blue("mkdir <path> - make directory\r\n") +
            blue("rmdir <path> - remove directory\r\n") +
            blue("touch <path> - create file\r\n") +
            blue("rm <path> - delete file\r\n") +
            blue("mv <path1> <path2> - move or rename file\r\n") +
            blue("exit - close connection and exit\r\n") +
            yellow("You can use cat and nano with sudo to see or edit config file\r\n") +
            red("ls does not show empty folders\r\n") +
            red("cd works only if there is some file at the end of given path (f.e. cd path/file.txt)\r\n") +
            red("Be carefull when editing config.json, wrong changes may cause system malfunction!"));
}

void Core::RAM()
{
    float percent = ((ESP.getHeapSize() - ESP.getFreeHeap()) / float(ESP.getHeapSize())) * 100.0;
    reply((String) "RAM available: " + ESP.getFreeHeap() + " Bytes (" + percent + "% used)\r\n");
}

void Core::ROM()
{
    float percent = SPIFFS.usedBytes() / float(SPIFFS.totalBytes()) * 100.0;
    reply((String) "ROM available: " + (SPIFFS.totalBytes() - SPIFFS.usedBytes()) + " Bytes (" + percent + "% used)\r\n");
}

void Core::ls()
{
    File dir = SPIFFS.open(currentPath);
    File file = dir.openNextFile();
    while (file)
    {
        reply((String)file.name() + "\t\t" + file.size() + " Bytes\r\n");
        file = dir.openNextFile();
    }
}

void Core::cd(String path)
{
    if(SPIFFS.exists(currentPath + path))
    {
        currentPath = currentPath + path.substring(0, path.lastIndexOf('/') + 1);
    }
    else if (path == "..")
    {
        if (currentPath != "/")
        {
            String copy = currentPath;
            copy.remove(currentPath.lastIndexOf('/'));
            currentPath = copy.substring(0, copy.lastIndexOf('/') + 1);
        }
    }
    else 
        reply("No such file found\r\n");
}

void Core::cat(String filename)
{
    if (SPIFFS.exists(currentPath + filename))
    {
        File file = SPIFFS.open(currentPath + filename);
        while(file.available())
            reply((String)(char)file.read());
        reply("\r\n");
        file.close();
    }
    else
        reply("No such file found\r\n");
}

void Core::nano(String filename)
{
    String f;
    f = filename.substring(0, 2) == "-a" ? filename.substring(3) : filename;
    if (SPIFFS.exists(currentPath + f))
    {
        reply("File content:\r\n");
        cat(f);
        if (filename.substring(0, 2) == "-a")
            reply("What to append to file:\r\n");
        else
            reply("New file content:\r\n");
        String content = getCommand();
        File file;
        if (filename.substring(0, 2) == "-a")
            file = SPIFFS.open(currentPath + f, filename.substring(1, 2).c_str());
        else
            file = SPIFFS.open(currentPath + f, "w");

        file.print(content);
        file.close();
    }
    else
        reply("No such file found\r\n");
}

void Core::mkdir(String path)
{
    SPIFFS.mkdir(currentPath + path);
}
void Core::rmdir(String path)
{
    SPIFFS.rmdir(currentPath + path);
}
void Core::touch(String filename)
{
    if (!SPIFFS.exists(currentPath + filename))
    {
        File f = SPIFFS.open(currentPath + filename, "w");
        f.close();
    }
    else
        reply("File already exists\r\n");
}
void Core::rm(String filename)
{
    if (SPIFFS.exists(currentPath + filename))
        SPIFFS.remove(currentPath + filename);
    else
        reply("No such file found\r\n");
}
void Core::mv(String filename, String newFilename)
{
    if (SPIFFS.exists(currentPath + filename))
        SPIFFS.rename(currentPath + filename, currentPath + newFilename);
    else
        reply("No such file found\r\n");
}

void Core::exit()
{
    reply("Bye!\r\n");
    client.stop();
}

void Core::execute(String command)
{
    //parse command and try to execute it
    if(command == "ram")
        RAM();
    else if (command == "rom")
        ROM();
    else if (command == "ls")
        ls();
    else if (command.substring(0, 2) == "cd")
        cd(command.substring(3));
    else if (command.substring(0, 3) == "cat")
    {
        if (command.substring(4) != "config.json")
            cat(command.substring(4));
        else
            reply("Permission denied\r\n");
    }
    else if (command.substring(0, 8) == "sudo cat")
    {
        reply("Password for sudo: ");
        String password = getCommand();
        if(password == sudoPassword)
            cat(command.substring(9));
        else
            reply("Wrong password\r\n");
    }
    else if (command.substring(0, 4) == "nano")
    {
        if (command.substring(5) != "config.json")
            nano(command.substring(5));
        else
            reply("Permission denied\r\n");
    }
    else if (command.substring(0, 9) == "sudo nano")
    {
        reply("Password for sudo: ");
        String password = getCommand();
        if (password == sudoPassword)
            nano(command.substring(10));
        else
            reply("Wrong password\r\n");
    }
    else if (command.substring(0, 5) == "mkdir")
    {
        mkdir(command.substring(6));
    }
    else if (command.substring(0, 5) == "rmdir")
    {
        rmdir(command.substring(6));
    }
    else if (command.substring(0, 5) == "touch")
    {
        touch(command.substring(6));
    }
    else if (command.substring(0, 2) == "rm")
    {
        if (command.substring(3) != "config.json")
            rm(command.substring(3));
        else
            reply("Permission denied\r\n");
    }
    else if (command.substring(0, 2) == "mv")
    {
        if (command.substring(3) != "config.json")
            mv(command.substring(3, command.lastIndexOf(' ')), command.substring(command.lastIndexOf(' ') + 1));
        else
            reply("Permission denied\r\n");
    }
    else if (command.substring(0, 4) == "help")
    {
        help();
    }
    else if (command.substring(0, 4) == "exit")
    {
        exit();
    }
    else
        reply("Unknown command\r\n");
}

String Core::getCommand()
{
    while (!client.available() && client.connected()) { /*wait*/}

    String command = "";
    while (client.available())
    {
        command += (char)client.read();
        delay(3);
    }
    Serial.println(command.substring(0, command.length() - 2));
    
    return command.substring(0, command.length() - 2);
}

String Core::green(String text)
{
    return "\u001b[32m" + text + "\u001b[0m";
}

String Core::yellow(String text)
{
    return "\u001b[33m" + text + "\u001b[0m";
}
String Core::red(String text)
{
    return "\u001b[31m" + text + "\u001b[0m";
}
String Core::blue(String text)
{
    return "\u001b[34;1m" + text + "\u001b[0m";
}
