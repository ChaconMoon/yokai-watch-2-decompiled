#include <ctr/svc.h>

__attribute__((naked))
Result
func_00113008(Handle *thread, ThreadFunc entrypoint, u32 arg, u32 *stackTop, s32 priority, s32 processorId)
{
    __asm__ volatile(
        "push {r0, r4}\n"
        "ldr r0, [sp, #8]\n"
        "ldr r4, [sp, #12]\n"
        "svc 0x00000008\n"
        "ldr r2, [sp]\n"
        "str r1, [r2]\n"
        "add sp, sp, #4\n"
        "pop {r4}\n"
        "bx lr");
}
