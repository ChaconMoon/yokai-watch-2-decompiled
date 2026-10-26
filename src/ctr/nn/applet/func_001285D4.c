#include <ctr/applet.h>

/**
 * @brief func_001285D4
 * @address 0x001285D4
 * nn::applet::detail::SetState08_0
 * Resets the signed state byte at offset 0x08 of g_AppletState_00814E00 to 0.
 */
void func_001285D4(void)
{
        g_AppletState_00814E00.unk_08 = 0;
}
