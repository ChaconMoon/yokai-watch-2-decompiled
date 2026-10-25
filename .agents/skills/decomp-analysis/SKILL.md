---
name: decomp-analysis
description: >-
  Analyzes any Nintendo 3DS function by name, symbol, or hexadecimal address for matching
  decompilation. Use this skill whenever the user asks to analyze, inspect, classify, or
  decompile a function (or invokes decomp-analysis), returning its clean ARM/Thumb assembly,
  technical explanation, namespace/submodule/class classification, proposed demangled & mangled
  names, target source/header paths, header layout explanation, and (when explicitly requested)
  the decompiled C/C++ code and full repository implementation.
---

# `decomp-analysis` — 3DS Function Decompilation & Classification Skill

This skill provides a standardized, end-to-end workflow to analyze, classify, explain, and (when explicitly requested) decompile and implement functions from a Nintendo 3DS (`ARM11 MPCore` / `ARMv6K`) binary. It is built for *Yo-kai Watch 2: Psychic Specters* and designed to be directly portable to any other Nintendo 3DS decompilation project.

---

## 1. Input Parameters

The skill accepts a **function identifier** (`<target>`), plus optional flags depending on the user's request:
- **`<target>` (Required)**:
  - A hexadecimal virtual memory address (e.g., `0x00340FEC`, `00340E5C`, `0x10B6D8`).
  - A raw or catalog symbol name (e.g., `func_00340FEC`, `FUN_00340e5c`, `svcExitProcess`).
  - A mangled or demangled C++ identifier (e.g., `_ZN2nn3nex21StationConnectionInfo5resetEv`, `StationConnectionInfo::reset`).
- **Explicit Request Modes**:
  - **Analysis Mode (Default per `AGENTS.md`)**: Returns the assembly, step-by-step explanation, classification (`Namespace`, `Layer/Submodule`, `Class`), proposed names, target paths (`src/` and `include/`), and header structure explanation **without** returning decompiled C/C++ code unless requested.
  - **Code Return Mode (*"devuelve el código decompilado / C++"*):** Also returns the exact, syntax-compliant C/C++ reconstruction matching the repository's coding style.
  - **Implementation Mode (*"impleméntalo"*):** Writes the declaration into the target header (`include/...`), adds the C/C++ implementation into the target source file (`src/...`), registers the symbol in `config/functions.csv` (sorted by ascending hexadecimal address), and verifies byte-exact matching via `make check`.

---

## 2. Step-by-Step Execution Procedure

### Step 1: Run the Automated Analyzer Script
Execute the bundled analyzer script passing the function identifier:
```bash
python3 .agents/skills/decomp-analysis/scripts/analyze_function.py <target>
```
- The script automatically inspects `extracted/code.raw.bin` (at base VMA `0x00100000`), resolves function bounds, disassembles ARM/Thumb instructions, resolves literal pool words (`.rodata` strings, vtables, constants), scans cross-references (XREFs), and infers the hierarchical classification.
- If the function size is not in the catalog or needs overriding, pass `--size <bytes>`. For Thumb functions, pass `--thumb`.
- For detailed ABI rules, consult [3ds-abi-and-patterns.md](./references/3ds-abi-and-patterns.md).

### Step 2: Verify Neighboring Context & Headers
Read the target header (`include/<layer>/<submodule>.h`) and target source file (`src/<layer>/<submodule>/<Class>.cpp` or `.c`) reported by the script to ensure full consistency with existing class definitions, member names, and indentation.

### Step 3: Deliver the Standardized `decomp-analysis` Report
Format your response using the following structured template:

```markdown
### Función: `<Nombre Propuesto C++>` (Dirección: `<0xADDRESS>`)
- **Identificador actual / Símbolo Mangled:** `<func_XXXXXXXX>` $\rightarrow$ `<_ZN... o nombre C>`
- **Clasificación Jerárquica:**
  - **Espacio de nombres (`Namespace`):** `<e.g., nn::nex | lfw | yw | extern "C">`
  - **Capa y Submódulo (`Layer / Submodule`):** `<ctr | engine | game>/<submódulo>`
  - **Clase / Estructura (`Class`):** `<Nombre de la clase o estructura>`
- **Rutas en el Repositorio:**
  - **Código fuente (`Source`):** `src/<layer>/<submodule>/<Archivo>.cpp` (o `.c`)
  - **Cabecera (`Header`):** `include/<layer>/<header>.h`
- **Tamaño:** `<N>` bytes de código (+ `<M>` bytes de literal pool si aplica)

#### 1. Ensamblador (`Target Assembly`)
```arm
<ensamblador limpio devuelto por analyze_function.py listo para decomp.me>
```

#### 2. Explicación Técnica de Qué Hace
- **Registros de entrada y salida:** Detallar qué recibe en `r0` (`this` o primer argumento), `r1`–`r3`, y qué devuelve en `r0` (o `r0:r1`).
- **Operaciones e instrucciones paso a paso:** Explicar el prólogo/epílogo, accesos a memoria con sus desplazamientos en hexadecimal (`+0x00`, `+0x04`, `+0x0C`...), constantes del literal pool, subllamadas (`bl`) y saltos condicionales.

#### 3. Explicación de Cabeceras (`include/...`)
- Explicar el layout de la clase/estructura involucrada, los tipos de ancho fijo de `include/types.h` (`u8`, `u16`, `u32`, `s16`, `s32`, `f32`, etc.), los offsets en hexadecimal (`0x...`) y cómo debe declararse el prototipo o método dentro de su `namespace` y `class`.
```

### Step 4: Return C++ Code & Implement (When Explicitly Requested)
1. **If the user explicitly requests the decompiled C/C++ code**, include a section **`#### 4. Código C++ Decompilado`** adhering strictly to the repository's syntax standards:
   - Use canonical fixed-width types from `include/types.h` (`u8`, `u16`, `u32`, `u64`, `s8`, `s16`, `s32`, `s64`, `f32`, `f64`).
   - Never use raw pointer arithmetic (`*(u32 *)((u8 *)this + 4)`) or `void *` casts when a `class` or `struct` models the layout.
   - Never place `struct` or `class` definitions inside `.c`/`.cpp` files; all definitions belong in `include/`.
   - Never use inline `__asm__` in decompilable C/C++ functions.
   - Follow the Allman brace style and 8-space/tab indentation inside `namespace` blocks used in `include/ctr/nex.h` and `src/ctr/nn/nex/*.cpp`, annotating each method with `// Function XXXXXXXX (<description>)`.
2. **If the user explicitly requests implementation**:
   - Edit the header file (`include/...`) and source file (`src/...`).
   - Add or update the entry in `config/functions.csv` keeping strict ascending hexadecimal address order:
     `address,symbol,size,layer,subsystem,level,status,description`
   - Run `make check` to compile with `armcc` (RVCT 4.0 b821 via `wibo`) / `arm-none-eabi-g++` and verify byte-exact matching against `extracted/code.raw.bin`.

---

## 3. Extrapolation to Other Nintendo 3DS Projects

The `.agents/skills/decomp-analysis` directory is self-contained and can be copied into any Nintendo 3DS decompilation repository:
- By default, `scripts/analyze_function.py` uses `--base-vma 0x00100000` (standard 3DS ExHeader `.text` base) and looks for `extracted/code.raw.bin` or `extracted/code.bin`.
- To target a different binary or VMA in another 3DS title, pass:
  ```bash
  python3 .agents/skills/decomp-analysis/scripts/analyze_function.py <target> \
    --binary path/to/code.bin \
    --base-vma 0x00100000 \
    --config-dir path/to/config
  ```
- Even if a new 3DS project does not yet have CSV catalogs (`functions.csv` or `classes_identified.csv`), the script automatically detects function boundaries (`bx lr` / `pop {..., pc}`), literal pools, strings, XREFs, and struct field offsets directly from the raw binary.

