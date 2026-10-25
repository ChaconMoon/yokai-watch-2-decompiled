#include <ctr/os.h>

extern void *g_tls_00815DE0;

/**
 * @brief nn::os::detail::SetTlsStorage (func_0010655C)
 * @address 0x0010655C
 * Reads the ARM11 MPCore Thread-Local Storage (TLS) base address from system
 * coprocessor CP15 (c13, c0, 3 / TPIDRURO) and caches it into the global TLS
 * management structure at offset +0x04 (address 0x00815DE0 + 4).
 */
void func_0010655C(void)
{
    void *tls;
    __asm__ volatile("mrc p15, 0, %0, c13, c0, 3" : "=r"(tls));
    *((void **)((char *)&g_tls_00815DE0 + 4)) = tls;
}
