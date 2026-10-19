#include <ctr/y2r.h>

__attribute__((naked)) u16 func_00112E60(const void *ptr)
{
    __asm__ volatile(
        "add r0, r0, #8576\n"
        "mov r0, r0\n"
        "ldrh r0, [r0, #72]\n"
        "bx lr\n");
}