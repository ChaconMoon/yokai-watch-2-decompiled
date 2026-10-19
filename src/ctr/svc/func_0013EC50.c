#include <ctr/svc.h>
__attribute__((naked)) void func_0013EC50(void)
{
        __asm__ volatile(
            "mov r0, #0\n"
            "mov r1, r0\n"
            "mov r0, r0\n"
            "svc 0x0000000a\n"
            "bx lr");
}
