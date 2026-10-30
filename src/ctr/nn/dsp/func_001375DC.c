#include <ctr/dsp.h>

/**
 * @brief func_001375DC
 * @address 0x001375DC
 * nn::dsp component cleanup & refcount decrement
 *
 * Invokes sub-cleanup func_0013769C on the component at offset +0x18 (24 bytes)
 * and decrements the counter / reference at offset +0x54 (84 bytes).
 *
 * @param obj Pointer to DspComponent_001375DC.
 */
void func_001375DC(DspComponent_001375DC *obj)
{
        func_0013769C(&obj->sub_18);
        obj->count_54 -= 1;
}
