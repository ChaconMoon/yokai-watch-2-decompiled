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

#ifdef __cplusplus
}
#endif

#endif /* ENGINE_LFW_H */

