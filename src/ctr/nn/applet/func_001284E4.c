#include <types.h>
#include <stdbool.h>

typedef struct AppletState {
    u8 pad[0x18];
    u32 attribute;
} AppletState;

extern AppletState g_AppletState_00814E00;

/**
 * @brief nn::applet::CTR::IsApplication (func_001284E4)
 * @address 0x001284E4
 * Checks whether the currently running CTR title is a standard application.
 * Reads the attribute bitfield from the global applet state structure at offset 0x18
 * (address 0x00814E00) and masks with ATTRIBUTE_TYPE_MASK (0x7).
 * @return true if the title type is an application (attribute & 7 == 0), false otherwise.
 */
bool func_001284E4(void)
{
    return (g_AppletState_00814E00.attribute & 7) == 0;
}
