#include <game/loops.h>

/**
 * @brief func_0010C880
 * @address 0x0010C880
 * Game loop controller state activation setter (0x00815C90 offset +0x00)
 */
void func_0010C880(void)
{
    g_LoopState_00815C90.enabled = 1;
}
