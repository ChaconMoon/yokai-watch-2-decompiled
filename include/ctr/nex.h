#ifndef CTR_NEX_H
#define CTR_NEX_H

#include "types.h"

#ifdef __cplusplus
extern "C"
{
#endif

        typedef struct NexElement
        {
                s32 unk_01;
                s16 unk_02;
        } NexElement;

        /* nn::nex leaf functions */
        void func_00301248(void);
        void func_00340CFC(NexElement *nexElement, s32 arg1, s16 arg2);
        void func_00340D08(NexElement *nexElement);

#ifdef __cplusplus
}
#endif

#endif /* CTR_NEX_H */