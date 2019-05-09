#include "Core.h"

Core core;

void setup()
{
    core.init();
}
void loop()
{
    core.handleClients();
}
