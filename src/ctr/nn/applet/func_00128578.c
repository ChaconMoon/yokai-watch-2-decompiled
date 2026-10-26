#include <ctr/applet.h>

/**
 * @brief func_00128578
 * @address 0x00128578
 * nn::applet::detail::SetState0C
 * Stores the given 8-bit unsigned value into g_AppletState_00814E00.unk_0C (offset 0x0C / 12 decimal).
 *
 * @param[in] arg0 The new state byte to store
 */
void func_00128578(u8 val)
{
        g_AppletState_00814E00.unk_0C = val;
}
