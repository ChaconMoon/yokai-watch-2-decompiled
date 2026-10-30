#include <ctr/dsp.h>

/**
 * @brief func_00137930
 * @address 0x00137930
 * nn::dsp channel sub-descriptor bit 0 flag exchange
 * Reads previous bit 0 value of flags_12 and updates bit 0 with new flag value.
 */
u16 func_00137930(DspChannel_00137920 *channel, u16 flag)
{
    DspSubChannel *sub = &channel->sub;
    u16 flags = sub->flags_12;
    u16 old = flags & 1;
    sub->flags_12 = (flags & ~1) | (flag & 1);
    return old;
}
