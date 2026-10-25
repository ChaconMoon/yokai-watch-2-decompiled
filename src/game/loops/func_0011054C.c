#include <game/loops.h>

/**
 * @brief func_0011054C
 * @address 0x0011054C
 * Struct header reset (zeros 8 bytes, sets byte 0 to 0xFF)
 */
void func_0011054C(YwLoopHeader *ywLoopHeader)
{
        ywLoopHeader->unk_00 = 0;
        ywLoopHeader->value = 0;
        ywLoopHeader->status = 0xFF;
}
