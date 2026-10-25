#include <ctr/svc.h>

/**
 * @brief svcDuplicateHandle
 * @address 0x0010AAC0
 * CTR kernel syscall wrapper stub (svc 0x38)
 */
__attribute__((naked))
Result
svcDuplicateHandle(Handle *handle, Handle original)
{
        __asm__ volatile(
            "push {r0}\n"
            "svc 0x00000038\n"
            "ldr r2, [sp]\n"
            "str r1, [r2]\n"
            "add sp, sp, #4\n"
            "bx lr");
}
