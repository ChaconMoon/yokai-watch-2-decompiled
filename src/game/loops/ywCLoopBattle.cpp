#include <game/loops.h>

extern "C" const char s_ywCLoopBattle[];

/**
 * @brief ywCLoopBattle::getClassType
 * @address 0x0010D500
 * Battle System Engine class descriptor type getter (returns 0).
 */
s32 ywCLoopBattle::getClassType()
{
	return 0;
}

/**
 * @brief ywCLoopBattle::getClassName
 * @address 0x0010D508
 * Returns the class identifier string "ywCLoopBattle" (0x008604C8).
 */
const char *ywCLoopBattle::getClassName()
{
	return s_ywCLoopBattle;
}
