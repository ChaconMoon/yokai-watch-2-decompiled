#include <ctr/svc.h>
/**
 * @brief func_0013EC50
 * @address 0x0013EC50
 * Thread yield stub via svc 0x0A (svcSleepThread(0))
 */
__attribute__((naked)) void func_0013EC50(void)
{
        __asm__ volatile(
            "mov r0, #0\n"
            "mov r1, r0\n"
            "mov r0, r0\n"
            "svc 0x0000000a\n"
            "bx lr");
}
