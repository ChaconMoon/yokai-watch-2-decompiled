#ifndef CTR_DSP_H
#define CTR_DSP_H

#include "types.h"

#ifdef __cplusplus
extern "C"
{
#endif

        /* ========================================================================
         * Nintendo CTR-SDK — Digital Signal Processor (nn::dsp)
         * ======================================================================== */

        extern s32 unk_0086A0A4;
        extern u32 unk_00815DFC;
        extern s8 unk_00815DAC;
        extern s8 unk_00815CA0;

        typedef struct DspHeader_00136318
        {
                u32 magic;  /* 0x00: Initialized to 0xE7E3FFFF */
                u32 status; /* 0x04: Initialized to 0 */
        } DspHeader_00136318;

        void func_00136154(void *arg);
        void func_00136318(DspHeader_00136318 *header); /* 0x00136318: initializes header */
        u32 func_00137054(void);                        /* 0x00137054: returns unk_00815DFC */
        s8 func_001389BC(void);                         /* 0x001389BC: returns unk_00815DAC */
        s8 func_00138A80(void);                         /* 0x00138A80: returns unk_00815CA0 */
        u32 func_00138A90(void);                        /* 0x00138A90: returns applet state field at 0x00814E00 (+0x10) */

#ifdef __cplusplus
}
#endif

#endif /* CTR_DSP_H */
