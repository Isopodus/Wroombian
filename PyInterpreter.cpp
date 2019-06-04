#include "PyInterpreter.h"

bool PyInterpreter::runCode(String code, String input)
{
    if (code == "")
        return false;

    client.begin(REXTESTER_HOST);
    
    StaticJsonBuffer<2048> jsonBuffer;
    JsonObject &payloadJson = jsonBuffer.createObject();
    payloadJson["LanguageChoice"] = "5";
    payloadJson["Program"] = code;
    payloadJson["Input"] = input;
    payloadJson["CompilerArgs"] = "";

    String payload;
    payloadJson.prettyPrintTo(payload);
    
    //Serial.println(payload);

    // make request with code
    client.addHeader("Content-Type", "application/json");
    int status = client.POST(payload);
    if (status == 200)
    {
        // parse response and save it
        JsonObject &responseJson = jsonBuffer.parseObject(client.getStream());
        result = responseJson["Result"].as<String>();
        if (result == "null")
            result = "";
        errors = responseJson["Errors"].as<String>();
        if (errors == "null")
            errors = "";
        stats = responseJson["Stats"].as<String>();

        // add \r to every \n
        result.replace("\n", "\r\n");
        errors.replace("\n", "\r\n");
        stats.replace("\n", "\r\n");

        return true;
    }

    return false;
}