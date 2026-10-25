#include <ctr/y2r.h>

extern void func_0011FDAC(Y2rContext *ctx);

/**
 * @brief func_00113F4C
 * @address 0x00113F4C
 * Y2R tail-call thunk to func_0011FDAC with global unk_008661EC
 */
void func_00113F4C(void)
{
        func_0011FDAC(&unk_008661EC);
}

