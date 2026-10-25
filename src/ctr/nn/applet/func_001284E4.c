#include <types.h>
#include <stdbool.h>

typedef struct AppletState {
    u8 pad[0x18];
    u32 attribute;
} AppletState;

extern AppletState g_AppletState_00814E00;

bool func_001284E4(void)
{
    return (g_AppletState_00814E00.attribute & 7) == 0;
}
