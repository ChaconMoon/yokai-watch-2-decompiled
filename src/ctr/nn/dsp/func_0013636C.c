#include <ctr/dsp.h>

/**
 * @brief func_0013636C
 * @address 0x0013636C
 * nn::dsp helper function
 *
 * Calls func_0012746C, stores the returned value into a local stack variable,
 * and passes the address of that local variable and arg0 to func_00146570.
 *
 * @param arg0 Pointer passed through to func_00146570.
 */
void func_0013636C(void *arg0)
{
        u32 temp = func_0012746C();
        func_00146570(&temp, arg0);
}
