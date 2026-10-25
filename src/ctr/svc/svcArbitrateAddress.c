#include <ctr/svc.h>

__attribute__((naked))
Result
svcArbitrateAddress(Handle arbiter, u32 addr, u32 type, s32 value, s64 timeout)
{
    __asm__ volatile(
        "push {r4, r5}\n"
        "ldr r4, [sp, #8]\n"
        "ldr r5, [sp, #12]\n"
        "svc 0x00000022\n"
        "pop {r4, r5}\n"
        "bx lr");
}
