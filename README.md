# Yo-kai Watch 2: Psychic Specters — Decompilation

A work-in-progress matching decompilation of *Yo-kai Watch 2: Psychic Specters* (*Mentespectros / Shin'uchi*, Level-5, 2014–2017) for the Nintendo 3DS.

The goal is C source that recompiles to a binary byte-for-byte identical to the original game code.

Part of the [**#DecompilandoEn358Dias**](https://github.com/ChaconMoon/Decompilation-in-358-2) challenge.

---

## Disclaimer

This repository does **NOT** contain the game ROM, any game assets, or any of the original binary/assembly. An existing, legally-obtained copy of the game is required to extract and build it.

This repository is a **matching decompilation only**. It does not contain or produce a playable build or any redistributable game binary, and building it requires an original, legally-obtained copy of the game.

All trademarks, characters, and the original game are property of Level-5 Inc. and Nintendo.

---

## AI Transparency Policy

This project is part of the [**#DecompilandoEn358Dias**](https://github.com/ChaconMoon/Decompilation-in-358-2) learning challenge.

In the interest of full transparency and honesty:
- **AI-Generated and Assisted Code**: AI (Gemini / Antigravity) is actively used in this project not only as an educational tutor for low-level concepts, but also to generate, draft, and test C implementations for matching. Several functions in this repository have been written or drafted with AI rather than written purely by hand.
- **Educational Laboratory**: The primary value of this project is learning to navigate ARM11 assembly, compiler quirks (RVCT/ARMCC), and 3DS reverse engineering. Carlos does not claim sole human authorship over code or solutions generated or co-authored with AI.
- **No False Claims**: We do not pretend this repository is entirely handcrafted. Being clear about what is AI-assisted and what is understood is central to the integrity of this journey.

For Carlos's full personal statement on the role, ethics, and daily reality of AI in this challenge, see the English [**Transparency in AI Usage**](https://github.com/ChaconMoon/Decompilation-in-358-2/blob/master/docs/AI-use-policy.MD) declaration in the main repository.

---

## Status

Initial exploratory passes on the EU (`00040000001B2900`) ARM11 executable (`code.raw.bin`, 7,737,344 bytes, image base `0x00100000`).

The current objective is establishing a reproducible verification pipeline, matching the first batch of atomic leaf functions, and classifying library vs game engine routines.

Progress is split into categories so that assembly is never counted as C decompilation:

<!-- PROGRESS_STATS_START -->

| Category | Count | Meaning |
| :--- | :---: | :--- |
| **Real C-decompiled matched functions** | **29** / 18,225 (0.16%) | Functions implemented in C and verified byte-exact |
| **Complete functions (C + verified original library assembly)** | **30** / 18,225 (0.16%) | Real C (29) + CRT/SDK assembly routines (1: `clear_bss`, etc.) |
| **Real C-decompiled matched bytes** | **408** / 6,238,892 bytes (0.0065%) | Real-C-only byte progress (444 B including CRT assembly) |
| **Layer 1: Nintendo CTR-SDK & Runtime (`src/ctr/`)** | **19** matched (320 B) | CRT startup, `svc` syscalls, `nn::os`, `nn::ndm`, `nn::nex` |
| **Layer 2: Level-5 Engine (`src/engine/`)** | **7** matched (72 B) | `lfw` (Framework), `lxp` (Cross-Platform), `gds` (Scripts) |
| **Layer 3: Yo-kai Watch 2 Game (`src/game/`)** | **4** matched (52 B) | `ywCLoop*` states, battle, RPG, menus, and entities |
| **Named / mapped candidates in manifest** | **32** / 18,225 | Functions actively tracked across `src/` and `scratches/` |
| **Memory Map (`.text` / `.rodata` / `.data` / `.bss`)** | Verified | Exact ExHeader boundaries mapped in `config/memory_map.json` |
| **Total `.text` functions** | 18,225 | Verified function count in `0x00100000`–`0x006F32AC` (EU v1.0) |
| **Region** | EU (`00040000001B2900`) | Multi-5 (PAL v1.0, `CTR-P-BYPP`) |
| **Architecture** | ARM11 MPCore (ARMv6K) | 32-bit Little Endian, VMA `0x00100000` |
| **Compiler** | ARMCC / RVCT 4.0 b821 | CTR-SDK 1.2.7 (`1.2.7.f-NINTENDO-CTR-SDK-v1`) |

<!-- PROGRESS_STATS_END -->

---

### Progress reporting policy

Only real C implementations are counted as C-decompiled progress. Assembly, whether a library's own or an authorized inline exception, is counted separately, and so is anything under `scratches/` or unverified headers.

---

## Target Candidates & Current Manifest

<!-- MANIFEST_TABLE_START -->

| Virtual Address | Symbol / Name | Layer / Module | Size | Level | Status | Description / Notes |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `0x00100024` | `clear_bss` | `ctr/crt` | 36 B | `2_control_flow` | 🟢 Matched | CRT startup zeroing loop for .bss section (0x00860934 - 0x0091B9BC) |
| `0x00104778` | `svcExitProcess` | `ctr/svc` | 8 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x03) |
| `0x00104D18` | `func_00104D18` | `ctr/nn_os` | 16 B | `2_accessor` | 🟢 Matched | nn::os startup global 8-bit flag setter (0x00814E54) |
| `0x001063F4` | `func_001063F4` | `ctr/nn_os` | 16 B | `2_accessor` | 🟢 Matched | CTR OS SystemConfig block field reader (0x1FF80000 + 0x40) |
| `0x0010678C` | `func_0010678C` | `ctr/nn_os` | 16 B | `2_accessor` | 🟢 Matched | nn::os startup global signed byte reader via literal pool (0x00814E00) |
| `0x0010AAA8` | `svcCreateEvent` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x21) |
| `0x0010AAC0` | `svcDuplicateHandle` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x38) |
| `0x0010B6D0` | `func_0010B6D0` | `engine/lfw` | 8 B | `1_leaf_stub` | 🟢 Matched | lfwCLoopEmpty virtual method (returns constant 0, table 0x00107488) |
| `0x0010B6D8` | `func_0010B6D8` | `engine/lfw` | 12 B | `2_accessor` | 🟢 Matched | lfwCLoopEmpty::GetClassName getter via literal pool (0x008602F8) |
| `0x0010B6E4` | `func_0010B6E4` | `engine/lfw` | 280 B | `4_cpp_vtable` | 🟡 In Review | lfwCLoop C++ class method (partially decompiled, ~82% match in decomp.me) |
| `0x0010C894` | `func_0010C894` | `game/loops` | 12 B | `2_accessor` | 🟢 Matched | Game loop subsystem pointer getter via literal pool (0x0086C8CC) |
| `0x0011054C` | `func_0011054C` | `game/loops` | 24 B | `3_arithmetic_logic` | 🟢 Matched | Struct header reset (zeros 8 bytes, sets byte 0 to 0xFF) |
| `0x001274A0` | `func_001274A0` | `ctr/nn_os` | 24 B | `3_arithmetic_logic` | 🟡 In Review | nn::os atomic spinlock acquire loop (ldrex/strex synchronization) |
| `0x00127520` | `func_00127520` | `ctr/nn_os` | 12 B | `2_accessor` | 🟢 Matched | CTR-SDK .text size / limit getter via literal pool (0x005F32AC) |
| `0x00127EEC` | `func_00127EEC` | `ctr/nn_ndm` | 12 B | `2_accessor` | 🟢 Matched | nn::ndm global state pointer getter via literal pool (0x00865F10) |
| `0x001280A8` | `func_001280A8` | `ctr/nn_ndm` | 24 B | `3_arithmetic_logic` | 🟢 Matched | nn::ndm bounds-checked struct array element indexer (stride 8, offset +0x0C) |
| `0x0012CB00` | `func_0012CB00` | `engine/lxp` | 12 B | `2_accessor` | 🟢 Matched | Level-5 engine global singleton getter via literal pool (0x00868A9C) |
| `0x0012FEC0` | `func_0012FEC0` | `engine/lxp` | 8 B | `1_leaf_stub` | 🟢 Matched | lxpCMemory boolean true stub (returns constant 1) |
| `0x00130018` | `func_00130018` | `engine/lxp` | 8 B | `1_leaf_stub` | 🟢 Matched | lxpCMemory virtual boolean true stub (returns constant 1) |
| `0x001300B0` | `func_001300B0` | `engine/lxp` | 12 B | `2_accessor` | 🟢 Matched | lxpCMemory manager pointer getter via literal pool (0x00868F10) |
| `0x0013F29C` | `func_0013F29C` | `engine/core` | 12 B | `2_accessor` | 🟢 Matched | Level-5 engine subsystem pointer getter via literal pool (0x00867DA8) |
| `0x00151FA0` | `svcCreateAddressArbiter` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x17) |
| `0x00151FBC` | `svcSleepThread` | `ctr/svc` | 8 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x28) |
| `0x00151FC4` | `svcGetThreadId` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x37) |
| `0x00171C78` | `func_00171C78` | `game/core` | 12 B | `2_accessor` | 🟢 Matched | Game subsystem global pointer getter via literal pool (0x0091B7B8) |
| `0x0017656C` | `func_0017656C` | `game/core` | 4 B | `1_leaf_stub` | 🟢 Matched | Game subsystem leaf empty void stub function (bx lr) |
| `0x00301248` | `func_00301248` | `ctr/nn_nex` | 4 B | `1_leaf_stub` | 🟢 Matched | nn::nex leaf empty void stub function (bx lr) |
| `0x00340CE8` | `func_00340CE8` | `ctr/nn_nex` | 20 B | `2_accessor` | 🟢 Matched | nn::nex multi-field struct copy assignment (32-bit +0x00, 16-bit +0x04) |
| `0x00340CFC` | `func_00340CFC` | `ctr/nn_nex` | 12 B | `2_accessor` | 🟢 Matched | nn::nex multi-field struct setter (32-bit +0x00, 16-bit +0x04) |
| `0x00340D08` | `func_00340D08` | `ctr/nn_nex` | 16 B | `2_accessor` | 🟢 Matched | nn::nex multi-field struct zero initializer (32-bit +0x00, 16-bit +0x04) |
| `0x00340D18` | `func_00340D18` | `ctr/nn_nex` | 4 B | `1_leaf_stub` | 🟢 Matched | nn::nex empty void leaf stub function (bx lr) |
| `0x00340D1C` | `func_00340D1C` | `ctr/nn_nex` | 20 B | `2_accessor` | 🟢 Matched | nn::nex multi-field struct copy constructor (32-bit +0x00, 16-bit +0x04) |

<!-- MANIFEST_TABLE_END -->

---

## Architectural Layers & Didactic Decompilation Roadmap

Instead of sorting functions purely by byte size across the entire binary, the decompilation is organized into **three architectural layers** (`ctr`, `engine`, `game`), and within each layer candidates are ordered by **didactic complexity level** (from Level 1 leaf stubs up to Level 4 C++ vtables):

### Layer 1: Nintendo CTR-SDK & ARM Runtime (`src/ctr/`)
Standard Nintendo 3DS system libraries (`1.2.7.f-NINTENDO-CTR-SDK-v1`), kernel supervisor calls (`svc`), C/C++ runtime startup (`crt`), and `nn::*` modules (`nn::os`, `nn::fs`, `nn::ndm`, `nn::nex`, `nn::dsp`).

| Didactic Level | Virtual Address | Symbol | Module | Size | Status | Description |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **L1: Syscall Stub** | `0x00104778` | `svcExitProcess` | `ctr/svc` | 8 B | 🟢 Matched | Kernel syscall wrapper (`svc 0x03`) |
| **L1: Syscall Stub** | `0x00151FBC` | `svcSleepThread` | `ctr/svc` | 8 B | 🟢 Matched | Kernel syscall wrapper (`svc 0x28`) |
| **L1: Leaf Stub** | `0x00301248` | `func_00301248` | `ctr/nn_nex` | 4 B | 🟢 Matched | Empty void stub (`bx lr`) in `nn::nex` |
| **L2: OS Accessor** | `0x00104D18` | `func_00104D18` | `ctr/nn_os` | 16 B | 🟢 Matched | Global 8-bit flag setter (`0x00814E54`) |
| **L2: MMIO Reader** | `0x001063F4` | `func_001063F4` | `ctr/nn_os` | 16 B | 🟢 Matched | Reads CTR `SystemConfig` page (`0x1FF80040`) |
| **L2: OS Accessor** | `0x0010678C` | `func_0010678C` | `ctr/nn_os` | 16 B | 🟢 Matched | Signed byte reader (`0x00814E00`) |
| **L2: CRT Loop** | `0x00100024` | `clear_bss` | `ctr/crt` | 36 B | 🟢 Matched | Startup `.bss` zeroing loop (`0x00860934`–`0x0091B9BC`) |
| **L3: Synchronization** | `0x001274A0` | `func_001274A0` | `ctr/nn_os` | 24 B | 🟡 In Review | Atomic spinlock acquire loop (`ldrex`/`strex`) |
| **L3: Syscall + Stack** | `0x0010AAA8` | `svcCreateEvent` | `ctr/svc` | 24 B | ⏳ Candidate | Kernel syscall wrapper with output pointer (`svc 0x21`) |
| **L3: Syscall + Stack** | `0x0010AAC0` | `svcDuplicateHandle` | `ctr/svc` | 24 B | ⏳ Candidate | Kernel syscall wrapper (`svc 0x38`) |
| **L3: Array Indexer** | `0x001280A8` | `func_001280A8` | `ctr/nn_ndm` | 24 B | ⏳ Candidate | Bounds-checked array element indexer (stride 8) |

### Layer 2: Level-5 Proprietary Engine (`src/engine/`)
Shared Level-5 middleware used across 3DS titles: **LFW** (*Level-5 Framework*: `lfwCObject`, `lfwCLoop`, `lfwCObj2DManager`, `lfwCObj3DManager`, `lfwCCameraManager`), **LXP** (*Level-5 Cross-Platform*: `lxpCMemory`, `lxpCStack`, `.fa` / `XPCK` archives), and **GDS** (*Generic Data Script*: `GDSFix`, `GDSSwitch`, `.cfg.bin` parsers).

| Didactic Level | Virtual Address | Symbol | Module | Size | Status | Description |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **L1: Virtual Stub** | `0x0010B6D0` | `func_0010B6D0` | `engine/lfw` | 8 B | 🟢 Matched | `lfwCLoopEmpty` virtual method (returns `0`, table `0x00107488`) |
| **L1: Virtual Stub** | `0x0012FEC0` | `func_0012FEC0` | `engine/lxp` | 8 B | 🟢 Matched | `lxpCMemory` boolean stub (returns `1`) |
| **L1: Virtual Stub** | `0x00130018` | `func_00130018` | `engine/lxp` | 8 B | 🟢 Matched | `lxpCMemory` virtual method (returns `1`, in 3 `.rodata` vtables) |
| **L2: RTTI Getter** | `0x0010B6D8` | `func_0010B6D8` | `engine/lfw` | 12 B | 🟢 Matched | `lfwCLoopEmpty::GetClassName` (`"lfwCLoopEmpty"` at `0x008602F8`) |
| **L2: Singleton Getter** | `0x0012CB00` | `func_0012CB00` | `engine/lxp` | 12 B | 🟢 Matched | Engine singleton getter (`0x00868A9C`, 10 callers) |
| **L2: Manager Getter** | `0x001300B0` | `func_001300B0` | `engine/lxp` | 12 B | 🟢 Matched | `lxpCMemory` manager pointer getter (`0x00868F10`) |
| **L3: Forwarding Thunk** | `0x00130D38` | `func_00130D38` | `engine/lxp` | 16 B | ⏳ Candidate | Null-checked method forwarding tail-call wrapper |
| **L4: C++ Class Method** | `0x0010B5D8` | `func_0010B5D8` | `engine/lfw` | 248 B | ⏳ Candidate | `lfwCLoopEmpty` factory / constructor (`0x00107484`) |
| **L4: C++ Class Method** | `0x0010B6E4` | `func_0010B6E4` | `engine/lfw` | 280 B | 🟡 In Review | `lfwCLoop` state update method with vtable dispatch |

### Layer 3: Yo-kai Watch 2 Game Logic (`src/game/`)
Game-specific state machines (`ywCLoopMain`, `ywCLoopRPG`, `ywCLoopBattle`, `ywCLoopMenu*`, `ywCLoopOrgeTime`), Yo-kai entities (`C$obj_yokai`), quests, watch map, and UI logic.

| Didactic Level | Virtual Address | Symbol | Module | Size | Status | Description |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **L1: Leaf Stub** | `0x0017656C` | `func_0017656C` | `game/core` | 4 B | 🟢 Matched | Empty void stub (`bx lr`) |
| **L1: Virtual Stub** | `0x0010CEE8` | `func_0010CEE8` | `game/loops` | 8 B | ⏳ Candidate | `ywCLoopRPG` virtual method (returns `0`, table `0x001074A0`) |
| **L1: Virtual Stub** | `0x0010CFF4` | `func_0010CFF4` | `game/loops` | 8 B | ⏳ Candidate | `ywCLoopMain` virtual method (returns `0`, table `0x00107494`) |
| **L2: RTTI Getter** | `0x0010CEF0` | `func_0010CEF0` | `game/loops` | 12 B | ⏳ Candidate | `ywCLoopRPG::GetClassName` (`"ywCLoopRPG"` at `0x0086048C`) |
| **L2: RTTI Getter** | `0x0010CFFC` | `func_0010CFFC` | `game/loops` | 12 B | ⏳ Candidate | `ywCLoopMain::GetClassName` (`"ywCLoopMain"` at `0x00860497`) |
| **L2: Pointer Getter** | `0x0010C894` | `func_0010C894` | `game/loops` | 12 B | 🟢 Matched | Game loop state pointer getter (`0x0086C8CC`) |
| **L2: Pointer Getter** | `0x00171C78` | `func_00171C78` | `game/core` | 12 B | 🟢 Matched | Global `.bss` state pointer getter (`0x0091B7B8`) |
| **L3: Struct Init** | `0x0011054C` | `func_0011054C` | `game/loops` | 24 B | 🟢 Matched | Struct header reset (zeros 8 bytes, sets byte 0 to `0xFF`) |

---

## Repository layout

```text
src/
├── ctr/         Layer 1: Nintendo CTR-SDK & ARM Runtime (crt/, svc/, nn/os/, nn/ndm/, nn/nex/)
├── engine/      Layer 2: Level-5 Engine (lfw/, lxp/, gds/, core/)
└── game/        Layer 3: Yo-kai Watch 2 Game Logic (loops/, core/)
include/
├── ctr/         CTR-SDK headers (svc.h, os.h)
├── engine/      Level-5 Framework & engine headers (lfw.h)
└── game/        Yo-kai Watch 2 game headers (loops.h)
config/          ExHeader memory map (memory_map.json), manifests (functions.csv, functions_classified.csv)
scratches/       Isolated WIP function matching scratchpads organized by layer
tools/           ROM extraction, disassembly, 3-layer classification, and verification scripts
notes/           Didactic learning roadmap (ROADMAP.md) and per-function reverse-engineering notes
```

---

## Building / verifying

You need your own copy of the game plus the toolchain (see `docs/` for setup).

### 1. Extracting the game code

Place your legally obtained retail ROM (`.3ds`, `.cxi` or `.cia`) inside the project root:

```bash
python tools/extract_rom.py --rom 00040000001B2900_v00.3ds
```

This extracts and decompresses the executable to `extracted/code.raw.bin` and verifies its reference hash:
- SHA-256: `b536dfce0a7138f2d5691532604d782b1ea3e20731120cc662baee118c370547`

### 2. Disassembling a function for decomp.me

Generate clean assembly ready for [decomp.me](https://decomp.me/):

```bash
python3 tools/dump_asm.py 0x10B6E4 280            # Formatted relative offsets
python3 tools/dump_asm.py 0x10B6E4 280 --plain    # Raw instructions only
```

Or inspect directly with GNU binutils:

```bash
arm-none-eabi-objdump -b binary -m arm -D --adjust-vma=0x00100000 \
    --start-address=0x10B6D0 --stop-address=0x10B6E8 \
    extracted/code.raw.bin
```

### 3. Compiling and verifying

```bash
make check            # Compiles and byte-compares candidate functions
```

A green `>>> MATCH <<<` means your C reproduces the original binary exactly, instruction for instruction.

---

## Credits

- **Level-5 Inc.**: Developers of *Yo-kai Watch 2*.
- **Yokimitsuro ([khdays-decomp](https://github.com/Yokimitsuro/khdays-decomp))**: Decompilation guidance, repository design, and the progress reporting methodology that inspired this structure.
- **Jack Price-Burns ([Decomp Academy](https://decomp-academy.dev/))**: Interactive matching decompilation foundations.
- **[pyctr](https://github.com/ihaveamac/pyctr)**: 3DS container parsing and LZSS decompression tooling.
- **[decomp.dev](https://decomp.dev/)**: The community driving modern video game matching decompilation.
