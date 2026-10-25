#include <ctr/y2r.h>

/**
 * @brief func_00112AA8
 * @address 0x00112AA8
 * Y2R channel state structure field zero-initialization
 *
 * @param dev Pointer to the Y2R device context holding channel state
 */
void func_00112AA8(Y2rDevice *dev)
{
        dev->state.field_524 = 0;
        dev->state.field_528 = 0;
        dev->state.field_530 = 0;
        dev->state.field_534 = 0;
        dev->state.field_538 = 0;
        dev->state.field_53C = 0;
        dev->state.field_540 = 0;
        dev->state.field_544 = 0;
        dev->state.field_548 = 0;
        dev->state.field_54C = 0;
        dev->state.field_550 = 0;
        dev->state.field_554 = 0;
        dev->state.field_558 = 0;
        dev->state.field_55C = 0;
        dev->state.field_560 = 0;
        dev->state.field_568 = 0;
        dev->state.field_56C = 0;
        dev->state.field_564 = 0;
        dev->state.flag_570 = 0;
        dev->state.flag_571 = 0;
        dev->state.flag_572 = 0;
        dev->state.flag_573 = 0;
}
