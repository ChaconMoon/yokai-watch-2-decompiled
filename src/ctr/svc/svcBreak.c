#include <ctr/svc.h>

/**
 * @brief svcBreak
 * @address 0x0013EC48
 * CTR kernel syscall wrapper stub (svc 0x3C)
 */
void svcBreak(u32 reason)
{
    __asm__ volatile("svc 0x0000003C");
}
