#include <game/loops.h>

extern "C" const char s_ywCLoopCapsule[];

/**
 * @brief ywCLoopCapsule::getClassType
 * @address 0x0010D63C
 * Crank-a-kai / Gashapon Subsystem class descriptor type getter (returns 0).
 */
s32 ywCLoopCapsule::getClassType()
{
	return 0;
}

/**
 * @brief ywCLoopCapsule::getClassName
 * @address 0x0010D644
 * Returns the class identifier string "ywCLoopCapsule" (0x008604D9).
 */
const char *ywCLoopCapsule::getClassName()
{
	return s_ywCLoopCapsule;
}
