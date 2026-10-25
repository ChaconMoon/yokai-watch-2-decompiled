#include <ctr/y2r.h>

/**
 * @brief func_00113F58
 * @address 0x00113F58
 * Y2R global bit 3 flag getter via literal pool (0x008661EC)
 */
u32 func_00113F58(void)
{
    return (unk_008661EC.flag >> 3) & 1;
}
