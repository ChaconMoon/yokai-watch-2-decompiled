#include <ctr/applet.h>

/**
 * @brief func_00128568
 * @address 0x00128568
 * nn::applet::detail::GetState0C
 * Reads and returns the 8-bit unsigned value at offset 0x0C (12 decimal) from g_AppletState_00814E00.
 *
 * @return u8 The state byte at offset 0x0C
 */
u8 func_00128568(void)
{
        return g_AppletState_00814E00.unk_0C;
}
