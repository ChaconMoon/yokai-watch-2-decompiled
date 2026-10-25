#include <ctr/svc.h>

/**
 * @brief svcExitProcess
 * @address 0x00104778
 * CTR kernel syscall wrapper stub (svc 0x03)
 */
void svcExitProcess(void)
{
    __asm__ volatile("svc 0x00000003");
}
