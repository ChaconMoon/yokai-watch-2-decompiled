# Official Documentation: Network Daemon Manager (`nn::ndm`)

> **Subsystem:** Nintendo CTR-SDK Network Daemon Manager (`src/ctr/nn/ndm/`, `include/ctr/ndm.h`)  
> **Layer:** Layer 1 — Nintendo CTR-SDK & ARM Runtime  
> **Author & Documentation:** Carlos  
> **Status:** 100% C byte-exact matching (3 verified functions)

---

## 1. Subsystem Overview

The **Network Daemon Manager (`nn::ndm`)** is the Nintendo 3DS system service responsible for arbitrating background and foreground wireless network communications. It coordinates sleep-mode connectivity, SpotPass, StreetPass exchanges, and powers down the wireless hardware when the console lid is closed or battery levels drop.

In *Yo-kai Watch 2*, this subsystem manages connection state queries and bounds-checked indexing into the active network configuration tables.

---

## 2. Data Structures & Memory Layout

### `NdmContainer` & `NdmElement8` Layout
Defined in [`include/ctr/ndm.h`](../../include/ctr/ndm.h):

```cpp
/* Element size: 0x08 bytes (stride) */
typedef struct NdmElement8 {
    u32 field_00;   /* +0x00: Element attribute / identifier */
    u32 field_04;   /* +0x04: Connection parameter / status flags */
} NdmElement8;

/* Container header */
typedef struct NdmContainer {
    u32         unk_00;   /* +0x00: Header magic / state flags */
    u16         count;    /* +0x04: Active element count / table boundary */
    u16         unk_06;   /* +0x06: Alignment padding */
    u32         unk_08;   /* +0x08: Reserved / container flags */
    NdmElement8 items[1]; /* +0x0C: Dynamic array of network entries */
} NdmContainer;
```

---

## 3. Technical Specifications & Author's Notes

### 1. `func_00127EE0` — Global State Offset Reader
* **Layer / Subsystem:** `ctr/ndm`
* **VMA Address:** `0x00127EE0` (Size: 12 B)
* **Prototype:** `void *func_00127EE0(void)`
* **Source:** [`src/ctr/nn/ndm/func_00127EE0.c`](../../src/ctr/nn/ndm/func_00127EE0.c)
* **Header:** [`include/ctr/ndm.h`](../../include/ctr/ndm.h)
* **Disassembly:**
  ```arm
  ldr  r0, [pc]      @ 0x00865F18
  bx   lr
  .word 0x00865F18
  ```
* **Author's Notes:**
  Devuelve un puntero a una sub-estructura del estado de la red.

---

### 2. `func_00127EEC` — Global State Pointer Getter
* **Layer / Subsystem:** `ctr/ndm`
* **VMA Address:** `0x00127EEC` (Size: 12 B)
* **Prototype:** `void *func_00127EEC(void)`
* **Source:** [`src/ctr/nn/ndm/func_00127EEC.c`](../../src/ctr/nn/ndm/func_00127EEC.c)
* **Header:** [`include/ctr/ndm.h`](../../include/ctr/ndm.h)
* **Disassembly:**
  ```arm
  ldr  r0, [pc]      @ 0x00865F10
  bx   lr
  .word 0x00865F10
  ```
* **Author's Notes:**
  Devuelve un puntero a la instancia global (singleton) de la clase ndm

---

### 3. `func_001280A8` — Bounds-Checked Array Element Indexer
* **Layer / Subsystem:** `ctr/ndm`
* **VMA Address:** `0x001280A8` (Size: 24 B)
* **Prototype:** `NdmElement8 *func_001280A8(NdmContainer *ctx, u32 index)`
* **Source:** [`src/ctr/nn/ndm/func_001280A8.c`](../../src/ctr/nn/ndm/func_001280A8.c)
* **Header:** [`include/ctr/ndm.h`](../../include/ctr/ndm.h)
* **Disassembly:**
  ```arm
  ldrh  r2, [r0, #4]        @ Load count/capacity (+0x04)
  cmp   r2, r1              @ Compare count vs index
  addhi r0, r0, r1, lsl #3  @ If index < count: r0 += index * 8
  addhi r0, r0, #12         @ r0 += 0x0C (items array base offset)
  movls r0, #0              @ If index >= count: return NULL (0)
  bx    lr
  ```
* **Author's Notes:**
  Accede a los elementos de un array de conexiones web
