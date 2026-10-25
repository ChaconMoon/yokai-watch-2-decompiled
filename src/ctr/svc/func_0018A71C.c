#include <ctr/svc.h>

/**
 * @brief nn::svc::CreateMemoryBlock (func_0018A71C)
 * @address 0x0018A71C
 * CTR kernel syscall wrapper for svc 0x1E.
 * Creates a shared memory block object that can be mapped into multiple processes.
 * @param memoryBlock Pointer receiving the created memory block Handle.
 * @param addr Base virtual address for the memory block.
 * @param size Size of the memory block in bytes.
 * @param myPermission Permissions granted to the creating process.
 * @param otherPermission Permissions granted to other processes mapping the block.
 * @return Kernel Result code.
 */
__attribute__((naked))
Result
func_0018A71C(Handle *memoryBlock, u32 addr, u32 size, u32 myPermission, u32 otherPermission)
{
    __asm__ volatile(
        "push {r0}\n"
        "ldr r0, [sp, #4]\n"
        "svc 0x0000001e\n"
        "ldr r2, [sp]\n"
        "str r1, [r2]\n"
        "add sp, sp, #4\n"
        "bx lr");
}
