#include <ctr/svc.h>

/**
 * @brief svcCreateMemoryBlock
 * @address 0x0018A738
 * CTR kernel syscall wrapper stub (svc 0x13)
 */
__attribute__((naked))
Result
svcCreateMemoryBlock(Handle *memblock, u32 addr, u32 size, u32 myPerm, u32 otherPerm)
{
        __asm__ volatile(
            "push {r0}\n"
            "svc 0x00000013\n"
            "ldr r2, [sp]\n"
            "str r1, [r2]\n"
            "add sp, sp, #4\n"
            "bx lr");
}
