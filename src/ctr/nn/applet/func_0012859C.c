#include <ctr/applet.h>

/**
 * @brief func_0012859C
 * @address 0x0012859C
 * nn::applet::detail::SetState08_1
 * Sets the signed state byte at offset 0x08 of g_AppletState_00814E00 to 1.
 */
void func_0012859C(void)
{
        g_AppletState_00814E00.unk_08 = 1;
}
