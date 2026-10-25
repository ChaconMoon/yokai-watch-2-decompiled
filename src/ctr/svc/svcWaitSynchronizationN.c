#include <ctr/svc.h>
#include <stdbool.h>

__attribute__((naked))
Result
svcWaitSynchronizationN(s32 *outIndex, const Handle *handles, s32 handleCount, bool waitAll, s64 timeout)
{
    __asm__ volatile(
        "push {r0, r4}\n"
        "ldr r0, [sp, #8]\n"
        "ldr r4, [sp, #12]\n"
        "svc 0x00000025\n"
        "ldr r2, [sp]\n"
        "str r1, [r2]\n"
        "add sp, sp, #4\n"
        "pop {r4}\n"
        "bx lr");
}
