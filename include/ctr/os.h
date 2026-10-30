#ifndef CTR_OS_H
#define CTR_OS_H

#include "types.h"

#ifdef __cplusplus
extern "C"
{
#endif

/* CTR-SDK Configuration Memory Page (0x1FF80000) */
#define CTR_CONFIG_PAGE_VMA 0x1FF80000u

        extern char __text_start[];
        extern u8 unk_00828EEC;
        extern u32 unk_0086FC60;
        extern u32 unk_0086FC48;
        extern u8 g_flag_00814E54;

        /* nn::os initialization & configuration helpers */
        void func_00104D18(u8 flag); /* 0x00104D18 */
        u32 func_001063F4(void);     /* 0x001063F4 (reads 0x1FF80040) */
        void func_00106504(void);    /* 0x00106504 (app heap init 32 MB) */
        void func_00106518(void);    /* 0x00106518 */
        void func_00112EF4(void *addr, u32 base, u32 size);
        s8 func_0010678C(void);         /* 0x0010678C */
        void func_001274A0(vu32 *lock); /* 0x001274A0 (ldrex/strex spinlock) */
        u32 func_00127520(void);        /* 0x00127520 */
        void *func_001275D8(void);      /* 0x001275D8 (.text base address getter) */
        void func_0012788C(u8 val);     /* 0x0012788C (global flag setter) */

#ifdef __cplusplus
}
#endif

#endif /* CTR_OS_H */
