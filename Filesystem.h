#include <Arduino.h>
#include "SPIFFS.h"
#include "FS.h"

class Filesystem
{
private:
    int countChars(String str, char c);
    void checkSlash(String &path);
    String makeTab(String str);

public:
    String currentPath = "/";

    void init(); // initialize filesystem
    bool dirExists(String &dirPath); // check if directory exists (current path included)
    bool fileExists(String &filePath); // check if file exists (current path included)
    bool goToDir(String dirPath);      // go to some directory (current path included)
    bool goBack();  // go 1 directory back
    String readFile(String filePath); // get content of a file
    File getFile(String filePath, String mode = "r"); // get file object

    void mkdir(String dirPath); // make directory
    void rmdir(String dirPath); // remove directory
    bool touch(String filePath); // create file
    void rm(String filePath); // remove file
    void mv(String filePath, String newFilePath); // rename or move file

    String ls(); // get list of files and dirs as message

    Filesystem();
    ~Filesystem();
};


