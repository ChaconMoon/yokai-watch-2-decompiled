#include <ctr/applet.h>

/**
 * @brief func_00128628
 * @address 0x00128628
 * nn::applet::detail::SetState07_1
 * Sets the signed state byte at offset 0x07 of g_AppletState_00814E00 to 1.
 */
void func_00128628(void)
{
        g_AppletState_00814E00.unk_07 = 1;
}
