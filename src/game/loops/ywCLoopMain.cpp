#include <game/loops.h>

extern "C" const char s_ywCLoopMain[];

/**
 * @brief ywCLoopMain::getClassType
 * @address 0x0010CFF4
 * Primary Game State Machine class descriptor type getter (returns 0).
 */
s32 ywCLoopMain::getClassType()
{
	return 0;
}

/**
 * @brief ywCLoopMain::getClassName
 * @address 0x0010CFFC
 * Returns the class identifier string "ywCLoopMain" (0x00860497).
 */
const char *ywCLoopMain::getClassName()
{
	return s_ywCLoopMain;
}
