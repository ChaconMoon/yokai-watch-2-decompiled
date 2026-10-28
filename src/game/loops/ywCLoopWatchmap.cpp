#include <game/loops.h>

extern "C" const char s_ywCLoopWatchmap[];

/**
 * @brief ywCLoopWatchmap::getClassType
 * @address 0x0010DD40
 * Yo-kai Radar & Town Map class descriptor type getter (returns 0).
 */
s32 ywCLoopWatchmap::getClassType()
{
	return 0;
}

/**
 * @brief ywCLoopWatchmap::getClassName
 * @address 0x0010DD48
 * Returns the class identifier string "ywCLoopWatchmap" (0x00860556).
 */
const char *ywCLoopWatchmap::getClassName()
{
	return s_ywCLoopWatchmap;
}
