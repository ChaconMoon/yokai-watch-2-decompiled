#include <ctr/svc.h>

__attribute__((naked))
s64 *func_005F015C(s64 *outTick)
{
    __asm__ volatile(
        "push {r4, lr}\n"
        "mov r4, r0\n"
        "svc 0x00000028\n"
        "strd r0, [r4]\n"
        "mov r0, r4\n"
        "pop {r4, pc}");
}
