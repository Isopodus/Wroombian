#include <Arduino.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>

#define REXTESTER_HOST "https://rextester.com/rundotnet/api" // rextester URL

class PyInterpreter {
private:
    HTTPClient client;

public:
    String result = "";
    String errors = "";
    String stats = "";

    bool runCode(String code, String input = "");
};
