# Yo-kai Watch 2: Psychic Specters — Decompilation

A work-in-progress matching decompilation of *Yo-kai Watch 2: Psychic Specters* (*Mentespectros / Shin'uchi*, Level-5, 2014–2017) for the Nintendo 3DS (CTR).

The goal is clean, readable C/C++ source code that recompiles to a binary byte-for-byte identical to the original retail game (`code.raw.bin`).

Part of the [**#DecompilandoEn358Dias**](https://github.com/ChaconMoon/Decompilation-in-358-2) learning challenge.

---

## Disclaimer

This repository does **NOT** contain the game ROM, any copyrighted game assets, or proprietary Nintendo SDK binaries. An existing, legally obtained copy of the game is required to extract and verify the matching code.

This project is a **matching decompilation only**. It does not produce a standalone or playable game build, nor does it distribute proprietary code.

All trademarks, characters, game assets, and the original game binary are property of Level-5 Inc. and Nintendo.

---

## AI Transparency Policy

This project is part of the [**#DecompilandoEn358Dias**](https://github.com/ChaconMoon/Decompilation-in-358-2) learning journey.

In the interest of full transparency and academic honesty:
- **AI-Assisted and Co-Authored Code:** AI (Gemini / Antigravity) is used actively as a low-level technical assistant, helping navigate ARM11 disassembly, explore compiler heuristics (`armcc` RVCT 4.0 b821), draft initial C implementations, and extract modular assembly stubs.
- **Educational Laboratory:** The primary goal is mastering reverse engineering, ARM assembly idioms, and Nintendo 3DS system architecture. Carlos leads the architectural direction, semantics, naming, and verification, but does not claim sole handcrafted authorship over AI-assisted code.
- **No False Claims:** We make no false pretenses of this codebase being purely written by hand. Clear distinction between what is understood, what is verified, and what is AI-assisted is foundational to this repository.

For Carlos' full personal statement, see the [**Transparency in AI Usage**](https://github.com/ChaconMoon/Decompilation-in-358-2/blob/master/docs/AI-use-policy.MD) declaration in the main repository.

---

## Status & Progress

Exploratory matching passes targeting the European (`CTR-P-BYPP` / `00040000001B2900`) release.

Progress is split into categories so that extracted assembly stubs are never counted as C decompilation:

<!-- PROGRESS_STATS_START -->

| Category | Count | Meaning |
| :--- | :---: | :--- |
| **Decompiled C/C++ (Functions)** | **72** / 18,225 (0.40%) | Functions implemented in C/C++ and verified byte-exact |
| **Total Binary Code Covered** | **1,392 B** / 6,238,892 B (0.0223%) | C/C++ compiled bytes vs total executable `.text` (0.0180% of `7,737,344 B` binary) |
| **Assembly Stubs (`.s` extracted)** | **393** / 18,225 (2.16%) | Split stubs for building & progressive replacement (63,840 B / 1.0233%) |
| **Build Coverage (C/C++ + ASM Stubs)** | **465** / 18,225 (2.55%) | Combined C/C++ & assembly matching `code.raw.bin` (65,232 B / 1.0456%) |
| **Layer 1: Nintendo CTR-SDK (`src/ctr/`)** | **61** C matched + **390** stubs | CRT startup, `svc`, `nn::os`, `nn::y2r`, `nn::nex`, `nn::dsp` |
| **Layer 2: Level-5 Engine (`src/engine/`)** | **7** C matched + **3** stubs | `lfw` base classes, `lfwCLoop`, `lxp`, `gds` |
| **Layer 3: Yo-kai Watch 2 Game (`src/game/`)** | **4** C matched + **0** stubs | `ywCLoop*` state machines, battle, RPG entities |
| **Cataloged in Manifest** | **468** / 18,225 | Functions actively tracked across `src/` and `scratches/` |
| **Executable Size (`.text`)** | 6,238,892 B | Exact code segment size from NCCH ExHeader (EU `00040000001B2900`) |
| **Full Binary Image (`code.raw.bin`)** | 7,737,344 B | Decompressed CXI `.code` image (`.text` + `.rodata` + `.data`) |
| **Architecture** | ARM11 MPCore (ARMv6K) | 32-bit Little Endian, VMA `0x00100000` |
| **Compiler** | ARMCC / RVCT 4.0 b821 | CTR-SDK 1.2.7 (`1.2.7.f-NINTENDO-CTR-SDK-v1`) |

<!-- PROGRESS_STATS_END -->

> 📊 **Manifest & Catalogs:**
> - The active function catalog is maintained in [`config/functions.csv`](config/functions.csv).
> - The complete database of 18,225 functions classified by layer and difficulty is in [`config/functions_classified.csv`](config/functions_classified.csv).
> - All identified C++ classes and structures with vtable mappings are tracked in [`config/classes_identified.csv`](config/classes_identified.csv).

---

## 🏛️ Architectural Layers & Methodology

The codebase is organized into **three distinct architectural layers**:

1. **Layer 1 — Nintendo CTR-SDK & ARM Runtime (`src/ctr/`, `include/nn/`, `include/ctr/`)**
   - Startup routines (`crt`), kernel supervisor call wrappers (`svc`), and official CTR-SDK middleware (`nn::os`, `nn::fs`, `nn::ndm`, `nn::nex`, `nn::dsp`, `nn::y2r`).
   - Types and headers reference community standards ([3dsdecomp/nnsdk](https://github.com/3dsdecomp/nnsdk), [libctru](https://github.com/devkitPro/libctru)).

2. **Layer 2 — Level-5 Proprietary Engine (`src/engine/`, `include/engine/`)**
   - Shared Level-5 middleware: **LFW** (*Level-5 Framework*: base classes, `lfwCLoop`, cameras, managers), **LXP** (*Level-5 Cross-Platform*: memory managers, containers, resources), and **GDS** (*Generic Data Script*: data-driven script parsers).

3. **Layer 3 — Yo-kai Watch 2 Game Logic (`src/game/`, `include/game/`)**
   - Game-specific state machines (`ywCLoopMain`, `ywCLoopRPG`, `ywCLoopBattle`, menus), Yo-kai entities (`C$obj_yokai`), battle mechanics, and UI.

### 🔄 The "Split & Replace" Methodology
Inspired by modern decompilation workflows (such as [Yokimitsuro/khdays-decomp](https://github.com/Yokimitsuro/khdays-decomp) and Splat):
1. **Extraction into Modular Assembly (`.s`):** Non-decompiled routines are extracted into isolated `.s` files, ensuring 100% byte-exact matching and full buildability from day one.
2. **Progressive C/C++ Replacement:** Functions are iteratively decompiled into pure C/C++ (`.c` / `.cpp`), replacing their corresponding `.s` files one by one.
3. **Zero Regressions:** Every commit and change is strictly verified with `make check`. Assembly stubs are kept separate from genuine C decompilation in all progress metrics.

---

## Repository Layout

```text
.
├── src/                # Decompiled C/C++ source code and modular assembly stubs (.s)
│   ├── ctr/            # Layer 1: Nintendo CTR-SDK (crt/, svc/, nn/os/, nn/dsp/, nn/y2r/, nn/nex/)
│   ├── engine/         # Layer 2: Level-5 Engine (lfw/, lxp/, gds/, core/)
│   └── game/           # Layer 3: Yo-kai Watch 2 Game Logic (loops/, core/)
├── include/            # C/C++ headers, structures, and system types
│   ├── nn/             # Nintendo CTR-SDK official types (Result.h, Handle.h, os/, fs/, srv/, etc.)
│   ├── ctr/            # CTR subsystem aggregated headers (svc.h, os.h, y2r.h, nex.h, dsp.h)
│   ├── engine/         # Level-5 engine headers (lfw.h, lxp.h, core.h)
│   └── game/           # Game logic headers (loops.h, core.h)
├── config/             # Memory map (memory_map.json), manifests (functions.csv, classes_identified.csv)
├── tools/              # Verification (check_match.py), progress auditor, dump, and armcc compiler
├── scratches/          # Isolated WIP function matching scratchpads organized by layer
├── docs/               # Technical notes and daily reverse engineering session logs
└── notes/              # Didactic learning roadmap (ROADMAP.md) and per-function analysis
```

---

## Building & Verification

### 1. Extracting Reference Binaries
Place your legally obtained retail ROM (`.3ds`, `.cxi` or `.cia`) inside the project root:

```bash
python3 tools/extract_rom.py --rom 00040000001B2900_v00.3ds
```

This extracts and decompresses the executable to `extracted/code.raw.bin` (SHA-256: `b536dfce0a7138f2d5691532604d782b1ea3e20731120cc662baee118c370547`).

### 2. Compiling & Matching

```bash
make check            # Compiles and byte-compares candidate functions and stubs
make progress         # Audits progress metrics and synchronizes README.md
make report           # Generates reference objects and build/report.json via objdiff-cli
make classes          # Synchronizes config/classes_identified.csv from binary RTTI
```

Status indicators reported by `make check`:
- `>>> MATCH (C) <<<`: Real decompiled C/C++ function compiling byte-for-byte identical to the retail binary.
- `>>> ASM STUB <<<`: Modular assembly stub (`.s`) verified bit-for-bit to guarantee zero regressions during "Split & Replace".
- `>>> MATCH (COMMUNITY ACCEPTED) <<<`: Equivalent C implementation with acceptable compiler register allocation difference.
- `>>> REGRESSION / MISMATCH <<<`: Indicates a divergence against `extracted/code.raw.bin` that blocks matching.

### 3. Disassembling for decomp.me

```bash
make dump FUNC=0x0010B6E4                        # Raw assembly with relative offsets
python3 tools/dump_asm.py 0x0010B6E4 280 --plain # Instruction-only output ready for decomp.me
```

---

## Credits & External References

- **Level-5 Inc.**: Developers of *Yo-kai Watch 2*.
- **[3dsdecomp/nnsdk](https://github.com/3dsdecomp/nnsdk)**: Community reverse-engineering of the Nintendo 3DS SDK (`nnsdk`), providing standard `nn::` namespace definitions.
- **[devkitPro / libctru](https://github.com/devkitPro/libctru)**: Open-source Nintendo 3DS user-space library and hardware documentation.
- **Yokimitsuro ([khdays-decomp](https://github.com/Yokimitsuro/khdays-decomp))**: Decompilation guidance, repository design, and the progress reporting methodology that inspired this structure.
- **Jack Price-Burns ([Decomp Academy](https://decomp-academy.dev/))**: Interactive matching decompilation foundations.
- **[pyctr](https://github.com/ihaveamac/pyctr)**: 3DS container parsing and LZSS decompression tooling.
- **[decomp.dev](https://decomp.dev/)**: The community driving modern video game matching decompilation.