#include <game/loops.h>

extern "C" const char s_ywCLoopRace[];

/**
 * @brief ywCLoopRace::getClassType
 * @address 0x0010D234
 * Bicycle Racing Minigame Loop class descriptor type getter (returns 0).
 */
s32 ywCLoopRace::getClassType()
{
	return 0;
}

/**
 * @brief ywCLoopRace::getClassName
 * @address 0x0010D23C
 * Returns the class identifier string "ywCLoopRace" (0x008604AF).
 */
const char *ywCLoopRace::getClassName()
{
	return s_ywCLoopRace;
}
