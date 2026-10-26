#include <engine/lfw.h>

typedef struct AppletState {
    u8  pad[0x18];
    u32 attribute;
} AppletState;

extern AppletState g_AppletState_00814E00;

/**
 * @brief func_0010C598
 * @address 0x0010C598
 * Level-5 Framework applet attribute getter
 * Reads the 32-bit attribute field at offset 0x18 from the global applet state (0x00814E00).
 *
 * @return u32 The applet attribute bitfield
 */
u32 func_0010C598(void)
{
    return g_AppletState_00814E00.attribute;
}

