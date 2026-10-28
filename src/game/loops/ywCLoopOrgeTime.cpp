#include <game/loops.h>

extern "C" const char s_ywCLoopOrgeTime[];

/**
 * @brief ywCLoopOrgeTime::getClassType
 * @address 0x0010DC40
 * Terror Time / Oni Time Chase Loop class descriptor type getter (returns 0).
 */
s32 ywCLoopOrgeTime::getClassType()
{
	return 0;
}

/**
 * @brief ywCLoopOrgeTime::getClassName
 * @address 0x0010DC48
 * Returns the class identifier string "ywCLoopOrgeTime" (0x00860546).
 */
const char *ywCLoopOrgeTime::getClassName()
{
	return s_ywCLoopOrgeTime;
}
