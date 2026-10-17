#ifndef CTR_OS_H
#define CTR_OS_H

#include "types.h"

#ifdef __cplusplus
extern "C" {
#endif

/* CTR-SDK Configuration Memory Page (0x1FF80000) */
#define CTR_CONFIG_PAGE_VMA 0x1FF80000u

/* nn::os initialization & configuration helpers */
void func_00104D18(u8 flag);                /* 0x00104D18 */
u32  func_001063F4(void);                   /* 0x001063F4 (reads 0x1FF80040) */
s8   func_0010678C(void);                   /* 0x0010678C */
void func_001274A0(vu32 *lock);             /* 0x001274A0 (ldrex/strex spinlock) */
u32  func_00127520(void);                   /* 0x00127520 */

#ifdef __cplusplus
}
#endif

#endif /* CTR_OS_H */

