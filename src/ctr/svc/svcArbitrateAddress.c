#include <ctr/svc.h>

/**
 * @brief nn::svc::ArbitrateAddress (svcArbitrateAddress)
 * @address 0x00166948
 * CTR kernel syscall wrapper for svc 0x22.
 * Synchronizes threads using an address arbiter object for fast user-space mutexes
 * and condition variables.
 * @param arbiter Handle to the address arbiter.
 * @param addr Virtual address to arbitrate on.
 * @param type Arbitration operation type (signal, wait, etc.).
 * @param value Comparison value for conditional wait.
 * @param timeout Timeout in nanoseconds (<= 0 for no timeout).
 * @return Kernel Result code.
 */
__attribute__((naked))
Result
svcArbitrateAddress(Handle arbiter, u32 addr, u32 type, s32 value, s64 timeout)
{
    __asm__ volatile(
        "push {r4, r5}\n"
        "ldr r4, [sp, #8]\n"
        "ldr r5, [sp, #12]\n"
        "svc 0x00000022\n"
        "pop {r4, r5}\n"
        "bx lr");
}
