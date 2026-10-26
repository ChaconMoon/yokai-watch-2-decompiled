#include <ctr/applet.h>

/**
 * @brief func_00128608
 * @address 0x00128608
 * nn::applet::detail::GetState0D
 * Returns the signed 8-bit state value from g_AppletState_00814E00.unk_0D (offset 0x0D / 13 decimal).
 *
 * @return s8 The signed state byte at offset 0x0D
 */
s8 func_00128608(void)
{
        return g_AppletState_00814E00.unk_0D;
}
