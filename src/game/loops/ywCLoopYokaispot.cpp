#include <game/loops.h>

extern "C" const char s_ywCLoopYokaispot[];

/**
 * @brief ywCLoopYokaispot::getClassType
 * @address 0x0010E35C
 * Yo-kai Spot Environmental Puzzle class descriptor type getter (returns 0).
 */
s32 ywCLoopYokaispot::getClassType()
{
	return 0;
}

/**
 * @brief ywCLoopYokaispot::getClassName
 * @address 0x0010E364
 * Returns the class identifier string "ywCLoopYokaispot" (0x008605AA).
 */
const char *ywCLoopYokaispot::getClassName()
{
	return s_ywCLoopYokaispot;
}
