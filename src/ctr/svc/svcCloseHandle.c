#include <include/types.h>

void svcCloseHandle(void)
{
        __asm__ volatile("svc 0x00000023");
}
