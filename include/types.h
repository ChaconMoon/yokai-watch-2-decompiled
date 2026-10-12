#ifndef TYPES_H
#define TYPES_H

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================
 * Fixed-width integer types (Nintendo 3DS / ARM 32-bit little-endian)
 * ======================================================================== */

typedef unsigned char       u8;
typedef unsigned short      u16;
typedef unsigned int        u32;
typedef unsigned long long  u64;

typedef signed char         s8;
typedef signed short        s16;
typedef signed int          s32;
typedef signed long long    s64;

typedef volatile u8         vu8;
typedef volatile u16        vu16;
typedef volatile u32        vu32;
typedef volatile u64        vu64;

typedef volatile s8         vs8;
typedef volatile s16        vs16;
typedef volatile s32        vs32;
typedef volatile s64        vs64;

/* ========================================================================
 * Floating-point types
 * ======================================================================== */

typedef float               f32;
typedef double              f64;

/* ========================================================================
 * Boolean and pointer types
 * ======================================================================== */

typedef s32                 bool32;
typedef u32                 uintptr_t;
typedef s32                 intptr_t;

#ifndef NULL
#ifdef __cplusplus
#define NULL 0
#else
#define NULL ((void *)0)
#endif
#endif

#ifndef TRUE
#define TRUE 1
#endif

#ifndef FALSE
#define FALSE 0
#endif

/* ========================================================================
 * Compile-time static assertions to validate type widths
 * ======================================================================== */

#define STATIC_ASSERT(cond) typedef char __static_assert_##__LINE__[(cond) ? 1 : -1]

#ifdef __cplusplus
}
#endif

#endif /* TYPES_H */
