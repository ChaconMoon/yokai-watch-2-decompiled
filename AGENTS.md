# Instructions and Guidelines for Agents (AGENTS.md)

This repository is dedicated to the **matching decompilation** of *Yo-kai Watch 2: Psychic Specters* (*Mentespectros / Shin'uchi*, EU `00040000001B2900` / `CTR-P-BYPP`) for the Nintendo 3DS (CTR).

---

## ⚠️ Strict User Rule (CRITICAL)

> **DO NOT return decompiled code (C / C++) to the user unless explicitly requested.**
> 
> - Do not write C reconstructions or pseudocode in responses unless the user expressly requests it (e.g., *"give me the C code for function X"*).
> - The agent's role must focus on:
>   - Explaining concepts and guiding workflows with a **didactic, progressive approach**.
>   - Inspecting assembly, instructions, registers, XREFs, vtables, and function calls via Ghidra / binutils.
>   - Dumping assembly (`tools/dump_asm.py`) formatted for `decomp.me`.
>   - Classifying functions into their architectural layer (`ctr`, `engine`, `game`), managing metrics, manifests (`config/functions.csv`, `config/functions_candidates.csv`, `config/functions_classified.csv`), and repository tools.
>   - Assisting with compiler configurations, options, and flags (ARMCC / RVCT 4.0 b821 vs GCC).

### 🛡️ Estándares de Sintaxis y Calidad en Decompilación (OBLIGATORIO)

- **Debes asegurarte de que la sintaxis de las funciones sea correcta según los estándares de los proyectos de decompilación; no debes aceptar nada que sea incorrecto** (por ejemplo: no aceptar aritmética cruda de punteros `*(u32 *)arg0` sobre `void *` cuando corresponde un `struct`, no dejar `structs` encerrados en archivos `.c` en lugar de `include/`, usar siempre hexadecimal `0x...` para offsets y paddings de estructuras, y evitar `__asm__` inline en funciones C decompilables).
- **Deberemos hacer una revisión de las funciones decompiladas para mejorar la sintaxis y que sea correcta según los estándares esperados en una decompilación.**

### 📋 Required Format When Delivering Functions to Decompile

Whenever the user requests functions to decompile, deliver them one by one following this exact structure:

```markdown
### Function <N>: `<symbol_name>` (Address: `<0xADDRESS>`)
- **Layer / Module:** `<ctr | engine | game>/<subsystem>` (Target path: `src/<layer>/<subsystem>/<symbol_name>.c`)
- **Didactic Level:** `<Level 1..4 — e.g. L1: Leaf Stub / L2: Accessor / L3: Control Flow / L4: C++ Vtable>`
- **Size:** <N> bytes of code (+ <N> bytes of literal pool if applicable)
- **Type:** <Brief functional description: stub, global setter, offset read, virtual method call...>
- **Literal pool / Notes:** <Detail loaded RAM addresses, offsets, XREFs, or constants>

```arm
<clean assembly instructions ready to paste into Target Assembly in decomp.me with internal branches resolved to local labels .L_<ADDRESS>>
```
```

---

## 🏛️ 3-Layer Repository Architecture & Didactic Methodology

Functions are **not** organized in a flat size-sorted folder. Instead, the project combines a **3-layer architectural hierarchy** with a **didactic progression** (Level 1 to Level 4) inside each layer:

1. **Layer 1 — Nintendo CTR-SDK & ARM Runtime (`src/ctr/`, `include/ctr/`)**
   - `src/ctr/crt/`: Startup routines (`_start`, `clear_bss`) and ARM C/C++ runtime (`aeabi`, Thumb library helpers).
   - `src/ctr/svc/`: Nintendo 3DS kernel Supervisor Call wrappers (`svcExitProcess`, `svcSleepThread`, `svcCreateEvent`, etc.).
   - `src/ctr/nn/`: Official CTR-SDK modules (`os/`, `fs/`, `ndm/`, `nex/`, `dsp/`, `y2r/`, `cecd/`).
2. **Layer 2 — Level-5 Proprietary Engine (`src/engine/`, `include/engine/`)**
   - `src/engine/lfw/`: *Level-5 Framework* base classes (`lfwCObject`, `lfwCLoop`, `lfwCLoopEmpty`, `lfwCObj2DManager`, `lfwCObj3DManager`, `lfwCCameraManager`).
   - `src/engine/lxp/`: *Level-5 Cross-Platform* utilities (`lxpCMemory`, `lxpCStack`, `.fa` / `XPCK` / `XCMB` containers).
   - `src/engine/gds/`: *Generic Data Script* (`GDSFix`, `GDSSwitch`, `.cfg.bin` parsers).
   - `src/engine/core/`: Shared Level-5 engine subsystems.
3. **Layer 3 — Yo-kai Watch 2 Game Logic (`src/game/`, `include/game/`)**
   - `src/game/loops/`: Game state machines derived from `lfwCLoop` (`ywCLoopMain`, `ywCLoopRPG`, `ywCLoopBattle`, `ywCLoopMenu*`, `ywCLoopOrgeTime`, `ywCLoopQR`, etc.).
   - `src/game/core/` (and `battle/`, `rpg/`, `menu/`, `world/`): Game-specific entities (`C$obj_yokai`), mechanics, and UI.

### File Granularity Convention
- **Current Didactic Stage:** Maintain **1 file per function** placed in its corresponding layer/submodule directory (e.g., `src/engine/lfw/func_0010B6D8.c`, WIP scratches in `scratches/<layer>/<subsystem>/`).
- **Translation Unit (TU) Consolidation:** Once all contiguous methods of a C++ class or module (verified via vtables/literal pools) are matched, they can be consolidated into a single class translation unit (e.g., `src/engine/lfw/lfwCLoopEmpty.c`).
- **Manifest Discipline (`config/functions.csv`):** Every cataloged function must specify `address,symbol,size,layer,subsystem,level,status,description` and remain sorted in ascending hexadecimal address order.

---

## Project Information & ExHeader Memory Map

- **Platform:** Nintendo 3DS (CTR)
- **Architecture:** ARM11 MPCore (`ARM:LE:32:v6` / ARMv6K, Little Endian)
- **Base Address (VMA):** `0x00100000`
- **Reference Binary:** `extracted/code.raw.bin` (`7,737,344` bytes total image)
  - SHA-256 Hash: `b536dfce0a7138f2d5691532604d782b1ea3e20731120cc662baee118c370547`
- **Target Compiler:** ARM C/C++ Compiler (`armcc` RVCT 4.0 b821 via `tools/wibo`, SDK `1.2.7.f-NINTENDO-CTR-SDK-v1`, fallback `arm-none-eabi-gcc`)
- **Canonical ExHeader Section Map (`config/memory_map.json`):**

| Section | Start VMA | End VMA | Exact Size | Notes |
| :--- | :--- | :--- | :---: | :--- |
| **`.text`** | `0x00100000` | `0x006F32AC` | `6,238,892 B` (`0x5F32AC`) | **18,225 valid executable functions** (`ctr`: ~3,632, `engine`: ~6,590, `game`: ~7,996) |
| **`.rodata`** | `0x006F4000` | `0x0080C42C` | `1,147,948 B` (`0x11842C`) | Read-only strings, constants, and C++ `vtables` (never classify `.rodata` addresses as functions) |
| **`.data`** | `0x0080D000` | `0x00860934` | `342,324 B` (`0x053934`) | Initialized globals and RTTI class name strings (`lfw*`, `yw*`) |
| **`.bss`** | `0x00860934` | `0x0091B9BC` | `766,088 B` (`0x0BB088`) | Zero-initialized globals cleared at boot by `clear_bss` (`0x00100024`) |

---

## Tooling & Environment

### 1. Ghidra & MCP Server
- **GhidraMCP** extension listening at `http://127.0.0.1:8080/` (when Ghidra is open).
- Enables querying Ghidra directly (`get_program_info`, `disassemble_function`, `get_function_by_address`, `list_functions`, `read_memory`, etc.).

### 2. Local Scripts (`tools/`) & Makefile Targets
- `tools/dump_asm.py` (`make dump FUNC=0xADDRESS`):
  - Dumps clean function disassembly with relative offsets or `--plain` mode ready for `decomp.me`. Supports ARM (default) and Thumb (`--thumb`).
- `tools/check_match.py` (`make check`):
  - Compiles all units in `src/` into `build/src/<layer>/<subsystem>/*.o` and verifies byte-exact instruction and ELF relocation matching against `extracted/code.raw.bin`.
- `tools/classify_functions.py`:
  - Classifies all `.text` functions (`0x00100000`–`0x006F32AC`) by architectural layer (`ctr`, `engine`, `game`), subsystem, and didactic difficulty (`1_trivial` to `7_complex_caller`) into `config/functions_classified.csv`.
- `tools/audit_progress.py` (`make progress`):
  - Reads `config/functions.csv`, computes per-layer metrics relative to the exact `.text` size (`6,238,892` bytes / `18,225` functions), and updates `README.md` and `objdiff.json`.
- `tools/generate_expected.py` & `tools/generate_undecompiled.py` (`make report`):
  - Generates reference `.o` files in `expected/` and builds `build/report.json` via `tools/objdiff-cli`.
- `tools/extract_rom.py` (`make extract`):
  - Extracts and decompresses `code.raw.bin` from decrypted `.3ds` / `.cxi` ROMs.
