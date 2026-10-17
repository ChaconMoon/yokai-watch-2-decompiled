#include <include/types.h>

void svcExitProcess(void)
{
    __asm__ volatile ("svc 0x00000003");
}
