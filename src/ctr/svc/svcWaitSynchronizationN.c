#include <ctr/svc.h>
#include <stdbool.h>

/**
 * @brief nn::svc::WaitSynchronizationN (svcWaitSynchronizationN)
 * @address 0x0013EC64
 * CTR kernel syscall wrapper for svc 0x25.
 * Suspends execution until one or all specified synchronization handles are signaled.
 * @param outIndex Pointer receiving the index of the handle that satisfied the wait condition.
 * @param handles Array of kernel synchronization handles to wait on.
 * @param handleCount Number of handles in the array (max 64).
 * @param waitAll If true, waits until all handles are signaled; if false, any handle wakes the caller.
 * @param timeout Maximum wait duration in nanoseconds.
 * @return Kernel Result code.
 */
__attribute__((naked))
Result
svcWaitSynchronizationN(s32 *outIndex, const Handle *handles, s32 handleCount, bool waitAll, s64 timeout)
{
    __asm__ volatile(
        "push {r0, r4}\n"
        "ldr r0, [sp, #8]\n"
        "ldr r4, [sp, #12]\n"
        "svc 0x00000025\n"
        "ldr r2, [sp]\n"
        "str r1, [r2]\n"
        "add sp, sp, #4\n"
        "pop {r4}\n"
        "bx lr");
}
