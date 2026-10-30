# Official Documentation: Core Subsystems (`engine/core` & `game/core`)

> **Subsystem:** Engine & Game Core Singletons (`src/engine/core/`, `src/game/core/`)  
> **Layer:** Layer 2 (Level-5 Engine) & Layer 3 (Game Logic)  
> **Author & Documentation:** Carlos  
> **Status:** 100% C byte-exact matching (3 verified functions)

---

## 1. Subsystem Overview

This module covers the core singleton managers and callback helpers operating across the boundary between Level-5's proprietary engine base and Yo-kai Watch 2's high-level game logic:

* **Engine Core (`engine/core`):** Maintains the primary framework controller reference in `.data`/`.bss`.
* **Game Core (`game/core`):** Holds the master pointer to active gameplay entities (`C$obj_yokai`) and provides standard null-stub callbacks (`bx lr`).

---

## 2. Technical Specifications & Author's Notes

### 1. `func_0013F29C` — Level-5 Engine Core Pointer Getter
* **Layer / Subsystem:** `engine/core`
* **VMA Address:** `0x0013F29C` (Size: 12 B)
* **Prototype:** `void *func_0013F29C(void)`
* **Source:** [`src/engine/core/func_0013F29C.c`](../../src/engine/core/func_0013F29C.c)
* **Header:** [`include/engine/core.h`](../../include/engine/core.h)
* **Disassembly:**
  ```arm
  ldr  r0, [pc]      @ 0x00867DA8
  bx   lr
  .word 0x00867DA8
  ```
* **Author's Notes:**
  Devuelve la instancia maestra (singleton) del Level 5 Framework

---

### 2. `func_00171C78` — Game Subsystem Entity Manager Pointer Getter
* **Layer / Subsystem:** `game/core`
* **VMA Address:** `0x00171C78` (Size: 12 B)
* **Prototype:** `void *func_00171C78(void)`
* **Source:** [`src/game/core/func_00171C78.c`](../../src/game/core/func_00171C78.c)
* **Header:** [`include/game/core.h`](../../include/game/core.h)
* **Disassembly:**
  ```arm
  ldr  r0, [pc]      @ 0x0091B7B8
  bx   lr
  .word 0x0091B7B8
  ```
* **Author's Notes:**
  Devuelve la instancia maestra (singleton) del gestor de entidades del juego.

---

### 3. `func_0017656C` — Game Subsystem Null Callback Stub
* **Layer / Subsystem:** `game/core`
* **VMA Address:** `0x0017656C` (Size: 4 B)
* **Prototype:** `void func_0017656C(void)`
* **Source:** [`src/game/core/func_0017656C.c`](../../src/game/core/func_0017656C.c)
* **Header:** [`include/game/core.h`](../../include/game/core.h)
* **Disassembly:**
  ```arm
  bx   lr
  ```
* **Author's Notes (Carlos):**
  Se utiliza en tablas de callbacks o punteros a funciones donde un estado no requiere realizar ninguna acción.
