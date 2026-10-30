#include <ctr/dsp.h>

/**
 * @brief func_001385D0
 * @address 0x001385D0
 * nn::dsp status check and conditional call to func_001371D4.
 */
void func_001385D0(void)
{
        u32 res = func_001480C0() >> 31;
        if (res)
        {
                func_001371D4();
        }
}
