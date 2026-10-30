# Official Documentation: Supervisor Calls Subsystem (`ctr/svc`)

> **Subsystem:** Nintendo 3DS Kernel Supervisor Calls (`src/ctr/svc/`, `include/ctr/svc.h`)  
> **Layer:** Layer 1 — Nintendo CTR-SDK & ARM Runtime  
> **Author & Documentation:** Carlos  
> **Status:** 100% C byte-exact matching (25 verified routines)

---

## 1. Subsystem Overview

The **Supervisor Calls (`svc`)** subsystem represents the boundary between *Yo-kai Watch 2* (running in unprivileged ARM User Mode) and the Nintendo 3DS microkernel (running in privileged Supervisor Mode / Ring 0).

Because standard C does not have a native language construct to emit software interrupts, each routine acts as an assembly wrapper issuing an ARM `svc 0xNUM` instruction to request kernel-level operations:
* **Memory Management:** Heap and memory page allocation, permissions, and virtual address mapping.
* **Thread Scheduling:** Thread creation, termination, priorities, and execution yielding.
* **Synchronization Objects:** Kernel events, mutexes via address arbiters, and timers.
* **Handle Management:** Process, thread, and resource handle lifecycle.

---

## 2. Technical Specifications & Author's Notes

### I. Memory Management

#### 1. `svcControlMemory` (`0x0018A784` — 24 B)
* **SVC Opcode:** `svc 0x0B`
* **Prototype:** `Result svcControlMemory(u32 *addrOut, u32 addr0, u32 addr1, u32 size, u32 op, u32 perm)`
* **Source:** [`src/ctr/svc/svcControlMemory.c`](../../src/ctr/svc/svcControlMemory.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 2. `svcCreateMemoryBlock` (`0x0018A738` — 24 B)
* **SVC Opcode:** `svc 0x13`
* **Prototype:** `Result svcCreateMemoryBlock(Handle *memblock, u32 addr, u32 size, u32 myPerm, u32 otherPerm)`
* **Source:** [`src/ctr/svc/svcCreateMemoryBlock.c`](../../src/ctr/svc/svcCreateMemoryBlock.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 3. `svcCreateResourceLimit` (`0x0012F198` — 24 B)
* **SVC Opcode:** `svc 0x35`
* **Prototype:** `Result svcCreateResourceLimit(Handle *resourceLimit)`
* **Source:** [`src/ctr/svc/svcCreateResourceLimit.c`](../../src/ctr/svc/svcCreateResourceLimit.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

### II. Thread & Process Management

#### 4. `svcCreateThread` (`0x0018A750` — 24 B)
* **SVC Opcode:** `svc 0x27`
* **Prototype:** `Result svcCreateThread(Handle *thread, ThreadFunc entrypoint, u32 arg, u32 *stackTop, s32 priority, s32 processorId)`
* **Source:** [`src/ctr/svc/svcCreateThread.c`](../../src/ctr/svc/svcCreateThread.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 5. `svcExitThread` (`0x0012F190` — 8 B)
* **SVC Opcode:** `svc 0x09`
* **Prototype:** `void svcExitThread(void)`
* **Source:** [`src/ctr/svc/svcExitThread.c`](../../src/ctr/svc/svcExitThread.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 6. `svcSleepThread` (`0x00151FBC` — 8 B)
* **SVC Opcode:** `svc 0x28`
* **Prototype:** `void svcSleepThread(s64 nanoseconds)`
* **Source:** [`src/ctr/svc/svcSleepThread.c`](../../src/ctr/svc/svcSleepThread.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 7. `svcGetThreadId` (`0x00151FC4` — 24 B)
* **SVC Opcode:** `svc 0x37`
* **Prototype:** `Result svcGetThreadId(u32 *threadId, Handle thread)`
* **Source:** [`src/ctr/svc/svcGetThreadId.c`](../../src/ctr/svc/svcGetThreadId.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 8. `svcExitProcess` (`0x00104778` — 8 B)
* **SVC Opcode:** `svc 0x03`
* **Prototype:** `void svcExitProcess(void)`
* **Source:** [`src/ctr/svc/svcExitProcess.c`](../../src/ctr/svc/svcExitProcess.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

### III. Synchronization & Handles

#### 9. `svcCreateEvent` (`0x0010AAA8` — 24 B)
* **SVC Opcode:** `svc 0x21`
* **Prototype:** `Result svcCreateEvent(Handle *event, u32 resetType)`
* **Source:** [`src/ctr/svc/svcCreateEvent.c`](../../src/ctr/svc/svcCreateEvent.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 10. `svcCloseHandle` (`0x0018A714` — 8 B)
* **SVC Opcode:** `svc 0x23`
* **Prototype:** `Result svcCloseHandle(Handle handle)`
* **Source:** [`src/ctr/svc/svcCloseHandle.c`](../../src/ctr/svc/svcCloseHandle.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 11. `svcDuplicateHandle` (`0x0010AAC0` — 24 B)
* **SVC Opcode:** `svc 0x38`
* **Prototype:** `Result svcDuplicateHandle(Handle *handle, Handle original)`
* **Source:** [`src/ctr/svc/svcDuplicateHandle.c`](../../src/ctr/svc/svcDuplicateHandle.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 12. `svcWaitSynchronization1` (`0x0018A868` — 8 B)
* **SVC Opcode:** `svc 0x24`
* **Prototype:** `Result svcWaitSynchronization1(Handle handle, s64 nanoseconds)`
* **Source:** [`src/ctr/svc/svcWaitSynchronization1.c`](../../src/ctr/svc/svcWaitSynchronization1.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 13. `svcWaitSynchronizationN` (`0x0013EC64` — 36 B)
* **SVC Opcode:** `svc 0x25`
* **Prototype:** `Result svcWaitSynchronizationN(s32 *out, const Handle *handles, s32 handlesNum, bool waitAll, s64 nanoseconds)`
* **Source:** [`src/ctr/svc/svcWaitSynchronizationN.c`](../../src/ctr/svc/svcWaitSynchronizationN.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 14. `svcCreateAddressArbiter` (`0x00151FA0` — 24 B)
* **SVC Opcode:** `svc 0x17`
* **Prototype:** `Result svcCreateAddressArbiter(Handle *arbiter)`
* **Source:** [`src/ctr/svc/svcCreateAddressArbiter.c`](../../src/ctr/svc/svcCreateAddressArbiter.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 15. `svcArbitrateAddress` (`0x00166948` — 24 B)
* **SVC Opcode:** `svc 0x22`
* **Prototype:** `Result svcArbitrateAddress(Handle arbiter, u32 addr, u32 type, s32 val, s64 nanoseconds)`
* **Source:** [`src/ctr/svc/svcArbitrateAddress.c`](../../src/ctr/svc/svcArbitrateAddress.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 16. `svcCreateTimer` (`0x00112FF0` — 24 B)
* **SVC Opcode:** `svc 0x2D`
* **Prototype:** `Result svcCreateTimer(Handle *timer, u32 resetType)`
* **Source:** [`src/ctr/svc/svcCreateTimer.c`](../../src/ctr/svc/svcCreateTimer.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 17. `svcGetHandleInfo` (`0x0018A768` — 28 B)
* **SVC Opcode:** `svc 0x29`
* **Prototype:** `Result svcGetHandleInfo(s64 *out, Handle handle, u32 type)`
* **Source:** [`src/ctr/svc/svcGetHandleInfo.c`](../../src/ctr/svc/svcGetHandleInfo.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

### IV. Debug & System Helpers

#### 18. `svcBreak` (`0x0013EC48` — 8 B)
* **SVC Opcode:** `svc 0x3C`
* **Prototype:** `void svcBreak(u32 reason)`
* **Source:** [`src/ctr/svc/svcBreak.c`](../../src/ctr/svc/svcBreak.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 19. `func_0013EC50` — Thread Yield (`0x0013EC50` — 20 B)
* **SVC Opcode:** `svc 0x0A`
* **Prototype:** `void func_0013EC50(void)`
* **Source:** [`src/ctr/svc/func_0013EC50.c`](../../src/ctr/svc/func_0013EC50.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 20. `func_0013EC5C` — Sleep Milliseconds Wrapper (`0x0013EC5C` — 8 B)
* **SVC Opcode:** `svc 0x0A`
* **Prototype:** `void func_0013EC5C(s64 nanoseconds)`
* **Source:** [`src/ctr/svc/func_0013EC5C.c`](../../src/ctr/svc/func_0013EC5C.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 21. `func_0010AA84` — Alternate ControlMemory (`0x0010AA84` — 36 B)
* **SVC Opcode:** `svc 0x01`
* **Source:** [`src/ctr/svc/func_0010AA84.c`](../../src/ctr/svc/func_0010AA84.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 22. `func_00113008` — Alternate CreateThread (`0x00113008` — 36 B)
* **SVC Opcode:** `svc 0x08`
* **Source:** [`src/ctr/svc/func_00113008.c`](../../src/ctr/svc/func_00113008.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 23. `func_0013EC38` — Panic Break Stub (`0x0013EC38` — 24 B)
* **SVC Opcode:** `svc 0x3C`
* **Source:** [`src/ctr/svc/func_0013EC38.c`](../../src/ctr/svc/func_0013EC38.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 24. `func_0018A71C` — Alternate CreateMemoryBlock (`0x0018A71C` — 28 B)
* **SVC Opcode:** `svc 0x1E`
* **Source:** [`src/ctr/svc/func_0018A71C.c`](../../src/ctr/svc/func_0018A71C.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->

---

#### 25. `func_005F015C` — System Tick Pointer Store (`0x005F015C` — 24 B)
* **SVC Opcode:** `svc 0x28`
* **Source:** [`src/ctr/svc/func_005F015C.c`](../../src/ctr/svc/func_005F015C.c)
* **Header:** [`include/ctr/svc.h`](../../include/ctr/svc.h)
* **Author's Notes (Carlos):**
  <!-- Space for Carlos's official documentation notes -->
