#include <ctr/applet.h>

/**
 * @brief func_00128618
 * @address 0x00128618
 * nn::applet::detail::SetState0D
 * Stores the given signed 8-bit value into g_AppletState_00814E00.unk_0D (offset 0x0D / 13 decimal).
 *
 * @param[in] val The new state byte to store
 */
void func_00128618(s8 val)
{
        g_AppletState_00814E00.unk_0D = val;
}
