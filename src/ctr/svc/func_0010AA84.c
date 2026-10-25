#include <ctr/svc.h>

/**
 * @brief nn::svc::ControlMemory (func_0010AA84)
 * @address 0x0010AA84
 * CTR kernel syscall wrapper for svc 0x01.
 * Controls application virtual memory allocation, mapping, and page permissions.
 * @param outAddr Pointer receiving the allocated/modified virtual address.
 * @param addr0 Primary target address.
 * @param addr1 Secondary target address (for aliasing or mirroring).
 * @param size Size of the memory region in bytes (aligned to page size 0x1000).
 * @param op Memory operation flags (commit, free, reserve).
 * @param perm Memory permission flags (read, write, execute).
 * @return Kernel Result code.
 */
__attribute__((naked))
Result
func_0010AA84(u32 *outAddr, u32 addr0, u32 addr1, u32 size, u32 op, u32 perm)
{
    __asm__ volatile(
        "push {r0, r4}\n"
        "ldr r0, [sp, #8]\n"
        "ldr r4, [sp, #12]\n"
        "svc 0x00000001\n"
        "ldr r2, [sp]\n"
        "str r1, [r2]\n"
        "add sp, sp, #4\n"
        "pop {r4}\n"
        "bx lr");
}
