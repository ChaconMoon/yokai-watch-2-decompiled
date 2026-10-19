#include <include/types.h>

void svcBreak(u32 reason)
{
        __asm__ volatile("svc 0x0000003c");
}
