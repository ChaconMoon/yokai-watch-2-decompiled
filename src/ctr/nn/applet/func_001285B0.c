#include <ctr/applet.h>

/**
 * @brief func_001285B0
 * @address 0x001285B0
 * nn::applet::detail::GetState08
 * Returns the signed 8-bit state value from g_AppletState_00814E00.unk_08 (offset 0x08).
 *
 * @return s8 The signed state byte at offset 0x08
 */
s8 func_001285B0(void)
{
        return g_AppletState_00814E00.unk_08;
}
