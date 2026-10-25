#include <ctr/svc.h>

/**
 * @brief nn::svc::BreakReason4 (func_0013EC38)
 * @address 0x0013EC38
 * CTR kernel syscall wrapper for svc 0x3C with panic reason code #4.
 * Halts execution and triggers the CTR system panic handler.
 * Preserves ARM instruction alignment with an explicit 'mov r0, r0'.
 * @param arg0 First debug/diagnostic argument.
 * @param arg1 Second debug/diagnostic argument.
 */
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
