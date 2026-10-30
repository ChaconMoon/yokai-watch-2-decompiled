#include <ctr/dsp.h>

/**
 * @brief func_00137A0C
 * @address 0x00137A0C
 * nn::dsp channel sub-descriptor 8-bit signed state exchange
 * Reads previous field_14 value and stores new 8-bit signed value into sub-descriptor.
 */
s8 func_00137A0C(DspChannel_00137920 *channel, s8 state)
{
    DspSubChannel *sub = &channel->sub;
    s8 old = sub->field_14;
    sub->field_14 = state;
    return old;
}
