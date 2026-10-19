#include <ctr/svc.h>

__attribute__((naked))
Result
svcCreateResourceLimit(Handle *resourceLimit)
{
        __asm__ volatile(
            "push {r0}\n"
            "svc 0x00000035\n"
            "ldr r2, [sp]\n"
            "str r1, [r2]\n"
            "add sp, sp, #4\n"
            "bx lr");
}