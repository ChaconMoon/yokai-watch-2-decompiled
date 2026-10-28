#include <game/loops.h>

extern "C" const char s_ywCLoopQR[];

/**
 * @brief ywCLoopQR::getClassType
 * @address 0x0010FEBC
 * QR Code Scanner Subsystem class descriptor type getter (returns 0).
 */
s32 ywCLoopQR::getClassType()
{
	return 0;
}

/**
 * @brief ywCLoopQR::getClassName
 * @address 0x0010FEC4
 * Returns the class identifier string "ywCLoopQR" (0x00860794).
 */
const char *ywCLoopQR::getClassName()
{
	return s_ywCLoopQR;
}
