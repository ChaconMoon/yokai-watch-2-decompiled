#include <ctr/dsp.h>

/**
 * @brief func_00137F40
 * @address 0x00137F40
 * nn::dsp audio buffer size calculation
 *
 * Computes buffer memory offset/size based on block count and multiplier.
 * Formula: ((field_3C * field_55) * 640) + 32
 *
 * @param obj Pointer to DspBuffer_00137F40 structure.
 * @return u32 Calculated buffer size in bytes.
 */
u32 func_00137F40(DspBuffer_00137F40 *obj)
{
        u32 arg0 = obj->field_3C;
        u8 arg1 = obj->field_55;
        arg0 *= arg1;
        arg0 *= 5;
        arg0 <<= 7;
        return arg0 + 32;
}
