#include <ctr/svc.h>

void svcExitThread(void)
{
    __asm__ volatile("svc 0x00000009");
}
