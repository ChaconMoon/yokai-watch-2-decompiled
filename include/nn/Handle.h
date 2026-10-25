#pragma once

#include "nn/Types.h"

#ifdef __cplusplus

namespace nn {

struct Handle {
    u32 m_Handle;
    Handle()
        : m_Handle(0)
    {
    }
    Handle(u32 h)
        : m_Handle(h)
    {
    }
    operator u32() const { return m_Handle; }
};

} // namespace nn

#else

typedef struct nn_Handle {
    u32 m_Handle;
} nn_Handle;

typedef u32 Handle;

#endif
