#include <ctr/os.h>

extern void *g_tls_00815DE0;

void func_0010655C(void)
{
    void *tls;
    __asm__ volatile("mrc p15, 0, %0, c13, c0, 3" : "=r"(tls));
    *((void **)((char *)&g_tls_00815DE0 + 4)) = tls;
}
