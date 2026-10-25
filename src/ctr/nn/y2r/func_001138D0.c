#include <ctr/y2r.h>

extern const char unk_0086A420[];
extern u32 func_0011F51C(void *arg0);
extern void func_00125BF0(void *arg0, const char *file, u32 line, u32 errCode);

/**
 * @brief func_001138D0
 * @address 0x001138D0
 * Y2R error reporting assertion thunk invoking func_0011F51C and tail calling func_00125BF0
 * (Source assertion at line 1078 of unk_0086A420)
 *
 * @param arg0 Device or driver context instance pointer
 */
void func_001138D0(void *arg0)
{
        u32 err = func_0011F51C(arg0);
        func_00125BF0(arg0, unk_0086A420, 1078, err);
}
