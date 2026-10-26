#include <ctr/applet.h>

/**
 * @brief func_00128558
 * @address 0x00128558
 * nn::applet::detail::SetState10
 * Stores the given 32-bit value into g_AppletState_00814E00.unk_10 (offset 0x10).
 *
 * @param[in] val The new 32-bit state value
 */
void func_00128558(u32 val)
{
        g_AppletState_00814E00.unk_10 = val;
}
