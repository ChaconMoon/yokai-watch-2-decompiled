#include <engine/lfw.h>
#include <ctr/applet.h>

/**
 * @brief func_0010C6A4
 * @address 0x0010C6A4
 * Level-5 Framework applet unk_14 setter.
 * Stores the given 32-bit value into g_AppletState_00814E00.unk_14 (offset 0x14).
 *
 * @param[in] val The new 32-bit value to store
 */
void func_0010C6A4(u32 val)
{
    g_AppletState_00814E00.unk_14 = val;
}

