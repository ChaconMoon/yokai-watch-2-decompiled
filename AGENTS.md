# Instructions and Guidelines for Agents (AGENTS.md)

This repository is dedicated to the **matching decompilation** of *Yo-kai Watch 2: Psychic Specters* (*Mentespectros / Shin'uchi*, EU `00040000001B2900` / `CTR-P-BYPP`) for the Nintendo 3DS (CTR).

---

## ⚠️ Política de Uso de IA y Metodología "Split & Replace" (CRÍTICO)

### 🤖 Rol de la IA y del Desarrollador (Pacto de Trabajo en Pareja)
- **La IA asume la carga técnica de ingeniería inversa, matching y extracción:**
  - Extraer stubs en ensamblador (`.s`) organizados por clases y subsistemas modulares.
  - Generar el matching byte-exact 100% en C/C++ contra `code.raw.bin` configurando compiladores (`armcc` RVCT 4.0 b821 / GCC).
  - Proponer estructuras de datos y prototipos limpios en `include/`.
  - Explicar didácticamente el flujo de control, registros y arquitectura.
- **El Desarrollador (Carlos) asume la dirección de arquitectura, curaduría y documentación:**
  - Sustituir nombres provisionales o crudos (`field_524`, `unk_00814F28`) por nombres semánticos con significado en el juego/motor.
  - Redactar y enriquecer la documentación Doxygen (`@brief`, `@param`, `@return`, notas técnicas).
  - Cuidar la máxima legibilidad, formato y elegancia del código fuente.

### 🔄 Metodología "Split & Replace" (Inspirada en khdays-decomp y Splat)
1. **Extracción por Módulos:** Cada subsistema o clase en desarrollo se desglosa primero en funciones modulares en ensamblador (`.s`) para asegurar compilabilidad y verificación 100% byte-exact desde el inicio.
2. **Sustitución Progresiva a C/C++:** Siempre que se pueda decompilar en C/C++, se reemplaza el archivo `.s` por su equivalente `.c` / `.cpp`.
3. **Cero Regresiones:** Cada paso se valida inmediatamente con `make check`.
4. **Distinción por Capas:**
   - **Capa 1 (CTR-SDK / `src/ctr/`):** Decompilación asistida pragmática para resolver la infraestructura estándar del sistema basándose en proyectos de referencia (ACNL, libctru) y documentación oficial.
   - **Capas 2 y 3 (Engine / `src/engine/` y Game / `src/game/`):** Análisis profundo y guiado; el código de la lógica del juego y del motor de Level-5 se estudia, documenta y comprende a fondo.

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

### 🎓 Metodología del Ejercicio Didáctico Interactivo (OBLIGATORIO)

Para asegurar que el desarrollador (Carlos) comprenda a fondo la arquitectura, registros y semántica antes de organizar el código:

1. **Preparación Automática por la IA:**
   - Escribir el stub limpio `.s` en el directorio local protegido `asm/<layer>/<subsystem>/<symbol>.s` (ignorado en git) y proporcionar un enlace markdown clickeable para abrirlo en una pestaña del editor.
   - Actualizar automáticamente la cabecera correspondiente en `include/<layer>/` con el prototipo de la función y las declaraciones `extern` de variables de memoria.
2. **Planteamiento del Ejercicio:**
   - Entregar la función una por una con el formato estándar.
   - Plantear preguntas didácticas sobre qué hacen las instrucciones (desreferenciación, mnemónicos, tipos de datos C, convención AAPCS y retorno).
3. **Regla Socrática Estricta (NUNCA DAR LA SOLUCIÓN DIRECTA):**
   - **Si el desarrollador se equivoca o comete una imprecisión, la IA NUNCA debe darle la solución ni escribirle la respuesta.**
   - La IA debe responder con preguntas guía, pistas sobre registros o instrucciones concretas y analogías didácticas para que sea el propio desarrollador quien deduzca y corrija el error.
4. **Validación y Documentación:**
   - Una vez que el desarrollador explica o escribe el código C correcto, la IA lo consolida en `src/<layer>/<subsystem>/<symbol>.c` incorporando su explicación a los comentarios Doxygen.
   - Se valida inmediatamente con `make check` asegurando 100% byte-exact matching sin regresiones.

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
