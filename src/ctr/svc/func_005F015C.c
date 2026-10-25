#include <ctr/svc.h>

/**
 * @brief nn::svc::GetSystemTickToPtr (func_005F015C)
 * @address 0x005F015C
 * Invokes CTR kernel syscall svc 0x28 (GetSystemTick) to retrieve the 64-bit hardware
 * timer tick and stores the 64-bit value into the supplied pointer via strd.
 * @param outTick Pointer to an s64 variable that receives the system tick.
 * @return Returns the destination pointer outTick.
 */
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
