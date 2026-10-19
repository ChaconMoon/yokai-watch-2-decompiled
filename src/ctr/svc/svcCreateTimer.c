#include <ctr/svc.h>

__attribute__((naked))
Result
svcCreateTimer(Handle *timer, u32 resetType)
{
        __asm__ volatile(
            "push {r0}\n"
            "svc 0x0000002d\n"
            "ldr r2, [sp]\n"
            "str r1, [r2]\n"
            "add sp, sp, #4\n"
            "bx lr");
}
