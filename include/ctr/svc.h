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
        void svcExitProcess(void);                                                                    /* 0x00104778 (svc 0x03) */
        Result svcCreateEvent(Handle *event, u32 resetType);                                          /* 0x0010AAA8 (svc 0x21) */
        Result svcGetThreadId(u32 *threadId, Handle thread);                                          /* 0x00151FC4 (svc 0x37) */
        Result svcDuplicateHandle(Handle *out, Handle original);                                      /* 0x0010AAC0 (svc 0x38) */
        Result svcCreateAddressArbiter(Handle *arbiter);                                              /* 0x00151FA0 (svc 0x17) */
        void svcSleepThread(s64 nanoseconds);                                                         /* 0x00151FBC (svc 0x28) */
        Result svcCreateMemoryBlock(Handle *memblock, u32 addr, u32 size, u32 myPerm, u32 otherPerm); /* 0x0018A738 (svc 0x13) */
        typedef void (*ThreadFunc)(u32 arg);
        Result svcCreateThread(Handle *thread, ThreadFunc entrypoint, u32 arg, u32 *stackTop, s32 priority, s32 processorId); /* 0x0018A750 (svc 0x27) */
        Result svcControlMemory(u32 *addrOut, u32 addr0, u32 addr1, u32 size, u32 op, u32 perm);                              /* 0x0018A784 (svc 0x0B) */
        Result svcCreateTimer(Handle *timer, u32 resetType);                                                                  /* 0x00112FF0 (svc 0x2D) */
        Result svcCreateResourceLimit(Handle *resourceLimit);
        void svcExitThread(void);                                       /* 0x0012F190 (svc 0x09) */
        Result svcCloseHandle(Handle handle);                           /* 0x0018A714 (svc 0x23) */
        Result svcWaitSynchronization1(Handle handle, s64 nanoseconds); /* 0x0018A868 (svc 0x24) */
        void svcBreak(u32 reason);                                      /* 0x0013EC48 (svc 0x3C) */
        void func_0013EC5C(s64 nanoseconds);                            /* 0x0013EC5C (svc 0x0A) */
#ifdef __cplusplus
}
#endif

#endif /* CTR_SVC_H */
