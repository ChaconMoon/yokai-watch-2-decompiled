#include <ctr/svc.h>

/**
 * @brief svcCreateEvent
 * @address 0x0010AAA8
 * CTR kernel syscall wrapper stub (svc 0x21)
 */
__attribute__((naked))
Result
svcCreateEvent(Handle *event, u32 resetType)
{
        __asm__ volatile(
            "push {r0}\n"
            "svc 0x00000021\n"
            "ldr r2, [sp]\n"
            "str r1, [r2]\n"
            "add sp, sp, #4\n"
            "bx lr");
}
