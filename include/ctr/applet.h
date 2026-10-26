#ifndef CTR_APPLET_H
#define CTR_APPLET_H

#include "types.h"

typedef struct AppletState
{
        u8  pad_00[7];   /* 0x00 - 0x06 */
        s8  unk_07;      /* 0x07: Estado/flag con signo (func_00128628, func_0012863C, func_0012864C) */
        s8  unk_08;      /* 0x08: Estado/flag con signo (func_0012859C, func_001285B0, func_001285D4) */
        u8  pad_09[2];   /* 0x09 - 0x0A */
        u8  unk_0B;      /* 0x0B: Byte de estado (func_001285E8, func_001285F8) */
        u8  unk_0C;      /* 0x0C: Offset 12 decimal (func_00128568, func_00128578) */
        s8  unk_0D;      /* 0x0D: Offset 13 decimal con signo (func_00128608, func_00128618) */
        u8  pad_0E[2];   /* 0x0E - 0x0F: Relleno hasta 0x10 */
        u32 unk_10;      /* 0x10: Leído por func_00138A90, escrito por func_00128558 */
        u32 unk_14;      /* 0x14: Offset intermedio (func_0010C6A4) */
        u32 attribute;   /* 0x18: Atributo de tipo de título (func_001284E4, func_0010C598, func_0010C5C8) */
} AppletState;

extern AppletState g_AppletState_00814E00;

#ifdef __cplusplus
extern "C" {
#endif

void func_00128558(u32 val); /* 0x00128558: sets g_AppletState_00814E00.unk_10 (offset 0x10) */
u8   func_00128568(void);    /* 0x00128568: returns g_AppletState_00814E00.unk_0C (offset 0x0C) */
void func_00128578(u8 val);  /* 0x00128578: sets g_AppletState_00814E00.unk_0C (offset 0x0C) */
void func_0012859C(void);    /* 0x0012859C: sets g_AppletState_00814E00.unk_08 to 1 */
s8   func_001285B0(void);    /* 0x001285B0: returns g_AppletState_00814E00.unk_08 (offset 0x08) */
void func_001285D4(void);    /* 0x001285D4: sets g_AppletState_00814E00.unk_08 to 0 */
u8   func_001285E8(void);    /* 0x001285E8: returns g_AppletState_00814E00.unk_0B (offset 0x0B / 11 decimal) */
void func_001285F8(u8 val);  /* 0x001285F8: sets g_AppletState_00814E00.unk_0B (offset 0x0B / 11 decimal) */
s8   func_00128608(void);    /* 0x00128608: returns g_AppletState_00814E00.unk_0D (offset 0x0D / 13 decimal) */
void func_00128618(s8 val);  /* 0x00128618: sets g_AppletState_00814E00.unk_0D (offset 0x0D / 13 decimal) */
void func_00128628(void);    /* 0x00128628: sets g_AppletState_00814E00.unk_07 to 1 */
s8   func_0012863C(void);    /* 0x0012863C: returns g_AppletState_00814E00.unk_07 (offset 0x07) */
void func_0012864C(void);    /* 0x0012864C: sets g_AppletState_00814E00.unk_07 to 0 */

#ifdef __cplusplus
}
#endif

#endif /* CTR_APPLET_H */
