
#include <ctr/ndm.h>

/* 0x001280A8: Bounds-checked array element getter (stride 8, base offset +0x0C) */
/**
 * @brief func_001280A8
 * @address 0x001280A8
 * nn::ndm bounds-checked struct array element indexer (stride 8, offset +0x0C)
 */
NdmElement8 *func_001280A8(NdmContainer *ctx, u32 index)
{
        if (ctx->count <= index)
        {
                return NULL;
        }
        return &ctx->items[index];
}
