#include <ctr/svc.h>

/**
 * @brief svcWaitSynchronization1
 * @address 0x0018A868
 * CTR kernel syscall wrapper stub (svc 0x24)
 */
Result svcWaitSynchronization1(Handle handle, s64 nanoseconds)
{
        __asm__ volatile("svc 0x00000024");
}
