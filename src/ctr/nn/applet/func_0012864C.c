#include <ctr/applet.h>

/**
 * @brief func_0012864C
 * @address 0x0012864C
 * nn::applet::detail::SetState07_0
 * Resets the signed state byte at offset 0x07 of g_AppletState_00814E00 to 0.
 */
void func_0012864C(void)
{
        g_AppletState_00814E00.unk_07 = 0;
}
