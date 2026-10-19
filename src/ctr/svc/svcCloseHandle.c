#include <ctr/svc.h>

Result svcCloseHandle(Handle handle)
{
    __asm__ volatile("svc 0x00000023");
}
