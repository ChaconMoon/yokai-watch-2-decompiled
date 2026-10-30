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
        extern u32 unk_00815C78;
        extern s8 unk_00815DAC;
        extern s8 unk_00815CA0;
        extern u16 unk_00828E90;
        extern u32 unk_0088A85C;

        typedef struct DspHeader_00136318
        {
                u32 magic;  /* 0x00: Initialized to 0xE7E3FFFF */
                u32 status; /* 0x04: Initialized to 0 */
        } DspHeader_00136318;

        typedef struct DspSubChannel
        {
                u8  pad_00[0x10];   /* 0x00 - 0x0F */
                u16 field_10;       /* 0x10 (16): (0x24 + 0x10 = 0x34 / 52) */
                u16 flags_12;       /* 0x12 (18): (0x24 + 0x12 = 0x36 / 54) */
                s8  field_14;       /* 0x14 (20): (0x24 + 0x14 = 0x38 / 56) */
        } DspSubChannel;

        typedef struct DspChannel_00137920
        {
                u8            pad_00[0x24]; /* 0x00 - 0x23: 36 bytes */
                DspSubChannel sub;          /* 0x24: sub-channel component */
        } DspChannel_00137920;

        typedef struct DspPair_00137F28
        {
                u8   pad_00[0x14]; /* 0x00 - 0x13: 20 bytes */
                void *field_14;    /* 0x14 (20): first pair 1 */
                void *field_18;    /* 0x18 (24): first pair 2 */
                u8   pad_1C[0x0C]; /* 0x1C - 0x27: 12 bytes */
                void *field_28;    /* 0x28 (40): second pair 1 */
                void *field_2C;    /* 0x2C (44): second pair 2 */
        } DspPair_00137F28;

        typedef struct DspBuffer_00137F40
        {
                u8  pad_00[0x3C];  /* 0x00 - 0x3B: 60 bytes */
                u32 field_3C;      /* 0x3C (60): buffer block count */
                u8  pad_40[0x15];  /* 0x40 - 0x54: 21 bytes */
                u8  field_55;      /* 0x55 (85): block multiplier */
        } DspBuffer_00137F40;

        typedef struct DspChannel_00136804
        {
                u32 index; /* 0x00: channel index (0..15) */
        } DspChannel_00136804;

        typedef struct DspComponent_001375DC
        {
                u8  pad_00[0x18]; /* 0x00 - 0x17: 24 bytes */
                u8  sub_18[0x3C]; /* 0x18 - 0x53: sub-component passed to func_0013769C */
                s32 count_54;    /* 0x54 (84): reference / component counter */
        } DspComponent_001375DC;

        typedef struct DspInterface_00136420
        {
                void (**vtable)(void *self); /* 0x00: pointer to virtual function table */
        } DspInterface_00136420;

        u32  func_0012746C(void);
        void func_00136154(void *arg);
        void func_00136594(void *arg);
        void func_001365E4(void *arg);
        void func_001371D4(void);
        void func_0013769C(void *arg);
        void func_00146570(u32 *pTemp, void *arg0);
        void func_00147C74(void *obj, void *param);
        u32  func_001480C0(void);
        void func_0016A89C(void *arg);
        void func_00136318(DspHeader_00136318 *header); /* 0x00136318: initializes header */
        void func_0013636C(void *arg0);                 /* 0x0013636C: captures return from func_0012746C and passes to func_00146570 */
        void func_00136420(DspInterface_00136420 *obj); /* 0x00136420: virtual method dispatch at vtable[12] */
        DspChannel_00136804 *func_00136804(DspChannel_00136804 *obj); /* 0x00136804: clears channel bit in mask 0x00828E90 */
        void func_001375DC(DspComponent_001375DC *obj); /* 0x001375DC: decrements counter at +0x54 after sub-cleanup at +0x18 */
        u32 func_00137054(void);                        /* 0x00137054: returns unk_00815DFC */
        u16 func_00137920(DspChannel_00137920 *channel, u16 val); /* 0x00137920: exchange u16 field at +0x34 */
        u16 func_00137930(DspChannel_00137920 *channel, u16 flag); /* 0x00137930: exchange flag bit 0 at +0x36 */
        s8  func_00137A0C(DspChannel_00137920 *channel, s8 state); /* 0x00137A0C: exchange s8 field at +0x38 */
        void   func_00137F18(void *param);                                       /* 0x00137F18: wrapper calling func_00147C74(&unk_0088A85C, param) */
        bool32 func_00137F28(DspPair_00137F28 *obj, void *param1, void *param2); /* 0x00137F28: conditional pair setter (+0x14, +0x18) */
        u32    func_00137F40(DspBuffer_00137F40 *obj);                            /* 0x00137F40: buffer size computation */
        bool32 func_0013810C(DspPair_00137F28 *obj, void *param1, void *param2); /* 0x0013810C: conditional pair setter (+0x28, +0x2C) */
        void   func_001385D0(void);                                               /* 0x001385D0: status check and conditional call to func_001371D4 */
        bool32 func_001386D4(const char *str);                                    /* 0x001386D4: validates non-empty string */
        u32 func_001388CC(const char *str, u32 max_len);                         /* 0x001388CC: strnlen loop */
        s8 func_001389BC(void);                         /* 0x001389BC: returns unk_00815DAC */
        s8 func_00138A80(void);                         /* 0x00138A80: returns unk_00815CA0 */
        u32 func_00138A90(void);                        /* 0x00138A90: returns applet state field at 0x00814E00 (+0x10) */
        void func_00138AA0(void);                       /* 0x00138AA0: singleton wrapper -> func_001365E4(&unk_00815C78) */
        void func_00138AAC(void);                       /* 0x00138AAC: singleton wrapper -> func_0016A89C(&unk_00815C78) */
        void func_00138B58(void);                       /* 0x00138B58: singleton wrapper -> func_00136594(&unk_00815C78) */

#ifdef __cplusplus
}
#endif

#endif /* CTR_DSP_H */
