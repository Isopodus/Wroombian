#include <Arduino.h>

/*
Command template: command <options> <arguments>
Options should start with "-" (e.g. nano -a file.txt)
*/

class Command
{
public:
    Command(String command, String *commands, const int commandsCount);
    int commandId = -1;
    bool sudo = false;
    String action;

    int optionsIndex = 0;
    int argsIndex = 0;

    String options[5];
    String args[5];
};