#ifndef CTR_SVC_H
#define CTR_SVC_H

#include "types.h"

#ifdef __cplusplus
extern "C"
{
#endif

        typedef u32 Handle;
        typedef s32 Result;

        /* Nintendo 3DS Kernel Supervisor Calls (SVC) */
        void svcExitProcess(void);                               /* 0x00104778 (svc 0x03) */
        Result svcCreateEvent(Handle *event, u32 resetType);     /* 0x0010AAA8 (svc 0x21) */
        Result svcGetThreadId(u32 *threadId, Handle thread);     /* 0x00151FC4 (svc 0x37) */
        Result svcDuplicateHandle(Handle *out, Handle original); /* 0x0010AAC0 (svc 0x38) */
        Result svcCreateAddressArbiter(Handle *arbiter);         /* 0x00151FA0 (svc 0x17) */
        void svcSleepThread(s64 nanoseconds);                    /* 0x00151FBC (svc 0x28) */

#ifdef __cplusplus
}
#endif

#endif /* CTR_SVC_H */
