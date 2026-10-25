#include <ctr/y2r.h>

extern "C" {
        extern void *unk_00814F28[2];
        s32 func_00113700(void);
}

/**
 * @brief func_00113700
 * @address 0x00113700
 * Y2R buffer deallocation sequence on unk_00814F28
 *
 * @return Returns 1 on successful deallocation of both buffers
 */
s32 func_00113700(void)
{
        if (unk_00814F28[1] != 0) {
                delete (char *)unk_00814F28[1];
                unk_00814F28[1] = 0;
        }
        if (unk_00814F28[0] != 0) {
                delete (char *)unk_00814F28[0];
                unk_00814F28[0] = 0;
        }
        return 1;
}
