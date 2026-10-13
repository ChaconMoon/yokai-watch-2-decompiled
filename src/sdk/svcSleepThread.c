#include <include/types.h>

void svcSleepThread(s64 nanoseconds)
{
        __asm__ volatile("svc 0x00000028");
}
