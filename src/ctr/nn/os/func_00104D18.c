#include <ctr/os.h>

extern u8 g_flag_00814E54;

/**
 * @brief func_00104D18
 * @address 0x00104D18
 * nn::os startup global 8-bit flag setter (0x00814E54)
 */
void func_00104D18(u8 flag)
{
    g_flag_00814E54 = flag;
}
