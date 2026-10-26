#include <engine/lfw.h>
#include <ctr/applet.h>

/**
 * @brief func_0010C5C8
 * @address 0x0010C5C8
 * Level-5 Framework applet attribute setter.
 * Stores the given 32-bit attribute value into g_AppletState_00814E00.attribute (offset 0x18).
 *
 * @param[in] attribute The new applet attribute bitfield value
 */
void func_0010C5C8(u32 attribute)
{
        g_AppletState_00814E00.attribute = attribute;
}
