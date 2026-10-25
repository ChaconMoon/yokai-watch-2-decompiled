#include <ctr/svc.h>

__attribute__((naked))
void func_0013EC38(u32 arg0, u32 arg1)
{
    __asm__ volatile(
        "mov r2, r1\n"
        "mov r1, r0\n"
        "mov r0, #4\n"
        "mov r0, r0\n"
        "svc 0x0000003c\n"
        "bx lr");
}
