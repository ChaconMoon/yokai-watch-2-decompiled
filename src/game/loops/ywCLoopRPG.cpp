#include <game/loops.h>

extern "C" const char s_ywCLoopRPG[];

/**
 * @brief ywCLoopRPG::getClassType
 * @address 0x0010CEE8
 * Returns constant 0 as loop class type.
 */
s32 ywCLoopRPG::getClassType()
{
        return 0;
}

/**
 * @brief ywCLoopRPG::getClassName
 * @address 0x0010CEF0
 * Returns the class identifier string "ywCLoopRPG" (0x0086048C).
 */
const char *ywCLoopRPG::getClassName()
{
        return s_ywCLoopRPG;
}

