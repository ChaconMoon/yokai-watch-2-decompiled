#include <ctr/svc.h>

/**
 * @brief func_0013EC5C
 * @address 0x0013EC5C
 * CTR kernel syscall wrapper stub (svc 0x0A)
 */
void func_0013EC5C(s64 nanoseconds)
{
    __asm__ volatile("svc 0x0000000A");
}
