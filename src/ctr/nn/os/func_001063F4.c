#include <ctr/os.h>

/**
 * @brief func_001063F4
 * @address 0x001063F4
 * CTR OS SystemConfig block field reader (0x1FF80000 + 0x40)
 */
u32 func_001063F4(void)
{
    return *(volatile u32 *)0x1FF80040;
}
