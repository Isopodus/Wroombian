#include "Command.h"

Command::Command(String command, String *commands, const int commandsCount)
{
    //check for sudo
    if (command.startsWith("sudo"))
    {
        this->sudo = true;
        if (command.indexOf(' ') != -1)
            command.remove(0, command.indexOf(' ') + 1);
        else
            return;
    }

    //get action
    if (command.indexOf(' ') != -1)
    {
        this->action = command.substring(0, command.indexOf(' '));
        command.remove(0, command.indexOf(' ') + 1);

        //find command
        for (int i = 0; i < commandsCount; i++)
        {
            if (commands[i] == this->action)
            {
                commandId = i;
                break;
            }
        }
        
    }
    else
    {
        this->action = command;

        //find command
        for (int i = 0; i < commandsCount; i++)
        {
            if (commands[i] == this->action)
            {
                commandId = i;
                break;
            }
        }
        return;
    }

    //check for options
    while (command[0] == '-')
    {
        if (command.indexOf(' ') != -1)
        {
            this->options[optionsIndex] = command.substring(0, command.indexOf(' '));
            command.remove(0, command.indexOf(' ') + 1);
            optionsIndex++;
        }
        else
        {
            this->options[optionsIndex] = command;
            optionsIndex++;
            return;
        }
    }

    //get arguments
    while(command.length())
    {
        if (command.indexOf(' ') != -1)
        {
            this->args[argsIndex] = command.substring(0, command.indexOf(' '));
            command.remove(0, command.indexOf(' ') + 1);
            argsIndex++;
        }
        else
        {
            this->args[argsIndex] = command;
            argsIndex++;
            return;
        }
    }
}