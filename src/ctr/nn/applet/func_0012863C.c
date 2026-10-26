#include <ctr/applet.h>

/**
 * @brief func_0012863C
 * @address 0x0012863C
 * nn::applet::detail::GetState07
 * Returns the signed 8-bit state value from g_AppletState_00814E00.unk_07 (offset 0x07 / 7 decimal).
 *
 * @return s8 The signed state byte at offset 0x07
 */
s8 func_0012863C(void)
{
        return g_AppletState_00814E00.unk_07;
}
