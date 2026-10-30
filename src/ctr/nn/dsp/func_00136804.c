#include <ctr/dsp.h>

/**
 * @brief func_00136804
 * @address 0x00136804
 * nn::dsp channel bit clearing in global mask unk_00828E90
 *
 * If channel index is valid (< 16) and bit is set, clears bit and returns obj.
 *
 * @param obj Pointer to DspChannel_00136804 (index at offset 0).
 * @return Pointer to DspChannel_00136804.
 */
DspChannel_00136804 *func_00136804(DspChannel_00136804 *obj)
{
        u32 index = obj->index;

        if (index < 16)
        {
                u16 *p;
                p = &unk_00828E90;
                if ((*p >> index) & 1)
                {
                        *p &= ~(1 << index);
                }
        }
        return obj;
}
