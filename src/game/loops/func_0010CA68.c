#include <game/loops.h>

/**
 * @brief func_0010CA68
 * @address 0x0010CA68
 * Game loop controller state target context setter (0x00815C90 offset +0x04)
 */
void func_0010CA68(void *target)
{
    g_LoopState_00815C90.target = target;
}
