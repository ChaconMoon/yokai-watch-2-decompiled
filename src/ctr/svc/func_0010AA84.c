#include <ctr/svc.h>

__attribute__((naked))
Result
func_0010AA84(u32 *outAddr, u32 addr0, u32 addr1, u32 size, u32 op, u32 perm)
{
    __asm__ volatile(
        "push {r0, r4}\n"
        "ldr r0, [sp, #8]\n"
        "ldr r4, [sp, #12]\n"
        "svc 0x00000001\n"
        "ldr r2, [sp]\n"
        "str r1, [r2]\n"
        "add sp, sp, #4\n"
        "pop {r4}\n"
        "bx lr");
}
