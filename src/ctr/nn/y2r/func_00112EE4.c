#include <ctr/y2r.h>

extern void func_002FDAC4(u32 arg0, void *outPtr);

/**
 * @brief func_00112EE4
 * @address 0x00112EE4
 * Y2R stack buffer query invoking func_002FDAC4
 *
 * @param arg0 Configuration or query parameter passed in r0
 */
void func_00112EE4(u32 arg0)
{
        u32 stackVar;
        func_002FDAC4(arg0, &stackVar);
}

