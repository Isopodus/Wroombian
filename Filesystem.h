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

    void init();
    bool dirExists(String dirPath);
    bool fileExists(String filePath);
    bool goToDir(String dirPath);
    bool goBack();
    String readFile(String filePath);
    File getFile(String filePath, String mode = "r");

    void mkdir(String dirPath);
    void rmdir(String dirPath);
    bool touch(String filePath);
    void rm(String filePath);
    void mv(String filePath, String newFilePath);

    String ls();

    Filesystem();
    ~Filesystem();
};


