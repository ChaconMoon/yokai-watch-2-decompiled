#include <ctr/svc.h>

/**
 * @brief nn::svc::CreateThread (func_00113008)
 * @address 0x00113008
 * CTR kernel syscall wrapper for svc 0x08.
 * Spawns a new execution thread within the calling process.
 * @param thread Pointer receiving the created thread kernel Handle.
 * @param entrypoint Thread entrypoint function pointer.
 * @param arg User argument passed to the thread entrypoint.
 * @param stackTop Pointer to the top of the allocated thread stack memory.
 * @param priority Thread scheduling priority (0x18 - 0x3F).
 * @param processorId Target CPU core ID (0 = Core0 / AppCore, 1 = Core1 / SysCore, -1 = default).
 * @return Kernel Result code.
 */
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
