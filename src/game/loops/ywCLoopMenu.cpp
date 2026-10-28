#include <game/loops.h>

extern "C" const char s_ywCLoopMenu[];

/**
 * @brief ywCLoopMenu::getClassType
 * @address 0x0010D134
 * UI & Inventory Loop class descriptor type getter (returns 0).
 */
s32 ywCLoopMenu::getClassType()
{
	return 0;
}

/**
 * @brief ywCLoopMenu::getClassName
 * @address 0x0010D13C
 * Returns the class identifier string "ywCLoopMenu" (0x008604A3).
 */
const char *ywCLoopMenu::getClassName()
{
	return s_ywCLoopMenu;
}
