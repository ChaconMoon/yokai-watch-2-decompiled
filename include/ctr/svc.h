#ifndef CTR_SVC_H
#define CTR_SVC_H

#include "types.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef u32 Handle;
typedef s32 Result;

/* Nintendo 3DS Kernel Supervisor Calls (SVC) */
void svcExitProcess(void);                  /* 0x00104778 (svc 0x03) */
void svcSleepThread(s64 nanoseconds);       /* 0x00151FBC (svc 0x28) */

#ifdef __cplusplus
}
#endif

#endif /* CTR_SVC_H */

