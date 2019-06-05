#include "Kernel.h"

void Kernel::init()
{
    fs.init();

    StaticJsonBuffer<1024> jsonBuffer;
    JsonObject &config = jsonBuffer.parseObject(fs.readFile("config.json"));
    
    for (int i = 0; i < config["wifiSsids"].size(); i++)
    {
        wifi.addAP(config["wifiSsids"][i].as<char *>(), config["wifiPasswords"][i].as<char *>());
    }

    machineName = config["machineName"].as<String>();
    password = config["password"].as<String>();
    sudoPassword = config["sudoPassword"].as<String>();

    WiFi.softAP(AP_SSID, AP_PASS);

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

    // start telnet server
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
    case 13:
        python(command.args[0], command.options, command.sudo);
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
    reply((String) green(username + "@" + machineName) + ":" + blue(fs.currentPath) + "$ ");
}

void Kernel::help()
{
    reply((String)
          green("Available commands:\r\n") +
          blue((String)"help - show this message\r\n" +
          "ram - get RAM load\r\n" +
          "rom - get ROM load\r\n" +
          "ls - list files and directories\r\n" +
          "cd <path> - go to directory\r\n" +
          "cat <path> - print file content\r\n" +
          "nano [-a] <path> - rewrite file, -a to append\r\n" +
          "mkdir <path> - make directory\r\n" +
          "rmdir <path> - remove directory\r\n" +
          "touch <path> - create file\r\n" +
          "rm <path> - delete file\r\n" +
          "mv <path1> <path2> - move or rename file\r\n" +
          "python [-v] <path> - run python file, -v for verbose mode\r\n" +
          "exit - close connection and exit\r\n") +
          yellow("You can use cat and nano with sudo to see or edit config file\r\n") +
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
    int available = SPIFFS.totalBytes() - SPIFFS.usedBytes();
    reply((String) "ROM available: " + available + " Bytes (" + percent + "% used)\r\n");
}

void Kernel::ls()
{
    reply(fs.ls());
}

void Kernel::cd(String path)
{
    if (path == "..")
    {
        fs.goBack();
    }
    else if (!fs.goToDir(path))
        reply("No such directory found\r\n");
}

void Kernel::cat(String filename, bool sudo)
{

    if (fs.fileExists(filename))
    {
        if (checkSudo(filename, sudo))
        {
            File file = fs.getFile(filename);
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
    if (fs.fileExists(filename))
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
                file = fs.getFile(filename, "a");
            else
                file = fs.getFile(filename, "w");

            file.print(content);
            file.close();
        }
    }
    else
        reply("No such file found\r\n");
}

void Kernel::mkdir(String path)
{
    fs.mkdir(path);
}
void Kernel::rmdir(String path)
{
    fs.rmdir(path);
}
void Kernel::touch(String filename)
{
    if (!fs.fileExists(filename))
    {
        fs.touch(filename);
    }
    else
        reply("File already exists\r\n");
}
void Kernel::rm(String filename, bool sudo)
{
    if (fs.fileExists(filename))
    {
        if(checkSudo(filename, sudo))
        {
            fs.rm(filename);
        }
    }
    else
        reply("No such file found\r\n");
}
void Kernel::mv(String filename, String newFilename, bool sudo)
{
    if (fs.fileExists(filename))
    {
        if (checkSudo(filename, sudo))
        {
            fs.mv(filename, newFilename);
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

void Kernel::python(String filename, String *options, bool sudo)
{
    if (fs.fileExists(filename))
    {
        if (checkSudo(filename, sudo))
        {
            String code = fs.readFile(filename);
            reply("Input: ");
            String input = waitString();

            // run code
            if (pyInterpreter.runCode(code, input))
            {
                if (pyInterpreter.errors == "")
                    reply("\r\n" + green("Result:\r\n"));
                else
                    reply("\r\n" + yellow("Result:\r\n"));

                reply(pyInterpreter.result + "\r\n");

                // show stats if verbose option is set
                if (options[0] == "-v")
                    reply(blue("Stats:\r\n" + pyInterpreter.stats + "\r\n"));

                // shos errors if needed
                if (pyInterpreter.errors != "")
                    reply("\r\n" + red("Errors:\r\n" + pyInterpreter.errors + "\r\n"));
            }
            else
                reply("\r\n" + red("Connection refused or file is empty\r\n"));
        }
    }
    else
        reply("No such file found\r\n");
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
