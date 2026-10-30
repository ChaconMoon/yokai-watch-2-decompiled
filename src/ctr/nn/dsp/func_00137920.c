#include <ctr/dsp.h>

/**
 * @brief func_00137920
 * @address 0x00137920
 * nn::dsp channel sub-descriptor 16-bit field exchange
 * Reads previous field_10 value and stores new 16-bit value into sub-descriptor.
 */
u16 func_00137920(DspChannel_00137920 *channel, u16 val)
{
    DspSubChannel *sub = &channel->sub;
    u16 old = sub->field_10;
    sub->field_10 = val;
    return old;
}
