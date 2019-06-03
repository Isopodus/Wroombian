#include "Filesystem.h"

Filesystem::Filesystem()
{
}

Filesystem::~Filesystem()
{
}

void Filesystem::init()
{
    SPIFFS.begin();
}

String Filesystem::makeTab(String str)
{
    String res = "";
    for (int i = 0; i < 30 - str.length(); i++)
        res += ' ';
    return res;
}

void Filesystem::checkSlash(String &path)
{
    // if we are not in root and there is no slash' in the path already
    if (currentPath != "/" && path[0] != '/' && path != "..")
        path = "/" + path; // add slash
}

int Filesystem::countChars(String str, char c)
{
    int count = 0;
    for (int i = 0; i < str.length(); i++)
        if (str[i] == c)
            count++;
    return count;
}

String Filesystem::readFile(String filePath)
{
    checkSlash(filePath);
    String content = "";
    
    File file = SPIFFS.open(currentPath + filePath);
    if (file)
    {
        content = file.readString();
        file.close();   
    }
    Serial.println(content);
    return content;
}

File Filesystem::getFile(String filePath, String mode)
{
    checkSlash(filePath);

    File file = SPIFFS.open(currentPath + filePath, mode.c_str());
    if (file)
        return file;
    return File();
}

bool Filesystem::dirExists(String dirPath)
{
    checkSlash(dirPath);
    Serial.println(dirPath);

    //check if there is .empty file in dir
    if (SPIFFS.exists(currentPath + dirPath + "/.empty"))
        return true;
    else
        return false;
}

bool Filesystem::fileExists(String filePath)
{
    checkSlash(filePath);

    //check if there is such file and it is not .empty file
    if (SPIFFS.exists(currentPath + filePath) && filePath.substring(filePath.lastIndexOf('/')) != "/.empty")
        return true;
    else
        return false;
}

bool Filesystem::goToDir(String dirPath)
{
    // if such dir exists
    if (dirExists(dirPath))
    {
        // change path to requested dir
        currentPath = currentPath + dirPath.substring(0, dirPath.lastIndexOf('/'));
        return true;
    }
    return false;
}

bool Filesystem::goBack()
{
    // if we are not in root
    if (currentPath != "/")
    {
        // go 1 dir back
        if (currentPath.length() > 1 && currentPath.indexOf('/') != 0)
        {
            currentPath = currentPath.substring(0, currentPath.lastIndexOf('/'));
            return false;
        }
        else
        {
            currentPath = "/";
            return true;
        }
    }
    return false;
}

void Filesystem::mkdir(String dirPath)
{
    if (!dirExists(dirPath))
    {
        File f = SPIFFS.open(currentPath + dirPath + "/.empty", "w");
        f.close();
    }
}

void Filesystem::rmdir(String dirPath)
{
    if (dirExists(dirPath))
        SPIFFS.remove(currentPath + dirPath + "/.empty");
}

bool Filesystem::touch(String filePath)
{
    if (!fileExists(filePath))
    {
        SPIFFS.remove(currentPath + filePath);
    }

    return false;
}

String Filesystem::ls()
{
    String message = ""; // message to reply
    String shown = "";   // directories or files that were already shown (separated with spaces)

    File dir = SPIFFS.open(currentPath);
    File file = dir.openNextFile();

    while (file)
    {
        String path = file.name();
        //Serial.println(path);

        if (path.length() > 1 && path != currentPath.substring(1))
        {
            String filename = path.substring(path.lastIndexOf('/'));

            path.remove(0, currentPath.length());

            //current dirname
            // |   |  |  |
            // /some/_path/file.txt
            String dirname = path.substring(0, path.indexOf('/'));
            
            if (filename == "/.empty" && shown.indexOf(dirname) == -1) // if it is directory and it was not added
            {
                message += (String)dirname + makeTab(dirname) + "DIR\r\n";
                shown += dirname + " ";
            }
            else if (filename != "/.empty" && shown.indexOf(filename) == -1) // if it is file and it was not added
            {
                message += (String)filename + makeTab(filename) + (int)file.size() + " Bytes\r\n";
                shown += filename + " ";
            }
        }

        file = dir.openNextFile();
    }
    return message;
}

void Filesystem::rm(String filePath)
{
    checkSlash(filePath);
    SPIFFS.remove(currentPath + filePath);
}

void Filesystem::mv(String filePath, String newFilePath)
{
    checkSlash(filePath);
    SPIFFS.rename(currentPath + filePath, currentPath + newFilePath);
}