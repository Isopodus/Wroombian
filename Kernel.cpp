#include "Kernel.h"

void Kernel::init()
{
    SPIFFS.begin();

    StaticJsonBuffer<1024> jsonBuffer;
    File configFile = SPIFFS.open("/config.json");
    if (configFile)
    {
        JsonObject &config = jsonBuffer.parseObject(configFile);

        //set config
        for (int i = 0; i < config["wifiSsids"].size(); i++)
        {
            wifi.addAP(config["wifiSsids"][i].as<char *>(), config["wifiPasswords"][i].as<char *>());
        }

        machineName = config["machineName"].as<String>();
        password = config["password"].as<String>();
        sudoPassword = config["sudoPassword"].as<String>();

        //WiFi.softAP("Wroom", "wroomb1an");
    }

    Serial.begin(115200);
    Serial.print("Connecting");
    int tries = 0;
    while (wifi.run() != WL_CONNECTED && tries < 10)
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

void Kernel::execute(Command command)
{
    //try to execute command
    switch (command.commandId)
    {
    case 0:
        RAM();
        break;
    case 1:
        ROM();
        break;
    case 2:
        ls();
        break;
    case 3:
        cd(command.args[0]);
        break;
    case 4:
        cat(command.args[0], command.sudo);
        break;
    case 5:
        nano(command.args[0], command.options, command.sudo);
        break;
    case 6:
        mkdir(command.args[0]);
        break;
    case 7:
        rmdir(command.args[0]);
        break;
    case 8:
        touch(command.args[0]);
        break;
    case 9:
        rm(command.args[0], command.sudo);
        break;
    case 10:
        mv(command.args[0], command.args[1], command.sudo);
        break;
    case 11:
        help();
        break;
    case 12:
        exit();
        break;
    default:
        reply("Unknown command\r\n");
        break;
    }
}

void Kernel::handleClients()
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
            username = waitString();
            reply("Password: ");
            String password = waitString();
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
            //get command from the client and try to execute it
            execute(getCommand());
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

void Kernel::reply(String message)
{
    //Serial.print(message);
    client.print(message);
}

void Kernel::printPath()
{
    reply((String) green(username + "@" + machineName) + ":" + blue(currentPath) + "$ ");
}

int Kernel::countChars(String str, char c)
{
    int count = 0;
    for (int i = 0; i < str.length(); i++)
        if(str[i] == c)
            count++;
    return count;
}

String Kernel::makeTab(String str)
{
    String res = "";
    for (int i = 0; i < 30 - str.length(); i++)
        res += ' ';
    return res;
}

int Kernel::indexOf(String str, char c, int wich)
{
    int count = 0;
    for (int i = 0; i < str.length(); i++)
    {
        if (str[i] == c)
            count++;
        if (count == wich)
            return i;
    }
    return -1;
}

int Kernel::lastIndexOf(String str, char c, int wich)
{
    int count = 0;
    for (int i = str.length() - 1; i >= 0 ; i--)
    {
        if (str[i] == c)
            count++;
        if (count == wich)
            return i;
    }
    return -1;
}

void Kernel::help()
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
            red("Be carefull when editing config.json, wrong changes may cause system malfunction!\r\n"));
}

void Kernel::RAM()
{
    float percent = ((ESP.getHeapSize() - ESP.getFreeHeap()) / float(ESP.getHeapSize())) * 100.0;
    reply((String) "RAM available: " + ESP.getFreeHeap() + " Bytes (" + percent + "% used)\r\n");
}

void Kernel::ROM()
{
    float percent = SPIFFS.usedBytes() / float(SPIFFS.totalBytes()) * 100.0;
    reply((String) "ROM available: " + (SPIFFS.totalBytes() - SPIFFS.usedBytes()) + " Bytes (" + percent + "% used)\r\n");
}

void Kernel::ls()
{
    File dir;
    dir = SPIFFS.open(currentPath);
    String message = "";
    String shownDirs = "";
    File file = dir.openNextFile();
    while (file)
    {
        String path = file.name();

        //current dirname
        // |   |  |  |
        // /some/_path/file.txt
        String dirname = path.substring(currentPath.length() - 1, indexOf(path, '/', countChars(currentPath, '/')));
        String filename = path.substring(path.lastIndexOf('/'));
        if (filename == "/.empty" && shownDirs.indexOf(dirname) == -1)
        {
            message += (String)dirname + makeTab(dirname) + "DIR\r\n";
            if (dirname != "/")
                shownDirs += " " + dirname;
        }
        else if (filename != "/.empty" && shownDirs.indexOf(dirname) == -1)
        {
            message += (String)filename + makeTab(filename) + file.size() + " Bytes\r\n";
            if (dirname != "/")
                shownDirs += " " + dirname;
        }

        file = dir.openNextFile();
    }
    reply(message);
}

void Kernel::cd(String path)
{
    if (currentPath != "/" && path[0] != '/' && path != "..")
        path = "/" + path;
    if(SPIFFS.exists(currentPath + path + "/.empty"))
    {
        currentPath = currentPath + path.substring(0, path.lastIndexOf('/'));
    }
    else if (path == "..")
    {
        if (currentPath != "/")
        {
            if(countChars(currentPath, '/') != 1)
                currentPath = currentPath.substring(0, currentPath.lastIndexOf('/'));
            else
                currentPath = "/";
        }
    }
    else 
        reply("No such file found\r\n");
}

void Kernel::cat(String filename, bool sudo)
{
    if (currentPath != "/" && filename[0] != '/')
        filename = "/" + filename;
    if (SPIFFS.exists(currentPath + filename) && filename.substring(filename.lastIndexOf('/')) != "/.empty")
    {
        if (checkSudo(filename, sudo))
        {
            File file = SPIFFS.open(currentPath + filename);
            while(file.available())
                reply((String)(char)file.read());
            reply("\r\n");
            file.close();
        }
    }
    else
        reply("No such file found\r\n");
}

void Kernel::nano(String filename, String *options, bool sudo)
{
    if (currentPath != "/" && filename[0] != '/')
        filename = "/" + filename;
    if (SPIFFS.exists(currentPath + filename) && filename.substring(filename.lastIndexOf('/')) != "/.empty")
    {
        if (checkSudo(filename, sudo))
        {
            reply("File content:\r\n");
            cat(filename);
            if (options[0] == "-a")
                reply("What to append to file:\r\n");
            else
                reply("New file content:\r\n");
            String content = waitString();
            File file;
            if (options[0] == "-a")
                file = SPIFFS.open(currentPath + filename, "a");
            else
                file = SPIFFS.open(currentPath + filename, "w");

            file.print(content);
            file.close();
        }
    }
    else
        reply("No such file found\r\n");
}

void Kernel::mkdir(String path)
{
    if (currentPath != "/" && path[0] != '/')
        path = "/" + path;
    if (!SPIFFS.exists(currentPath + path + "/.empty"))
    {
        File f = SPIFFS.open(currentPath + path + "/.empty", "w");
        f.close();
    }
}
void Kernel::rmdir(String path)
{
    if (currentPath != "/" && path[0] != '/')
        path = "/" + path;
    if (SPIFFS.exists(currentPath + path + "/.empty"))
    {
        SPIFFS.remove(currentPath + path + "/.empty");
    }
}
void Kernel::touch(String filename)
{
    if (currentPath != "/" && filename[0] != '/')
        filename = "/" + filename;
    if (!SPIFFS.exists(currentPath + filename))
    {
        if (currentPath != "/" && !SPIFFS.exists(currentPath + filename.substring(0, filename.lastIndexOf('/')) + "/.empty"))
        {
            File f = SPIFFS.open(currentPath + filename.substring(0, filename.lastIndexOf('/')) + "/.empty", "w");
            f.close();
        }

        File f = SPIFFS.open(currentPath + filename, "w");
        f.close();
    }
    else
        reply("File already exists\r\n");
}
void Kernel::rm(String filename, bool sudo)
{
    if (currentPath != "/" && filename[0] != '/')
        filename = "/" + filename;
    if (SPIFFS.exists(currentPath + filename) && filename.substring(filename.lastIndexOf('/')) != "/.empty")
    {
        if(checkSudo(filename, sudo))
        {
            SPIFFS.remove(currentPath + filename);
        }
    }
    else
        reply("No such file found\r\n");
}
void Kernel::mv(String filename, String newFilename, bool sudo)
{
    if (currentPath != "/" && filename[0] != '/')
        filename = "/" + filename;
    if (SPIFFS.exists(currentPath + filename) && filename.substring(filename.lastIndexOf('/')) != "/.empty")
    {
        if (checkSudo(filename, sudo))
        {
            SPIFFS.rename(currentPath + filename, currentPath + newFilename);
        }
    }
    else
        reply("No such file found\r\n");
}

void Kernel::exit()
{
    reply("Bye!\r\n");
    client.stop();
}

bool Kernel::checkSudo(String filename, bool sudo)
{
    //sudo check for special files
    if (filename == "config.json")
    {
        if (sudo)
        {
            reply("Password for sudo: ");
            String password = waitString();
            if (password != sudoPassword)
            {
                reply("Wrong password\r\n");
                return false;
            }
            else
                return true;
        }
        else
        {
            reply("Permission denied\r\n");
            return false;
        }
    }
    return true;
}

String Kernel::waitString()
{
    while (!client.available() && client.connected()) { /*wait*/}

    String result = "";
    while (client.available())
    {
        result += (char)client.read();
        delay(3);
    }
    result = result.substring(0, result.length() - 2);
    Serial.println(result);
    return result;
}

Command Kernel::getCommand()
{
    return Command(waitString(), commands, commandsCount);
}

String Kernel::green(String text)
{
    return "\u001b[32m" + text + "\u001b[0m";
}

String Kernel::yellow(String text)
{
    return "\u001b[33m" + text + "\u001b[0m";
}
String Kernel::red(String text)
{
    return "\u001b[31m" + text + "\u001b[0m";
}
String Kernel::blue(String text)
{
    return "\u001b[34;1m" + text + "\u001b[0m";
}
