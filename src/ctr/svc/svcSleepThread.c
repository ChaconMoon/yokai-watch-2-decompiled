#include <ctr/svc.h>

/**
 * @brief svcSleepThread
 * @address 0x00151FBC
 * CTR kernel syscall wrapper stub (svc 0x28)
 */
void svcSleepThread(s64 nanoseconds)
{
    __asm__ volatile("svc 0x00000028");
}
