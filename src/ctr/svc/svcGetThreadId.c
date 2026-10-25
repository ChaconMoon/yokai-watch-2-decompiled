#include <ctr/svc.h>

/**
 * @brief svcGetThreadId
 * @address 0x00151FC4
 * CTR kernel syscall wrapper stub (svc 0x37)
 */
__attribute__((naked))
Result
svcGetThreadId(u32 *threadId, Handle thread)
{
        __asm__ volatile(
            "push {r0}\n"
            "svc 0x00000037\n"
            "ldr r2, [sp]\n"
            "str r1, [r2]\n"
            "add sp, sp, #4\n"
            "bx lr");
}
