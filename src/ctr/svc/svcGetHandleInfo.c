#include <ctr/svc.h>

__attribute__((naked))
Result
svcGetHandleInfo(s64 *out, Handle handle, u32 type)
{
    __asm__ volatile(
        "push {r0}\n"
        "svc 0x00000029\n"
        "ldr r3, [sp]\n"
        "str r1, [r3]\n"
        "str r2, [r3, #4]\n"
        "add sp, sp, #4\n"
        "bx lr");
}
