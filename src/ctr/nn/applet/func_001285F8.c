#include <ctr/applet.h>

/**
 * @brief func_001285F8
 * @address 0x001285F8
 * nn::applet::detail::SetState0B
 * Stores the given 8-bit unsigned value into g_AppletState_00814E00.unk_0B (offset 0x0B / 11 decimal).
 *
 * @param[in] arg0 The new state byte to store
 */
void func_001285F8(u8 val)
{
        g_AppletState_00814E00.unk_0B = val;
}
