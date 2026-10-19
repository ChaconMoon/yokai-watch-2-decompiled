#ifndef CTR_NDM_H
#define CTR_NDM_H

#include "types.h"

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================
 * Nintendo CTR-SDK — Network Daemon Manager (nn::ndm)
 * ======================================================================== */

extern s32 unk_00865F10;

void *func_00127EEC(void);

typedef struct NdmElement8 {
    u32 field_00;
    u32 field_04;
} NdmElement8;

typedef struct NdmContainer {
    u32         unk_00;
    u16         count;
    u16         unk_06;
    u32         unk_08;
    NdmElement8 items[1];
} NdmContainer;

NdmElement8 *func_001280A8(NdmContainer *ctx, u32 index);

#ifdef __cplusplus
}
#endif

#endif /* CTR_NDM_H */
