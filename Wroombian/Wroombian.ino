#include "Kernel.h"

Kernel kernel;

void setup()
{
    kernel.init();
}
void loop()
{
    kernel.handleClients();
}
