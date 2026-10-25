#include <ctr/svc.h>

/**
 * @brief svcCreateThread
 * @address 0x0018A750
 * CTR kernel syscall wrapper stub (svc 0x27)
 */
__attribute__((naked))
Result
svcCreateThread(Handle *thread, ThreadFunc entrypoint, u32 arg, u32 *stackTop, s32 priority, s32 processorId)
{
        __asm__ volatile(
            "push {r0}\n"
            "svc 0x00000027\n"
            "ldr r2, [sp]\n"
            "str r1, [r2]\n"
            "add sp, sp, #4\n"
            "bx lr");
}
