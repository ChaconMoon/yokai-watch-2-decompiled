#include <ctr/svc.h>

/**
 * @brief svcExitThread
 * @address 0x0012F190
 * CTR kernel syscall wrapper stub (svc 0x09)
 */
void svcExitThread(void)
{
    __asm__ volatile("svc 0x00000009");
}
