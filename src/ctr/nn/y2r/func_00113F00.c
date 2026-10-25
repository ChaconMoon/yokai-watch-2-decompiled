#include <ctr/y2r.h>

extern void func_0011F46C(void);
extern void func_0011FA98(void);
extern void func_0011FA7C(void);

/**
 * @brief func_00113F00
 * @address 0x00113F00
 * Y2R initialization sequence invoking func_0011F46C, func_0011FA98, func_0011FA7C
 *
 * @return Returns 1 on successful initialization
 */
s32 func_00113F00(void)
{
        func_0011F46C();
        func_0011FA98();
        func_0011FA7C();
        return 1;
}
