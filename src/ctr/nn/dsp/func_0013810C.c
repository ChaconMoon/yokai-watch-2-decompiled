#include <ctr/dsp.h>

/**
 * @brief func_0013810C
 * @address 0x0013810C
 * nn::dsp conditional pair setter
 *
 * Sets the second pair of 32-bit values at offset +0x28 and +0x2C if param1 is non-NULL.
 *
 * @param obj Pointer to DspPair_00137F28 structure.
 * @param param1 First value / pointer to store at +0x28 (checked against NULL).
 * @param param2 Second value / pointer to store at +0x2C.
 * @return bool32 TRUE (1) if param1 was non-NULL, FALSE (0) otherwise.
 */
bool32 func_0013810C(DspPair_00137F28 *obj, void *param1, void *param2)
{
        if (param1 == NULL)
        {
                return FALSE;
        }

        obj->field_28 = param1;
        obj->field_2C = param2;
        return TRUE;
}
