#include <ctr/svc.h>

__attribute__((naked))
Result
svcControlMemory(u32 *addrOut, u32 addr0, u32 addr1, u32 size, u32 op, u32 perm)
{
        __asm__ volatile(
            "push {r0}\n"
            "svc 0x0000000b\n"
            "ldr r2, [sp]\n"
            "str r1, [r2]\n"
            "add sp, sp, #4\n"
            "bx lr");
}
