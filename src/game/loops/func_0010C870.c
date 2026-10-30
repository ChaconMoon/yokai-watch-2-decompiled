#include <game/loops.h>

/**
 * @brief func_0010C870
 * @address 0x0010C870
 * Game loop controller state callback setter (0x00815C90 offset +0x08)
 */
void func_0010C870(void *callback)
{
    g_LoopState_00815C90.callback = callback;
}
