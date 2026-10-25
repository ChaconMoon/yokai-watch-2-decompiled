#include <ctr/svc.h>

/**
 * @brief nn::svc::GetHandleInfo (svcGetHandleInfo)
 * @address 0x0018A768
 * CTR kernel syscall wrapper for svc 0x29.
 * Queries diagnostic information and properties about a kernel handle.
 * @param out Pointer receiving the 64-bit handle information.
 * @param handle Target kernel handle.
 * @param type Information query sub-type.
 * @return Kernel Result code.
 */
__attribute__((naked))
Result
svcGetHandleInfo(s64 *out, Handle handle, u32 type)
{
    __asm__ volatile(
        "push {r0}\n"
        "svc 0x00000029\n"
        "ldr r3, [sp]\n"
        "str r1, [r3]\n"
        "str r2, [r3, #4]\n"
        "add sp, sp, #4\n"
        "bx lr");
}
