#include <game/loops.h>

/**
 * @brief func_0010C8A0
 * @address 0x0010C8A0
 * Game loop controller state mode setter (0x00815C90 offset +0x01)
 */
void func_0010C8A0(u8 mode)
{
    g_LoopState_00815C90.mode = mode;
}
