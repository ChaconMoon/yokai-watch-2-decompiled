#ifndef ENGINE_LFW_H
#define ENGINE_LFW_H

#include "types.h"

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================
 * Level-5 Framework (lfw) — Loop Class Descriptor Table
 * Located at 0x00107478 in .text (12 bytes per loop class descriptor)
 * ======================================================================== */
typedef struct LfwLoopClassInfo {
    void *(*createInstance)(void);
    s32   (*getClassType)(void);
    const char *(*getClassName)(void);
} LfwLoopClassInfo;

/* lfwCLoopEmpty (Descriptor at 0x00107484) */
s32         func_0010B6D0(void);            /* 0x0010B6D0: returns 0 */
const char *func_0010B6D8(void);            /* 0x0010B6D8: returns "lfwCLoopEmpty" (0x008602F8) */

/* Global pointer storage & accessors */
extern void *unk_00815DA8;
void        func_0010BBB8(void *ptr);       /* 0x0010BBB8: sets unk_00815DA8 = ptr */
u32         func_0010C598(void);            /* 0x0010C598: returns applet attribute at 0x00814E00 (+0x18) */
void        func_0010C5C8(u32 attr);        /* 0x0010C5C8: sets applet attribute at 0x00814E00 (+0x18) */
void        func_0010C6A4(u32 val);         /* 0x0010C6A4: sets applet unk_14 at 0x00814E00 (+0x14) */

#ifdef __cplusplus
}
#endif

#endif /* ENGINE_LFW_H */

