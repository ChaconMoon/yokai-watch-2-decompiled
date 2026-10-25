#include <ctr/y2r.h>

/**
 * @brief func_00112E60
 * @address 0x00112E60
 * Y2R struct offset 8648 u16 reader
 */
u16 func_00112E60(const Y2rObject *y2rObject)
{
        const Y2rSubContext *sub = &y2rObject->sub;
        __nop();
        return sub->flag;
}
