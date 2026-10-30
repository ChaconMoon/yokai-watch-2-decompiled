#include <ctr/dsp.h>

/**
 * @brief func_00137F28
 * @address 0x00137F28
 * nn::dsp conditional pair setter
 *
 * Sets a pair of 32-bit values at offset +0x14 and +0x18 if param1 is non-NULL.
 *
 * @param obj Pointer to DspPair_00137F28 structure.
 * @param param1 First value / pointer to store at +0x14 (checked against NULL).
 * @param param2 Second value / pointer to store at +0x18.
 * @return bool32 TRUE (1) if param1 was non-NULL, FALSE (0) otherwise.
 */
bool32 func_00137F28(DspPair_00137F28 *obj, void *param1, void *param2)
{
        if (param1 == NULL)
        {
                return FALSE;
        }

        obj->field_14 = param1;
        obj->field_18 = param2;
        return TRUE;
}
