#include <ctr/dsp.h>

/**
 * @brief func_00137F18
 * @address 0x00137F18
 * nn::dsp wrapper invoking func_00147C74 with global unk_0088A85C
 *
 * @param param Pointer passed as second argument to func_00147C74.
 */
void func_00137F18(void *param)
{
        func_00147C74(&unk_0088A85C, param);
}
