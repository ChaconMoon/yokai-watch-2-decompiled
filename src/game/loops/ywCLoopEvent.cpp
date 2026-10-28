#include <game/loops.h>

extern "C" const char s_ywCLoopEvent[];

/**
 * @brief ywCLoopEvent::getClassType
 * @address 0x0010D3A8
 * In-game Cutscenes & Scripted Events class descriptor type getter (returns 0).
 */
s32 ywCLoopEvent::getClassType()
{
	return 0;
}

/**
 * @brief ywCLoopEvent::getClassName
 * @address 0x0010D3B0
 * Returns the class identifier string "ywCLoopEvent" (0x008604BB).
 */
const char *ywCLoopEvent::getClassName()
{
	return s_ywCLoopEvent;
}
