#include <ctr/applet.h>
#include <ctr/dsp.h>

/**
 * @brief func_00138A90
 * @address 0x00138A90
 * nn::dsp global applet state field getter.
 * Reads and returns the 32-bit word at offset 0x10 from g_AppletState_00814E00.
 *
 * @return u32 Value stored at g_AppletState_00814E00.unk_10
 */
u32 func_00138A90(void)
{
        return g_AppletState_00814E00.unk_10;
}
