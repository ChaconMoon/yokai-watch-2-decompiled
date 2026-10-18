#include "types.h"

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

/* 0x001280A8: Bounds-checked array element getter (stride 8, base offset +0x0C) */
NdmElement8 *func_001280A8(NdmContainer *ctx, u32 index) {
    if (ctx->count <= index) {
        return NULL;
    }
    return &ctx->items[index];
}

