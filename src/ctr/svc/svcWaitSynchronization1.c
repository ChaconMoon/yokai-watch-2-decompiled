#include <ctr/svc.h>

Result svcWaitSynchronization1(Handle handle, s64 nanoseconds)
{
        __asm__ volatile("svc 0x00000024");
}
