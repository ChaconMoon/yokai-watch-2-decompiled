# Official Documentation: Level-5 Cross-Platform Utilities (`lxp`)

> **Subsystem:** Level-5 Cross-Platform Utilities & Memory (`src/engine/lxp/`, `include/engine/lxp.h`)  
> **Layer:** Layer 2 — Level-5 Proprietary Engine  
> **Author & Documentation:** Carlos  
> **Status:** 100% C byte-exact matching (4 verified functions)

---

## 1. Subsystem Overview

The **`lxp` (*Level-5 Cross-Platform*)** layer contains Level-5's hardware-agnostic core libraries shared across platforms. It encapsulates low-level memory allocation pools, custom containers, file archives (`.fa` / `XPCK`), and data streaming.

The `lxpCMemory` subsystem serves as the centralized heap manager from which all framework sub-allocators and game subsystems allocate dynamic memory.

---

## 2. Global State & Symbols

Defined in [`include/engine/lxp.h`](../../include/engine/lxp.h):

* `unk_00868A9C` (`.data` / `.bss`): Level-5 engine core manager singleton instance.
* `unk_00868F10` (`.data` / `.bss`): Global `lxpCMemory` master memory allocator pointer.

---

## 3. Technical Specifications & Author's Notes

### 1. `func_0012CB00` — Global Engine Singleton Getter
* **Layer / Subsystem:** `engine/lxp`
* **VMA Address:** `0x0012CB00` (Size: 12 B)
* **Prototype:** `void *func_0012CB00(void)`
* **Source:** [`src/engine/lxp/func_0012CB00.c`](../../src/engine/lxp/func_0012CB00.c)
* **Header:** [`include/engine/lxp.h`](../../include/engine/lxp.h)
* **Disassembly:**
  ```arm
  ldr  r0, [pc]      @ 0x00868A9C
  bx   lr
  .word 0x00868A9C
  ```
* **Author's Notes:**
  Devuelve el puntero a la instancia global del singleton del Level 5 Cross Platform (lxp).

---

### 2. `func_0012FEC0` — `lxpCMemory` Boolean Constant Stub
* **Layer / Subsystem:** `engine/lxp`
* **VMA Address:** `0x0012FEC0` (Size: 8 B)
* **Prototype:** `s32 func_0012FEC0(void)`
* **Source:** [`src/engine/lxp/func_0012FEC0.c`](../../src/engine/lxp/func_0012FEC0.c)
* **Header:** [`include/engine/lxp.h`](../../include/engine/lxp.h)
* **Disassembly:**
  ```arm
  mov  r0, #1
  bx   lr
  ```
* **Author's Notes:**
  Metodo de consulta para saber que el sistema lxp esta levantado, devuleve siempre 1.

---

### 3. `func_00130018` — `lxpCMemory` Virtual Boolean Constant Stub
* **Layer / Subsystem:** `engine/lxp`
* **VMA Address:** `0x00130018` (Size: 8 B)
* **Prototype:** `s32 func_00130018(void)`
* **Source:** [`src/engine/lxp/func_00130018.c`](../../src/engine/lxp/func_00130018.c)
* **Header:** [`include/engine/lxp.h`](../../include/engine/lxp.h)
* **Disassembly:**
  ```arm
  mov  r0, #1
  bx   lr
  ```
* **Author's Notes:**
  Implementa la respuesta por defecto del sistema de gestión de memoria, devuelve siempre 1.

---

### 4. `func_001300B0` — `lxpCMemory` Allocator Pointer Getter
* **Layer / Subsystem:** `engine/lxp`
* **VMA Address:** `0x001300B0` (Size: 12 B)
* **Prototype:** `void *func_001300B0(void)`
* **Source:** [`src/engine/lxp/func_001300B0.c`](../../src/engine/lxp/func_001300B0.c)
* **Header:** [`include/engine/lxp.h`](../../include/engine/lxp.h)
* **Disassembly:**
  ```arm
  ldr  r0, [pc]      @ 0x00868F10
  bx   lr
  .word 0x00868F10
  ```
* **Author's Notes:**
  Acceso global del LXP (singleton)
