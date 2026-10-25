#include <ctr/svc.h>

/**
 * @brief svcCloseHandle
 * @address 0x0018A714
 * CTR kernel syscall wrapper stub (svc 0x23)
 */
Result svcCloseHandle(Handle handle)
{
    __asm__ volatile("svc 0x00000023");
}
