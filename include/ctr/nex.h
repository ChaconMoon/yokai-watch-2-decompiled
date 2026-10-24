#ifndef CTR_NEX_H
#define CTR_NEX_H

#include "types.h"

#ifdef __cplusplus

namespace nn
{

        namespace nex
        {
                class StationConnectionInfo;

                class NexElement
                {
                        friend class StationConnectionInfo;

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

                struct ResultData
                {
                        u32 unk_01;
                        u32 unk_02;
                };

                class qResult
                {
                public:
                        // Function 0031F1E8 (Operator asignament for getter of qResult)
                        qResult &operator=(const qResult &other);

                        // Function 0031F1F4 (default constructor of qResult)
                        qResult();

                        // Function 0031F204 (Constructor with copy of qResult)
                        qResult(const qResult &other);

                        // Function 0031f210 (Getter / Conversion?)
                        u64 getValue() const;

                private:
                        ResultData m_data;
                };

                class StationConnectionInfo
                {
                public:
                        // Function 00340ECC (Resest connection and sets all values at zero)
                        void reset();

                        // Function 00340EAC
                        u32 setPort(u16 port);

                        // Function 00340EB8
                        u32 setElement(const NexElement &element);

                        // Function 00340E5C

                        // Function 00340EE8
                private:
                        s32 unk_00;
                        NexElement m_element;
                        u16 m_port;
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
