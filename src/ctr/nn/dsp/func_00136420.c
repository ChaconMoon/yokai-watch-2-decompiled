#include <ctr/dsp.h>

/**
 * @brief func_00136420
 * @address 0x00136420
 * nn::dsp virtual method dispatch (tail-call)
 *
 * Invokes the virtual method at vtable index 12 (offset 48 / 0x30) if obj is non-NULL.
 *
 * @param obj Pointer to DspInterface_00136420 object.
 */
void func_00136420(DspInterface_00136420 *obj)
{
        if (obj == NULL)
        {
                return;
        }
        obj->vtable[12](obj);
}
