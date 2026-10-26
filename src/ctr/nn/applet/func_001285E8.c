#include <ctr/applet.h>

/**
 * @brief func_001285E8
 * @address 0x001285E8
 * nn::applet::detail::GetState0B
 * Reads and returns the 8-bit unsigned value at offset 0x0B (11 decimal) from g_AppletState_00814E00.
 *
 * @return u8 The state byte at offset 0x0B
 */
u8 func_001285E8(void)
{
        return g_AppletState_00814E00.unk_0B;
}
