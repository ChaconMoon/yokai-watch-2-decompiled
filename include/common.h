#ifndef COMMON_H
#define COMMON_H

#include "types.h"

/* Convenience macros for ARM compiler alignment and packing attributes */
#if defined(__arm__) || defined(__CC_ARM)
    #define ALIGN(n) __attribute__((aligned(n)))
    #define PACKED   __attribute__((packed))
#else
    #define ALIGN(n)
    #define PACKED
#endif

#endif /* COMMON_H */
