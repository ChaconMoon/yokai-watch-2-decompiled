#include <ctr/svc.h>

/**
 * @brief svcCreateAddressArbiter
 * @address 0x00151FA0
 * CTR kernel syscall wrapper stub (svc 0x17)
 */
__attribute__((naked))
Result
svcCreateAddressArbiter(Handle *arbiter)
{
        __asm__ volatile(
            "push {r0}\n"
            "svc 0x00000017\n"
            "ldr r2, [sp]\n"
            "str r1, [r2]\n"
            "add sp, sp, #4\n"
            "bx lr");
}
