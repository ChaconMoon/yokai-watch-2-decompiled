#ifndef CTR_NEX_H
#define CTR_NEX_H

#include "types.h"

#ifdef __cplusplus

namespace nn
{

        namespace nex
        {
                class NexElement
                {
                public:
                        /* nn::nex leaf functions */

                        // Function 00340CE8 (Operator asignament for getter of NexElement)
                        NexElement &operator=(const NexElement &other);

                        // Function 00340CFC (Constructor with params of NexElement)
                        NexElement(s32 arg1, s16 arg2);

                        // Function 00340D08 (Constructor of NexElement)
                        NexElement();

                        // Function 00340D18 (Destructor of NexElement)
                        ~NexElement();

                        // Function 00340D1C (Constructor with copy of NexElement)
                        NexElement(const NexElement &other);

                private:
                        s32 unk_01;
                        s16 unk_02;
                };
        }
}
extern "C"
{
#else
typedef struct NexElement
{
        s32 unk_01;
        s16 unk_02;
} NexElement;
#endif
        void func_00301248(void);
#ifdef __cplusplus
}
#endif

#endif /* CTR_NEX_H */