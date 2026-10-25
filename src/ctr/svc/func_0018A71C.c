#include <ctr/svc.h>

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
