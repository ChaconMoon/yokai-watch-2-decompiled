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

Initial exploratory passes on the EU (`00040000001B2900`) ARM11 decompressed CXI binary image (`code.raw.bin`, 7,737,344 bytes; executable `.text`: 6,238,892 bytes, base `0x00100000`).

The current objective is establishing a reproducible verification pipeline, matching the first batch of atomic leaf functions, and classifying library vs game engine routines.

Progress is split into categories so that assembly is never counted as C decompilation:

<!-- PROGRESS_STATS_START -->

| Category | Count | Meaning |
| :--- | :---: | :--- |
| **Decompiled C/C++ (Decomp Mode)** | **72** / 18,225 (0.40%) | Real C/C++ verified byte-exact (1,392 B / 0.0223% of `.text` · 0.0180% of binary) |
| **Assembly Stubs (`.s` extracted)** | **393** / 18,225 (2.16%) | Split stubs for building & progressive replacement (63,840 B / 1.0233% of `.text` · 0.8251% of binary) |
| **Build Match Mode (Binary Code Coverage)** | **465** / 18,225 (2.55%) | Combined C/C++ & assembly matching `code.raw.bin` (65,232 B / 1.0456% of `.text` · 0.8431% of binary) |
| **Layer 1: Nintendo CTR-SDK (`src/ctr/`)** | **61** C matched + **390** stubs | CRT startup, `svc`, `nn::os`, `nn::y2r`, `nn::nex`, `nn::dsp` |
| **Layer 2: Level-5 Engine (`src/engine/`)** | **7** C matched + **3** stubs | `lfw` base classes, `lfwCLoop`, `lxp`, `gds` |
| **Layer 3: Yo-kai Watch 2 Game (`src/game/`)** | **4** C matched + **0** stubs | `ywCLoop*` state machines, battle, RPG entities |
| **Cataloged in Manifest** | **468** / 18,225 | Functions actively tracked across `src/` and `scratches/` |
| **Executable Size (`.text`)** | 6,238,892 B | Exact code segment size from NCCH ExHeader (EU `00040000001B2900`) |
| **Full Binary Image (`code.raw.bin`)** | 7,737,344 B | Decompressed CXI `.code` image (`.text` + `.rodata` + `.data`) |
| **Architecture** | ARM11 MPCore (ARMv6K) | 32-bit Little Endian, VMA `0x00100000` |
| **Compiler** | ARMCC / RVCT 4.0 b821 | CTR-SDK 1.2.7 (`1.2.7.f-NINTENDO-CTR-SDK-v1`) |

<!-- PROGRESS_STATS_END -->

---

### Progress reporting policy

Progress is presented under two complementary perspectives:
- **Decomp Mode (C/C++ Matching):** Measures strictly genuine, hand-crafted or AI-assisted C/C++ implementations verified bit-for-bit against the original game code.
- **Build Match Mode (Binary Code Coverage):** Measures total coverage of the executable (`.text`) and binary image (`code.raw.bin`), combining decompiled C/C++ and verified assembly stubs (`.s`) under the "Split & Replace" methodology. Assembly stubs are never counted as C decompilation. Scratches and unverified prototypes remain staged until verified.

---

## Target Candidates & Current Manifest

<!-- MANIFEST_TABLE_START -->

| Virtual Address | Symbol / Name | Layer / Module | Size | Level | Status | Description / Notes |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `0x00100000` | `func_00100000` | `ctr/crt` | 4 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00100004` | `func_00100004` | `ctr/crt` | 4 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00100008` | `func_00100008` | `ctr/crt` | 4 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x0010000C` | `func_0010000C` | `ctr/crt` | 4 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00100010` | `func_00100010` | `ctr/crt` | 4 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00100014` | `func_00100014` | `ctr/crt` | 4 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00100018` | `func_00100018` | `ctr/crt` | 4 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x0010001C` | `func_0010001C` | `ctr/crt` | 16 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (3 subcalls) |
| `0x00100024` | `clear_bss` | `ctr/crt` | 36 B | `2_control_flow` | ⚪ ASM Stub (Verified) | CRT startup zeroing loop for .bss section (0x00860934 - 0x0091B9BC) |
| `0x00100048` | `func_00100048` | `ctr/crt` | 18 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x0010005A` | `func_0010005A` | `ctr/crt` | 36 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00100080` | `func_00100080` | `ctr/crt` | 112 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x001000F8` | `func_001000F8` | `ctr/crt` | 8 B | `1_trivial` | ⚪ ASM Stub (Verified) | Constant return stub or leaf identity |
| `0x00100100` | `func_00100100` | `ctr/crt` | 40 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x0010012C` | `func_0010012C` | `ctr/crt` | 44 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00100158` | `func_00100158` | `ctr/crt` | 78 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (3 subcalls) |
| `0x001001A6` | `func_001001A6` | `ctr/crt` | 116 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x0010021C` | `thunk_FUN_00100224` | `ctr/crt` | 8 B | `1_trivial` | ⚪ ASM Stub (Verified) | Constant return stub or leaf identity |
| `0x00100224` | `func_00100224` | `ctr/crt` | 18 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x0010026E` | `func_0010026E` | `ctr/crt` | 66 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x001002C4` | `func_001002C4` | `ctr/crt` | 34 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x001002E8` | `thunk_FUN_001002f0` | `ctr/crt` | 8 B | `1_trivial` | ⚪ ASM Stub (Verified) | Constant return stub or leaf identity |
| `0x001002F0` | `func_001002F0` | `ctr/crt` | 18 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x00100302` | `func_00100302` | `ctr/crt` | 24 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x00100324` | `func_00100324` | `ctr/crt` | 22 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x0010063C` | `func_0010063C` | `ctr/crt` | 22 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x0010066A` | `func_0010066A` | `ctr/crt` | 82 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (3 subcalls) |
| `0x00100738` | `func_00100738` | `ctr/crt` | 34 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x0010075A` | `func_0010075A` | `ctr/crt` | 24 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00100784` | `func_00100784` | `ctr/crt` | 114 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (10 calls) |
| `0x0010080C` | `func_0010080C` | `ctr/crt` | 16 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00100850` | `func_00100850` | `ctr/crt` | 182 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (6 calls) |
| `0x00100A24` | `thunk_FUN_00100a36` | `ctr/crt` | 8 B | `1_trivial` | ⚪ ASM Stub (Verified) | Constant return stub or leaf identity |
| `0x00100A36` | `func_00100A36` | `ctr/crt` | 12 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00100A44` | `func_00100A44` | `ctr/crt` | 330 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (11 calls) |
| `0x00100BB4` | `func_00100BB4` | `ctr/crt` | 36 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00100BD8` | `func_00100BD8` | `ctr/crt` | 54 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00100C18` | `func_00100C18` | `ctr/crt` | 24 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00100C30` | `func_00100C30` | `ctr/crt` | 50 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00100C74` | `func_00100C74` | `ctr/crt` | 28 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00100CDC` | `func_00100CDC` | `ctr/crt` | 330 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (6 calls) |
| `0x00100E26` | `func_00100E26` | `ctr/crt` | 330 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x00100F70` | `func_00100F70` | `ctr/crt` | 232 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x00101058` | `func_00101058` | `ctr/crt` | 288 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (3 subcalls) |
| `0x00101178` | `func_00101178` | `ctr/crt` | 232 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00101260` | `func_00101260` | `ctr/crt` | 208 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x00101330` | `func_00101330` | `ctr/crt` | 50 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x001013EC` | `func_001013EC` | `ctr/crt` | 532 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (8 calls) |
| `0x001018D8` | `func_001018D8` | `ctr/crt` | 906 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (9 calls) |
| `0x00101C70` | `func_00101C70` | `ctr/crt` | 8 B | `1_trivial` | ⚪ ASM Stub (Verified) | Constant return stub or leaf identity |
| `0x00101C78` | `func_00101C78` | `ctr/crt` | 8 B | `1_trivial` | ⚪ ASM Stub (Verified) | Constant return stub or leaf identity |
| `0x00101C80` | `func_00101C80` | `ctr/crt` | 74 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00101CE4` | `func_00101CE4` | `ctr/crt` | 18 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x00101CF6` | `func_00101CF6` | `ctr/crt` | 14 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00102180` | `func_00102180` | `ctr/crt` | 18 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00102198` | `func_00102198` | `ctr/crt` | 104 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x0010223C` | `func_0010223C` | `ctr/crt` | 372 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (11 calls) |
| `0x001023D2` | `func_001023D2` | `ctr/crt` | 30 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x001023F0` | `func_001023F0` | `ctr/crt` | 54 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (3 subcalls) |
| `0x0010242C` | `func_0010242C` | `ctr/crt` | 50 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00102464` | `func_00102464` | `ctr/crt` | 68 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x001024AC` | `func_001024AC` | `ctr/crt` | 54 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (3 subcalls) |
| `0x001024E8` | `func_001024E8` | `ctr/crt` | 72 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (3 subcalls) |
| `0x00102534` | `func_00102534` | `ctr/crt` | 140 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (3 subcalls) |
| `0x001025C4` | `func_001025C4` | `ctr/crt` | 86 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x0010261A` | `func_0010261A` | `ctr/crt` | 26 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00102634` | `func_00102634` | `ctr/crt` | 108 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (3 subcalls) |
| `0x001026A4` | `func_001026A4` | `ctr/crt` | 8 B | `1_trivial` | ⚪ ASM Stub (Verified) | Constant return stub or leaf identity |
| `0x001026AC` | `func_001026AC` | `ctr/crt` | 116 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x00102720` | `func_00102720` | `ctr/crt` | 80 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x00102770` | `func_00102770` | `ctr/crt` | 534 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (21 calls) |
| `0x00102986` | `func_00102986` | `ctr/crt` | 138 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (6 calls) |
| `0x00102A10` | `func_00102A10` | `ctr/crt` | 40 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00102A40` | `func_00102A40` | `ctr/crt` | 18 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x00102A5C` | `func_00102A5C` | `ctr/crt` | 28 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00102A78` | `func_00102A78` | `ctr/crt` | 10 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x00102A82` | `func_00102A82` | `ctr/crt` | 10 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00102A8C` | `func_00102A8C` | `ctr/crt` | 28 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00102AAE` | `func_00102AAE` | `ctr/crt` | 26 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00102AC4` | `func_00102AC4` | `ctr/crt` | 40 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x00102AEC` | `func_00102AEC` | `ctr/crt` | 44 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (5 calls) |
| `0x00102B18` | `func_00102B18` | `ctr/crt` | 126 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (5 calls) |
| `0x00102B98` | `func_00102B98` | `ctr/crt` | 26 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00102BBC` | `func_00102BBC` | `ctr/crt` | 12 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00102BC8` | `func_00102BC8` | `ctr/crt` | 168 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00102C70` | `func_00102C70` | `ctr/crt` | 124 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00102CEC` | `func_00102CEC` | `ctr/crt` | 168 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00102D94` | `func_00102D94` | `ctr/crt` | 8 B | `1_trivial` | ⚪ ASM Stub (Verified) | Constant return stub or leaf identity |
| `0x00102ED8` | `func_00102ED8` | `ctr/crt` | 12 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00102EE4` | `func_00102EE4` | `ctr/crt` | 112 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00102F54` | `func_00102F54` | `ctr/crt` | 34 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00102F7C` | `func_00102F7C` | `ctr/crt` | 216 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (3 subcalls) |
| `0x00103054` | `func_00103054` | `ctr/crt` | 200 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (3 subcalls) |
| `0x00103162` | `func_00103162` | `ctr/crt` | 22 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00103178` | `func_00103178` | `ctr/crt` | 18 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00103254` | `func_00103254` | `ctr/crt` | 48 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00103390` | `func_00103390` | `ctr/crt` | 10 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x001033AC` | `func_001033AC` | `ctr/crt` | 10 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x001033BA` | `func_001033BA` | `ctr/crt` | 10 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x0010342A` | `func_0010342A` | `ctr/crt` | 12 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00103454` | `func_00103454` | `ctr/crt` | 184 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x0010351C` | `func_0010351C` | `ctr/crt` | 310 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x001037F0` | `func_001037F0` | `ctr/crt` | 738 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (17 calls) |
| `0x00103BBC` | `func_00103BBC` | `ctr/crt` | 14 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00103BCC` | `func_00103BCC` | `ctr/crt` | 12 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00103BDC` | `func_00103BDC` | `ctr/crt` | 8 B | `1_trivial` | ⚪ ASM Stub (Verified) | Constant return stub or leaf identity |
| `0x00103BF0` | `func_00103BF0` | `ctr/crt` | 106 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00103C60` | `func_00103C60` | `ctr/crt` | 152 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x001040D4` | `func_001040D4` | `ctr/crt` | 110 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x001043E8` | `func_001043E8` | `ctr/crt` | 110 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x001045D2` | `func_001045D2` | `ctr/crt` | 22 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x001045FA` | `func_001045FA` | `ctr/crt` | 12 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x0010463E` | `func_0010463E` | `ctr/crt` | 22 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00104666` | `func_00104666` | `ctr/crt` | 18 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x001046AC` | `func_001046AC` | `ctr/crt` | 8 B | `1_trivial` | ⚪ ASM Stub (Verified) | Constant return stub or leaf identity |
| `0x001046B4` | `func_001046B4` | `ctr/crt` | 288 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (30 calls) |
| `0x00104778` | `svcExitProcess` | `ctr/svc` | 8 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x03) |
| `0x00104780` | `func_00104780` | `ctr/nn_os` | 96 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (12 calls) |
| `0x001047E0` | `func_001047E0` | `ctr/nn_os` | 44 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x00104814` | `func_00104814` | `ctr/nn_os` | 76 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (6 calls) |
| `0x00104868` | `func_00104868` | `ctr/nn_os` | 32 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (8 calls) |
| `0x00104888` | `func_00104888` | `ctr/nn_os` | 44 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x001048B4` | `func_001048B4` | `ctr/nn_os` | 104 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (12 calls) |
| `0x00104924` | `func_00104924` | `ctr/nn_os` | 464 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (44 calls) |
| `0x00104B1C` | `func_00104B1C` | `ctr/nn_os` | 160 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (14 calls) |
| `0x00104BC0` | `func_00104BC0` | `ctr/nn_os` | 332 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (36 calls) |
| `0x00104D18` | `func_00104D18` | `ctr/nn_os` | 16 B | `2_accessor` | 🟢 Matched (C/C++) | nn::os startup global 8-bit flag setter (0x00814E54) |
| `0x00104D28` | `func_00104D28` | `ctr/nn_os` | 32 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00104D4C` | `func_00104D4C` | `ctr/nn_os` | 1992 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (127 calls) |
| `0x00105598` | `func_00105598` | `ctr/nn_os` | 2040 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (91 calls) |
| `0x001060B8` | `func_001060B8` | `ctr/nn_os` | 396 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (30 calls, vtable) |
| `0x00106244` | `func_00106244` | `ctr/nn_os` | 172 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (19 calls) |
| `0x00106300` | `func_00106300` | `ctr/nn_os` | 40 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00106328` | `func_00106328` | `ctr/nn_os` | 80 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x0010637C` | `func_0010637C` | `ctr/nn_os` | 52 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x001063B8` | `func_001063B8` | `ctr/nn_os` | 56 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x001063F4` | `func_001063F4` | `ctr/nn_os` | 16 B | `2_accessor` | 🟢 Matched (C/C++) | CTR OS SystemConfig block field reader (0x1FF80000 + 0x40) |
| `0x00106404` | `func_00106404` | `ctr/nn_os` | 80 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00106458` | `func_00106458` | `ctr/nn_os` | 184 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (9 calls) |
| `0x00106504` | `func_00106504` | `ctr/nn_os` | 16 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x00106518` | `func_00106518` | `ctr/nn_os` | 16 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x0010652C` | `func_0010652C` | `ctr/nn_os` | 48 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (13 calls) |
| `0x0010655C` | `func_0010655C` | `ctr/nn_os` | 20 B | `2_accessor` | 🟢 Matched (C/C++) | nn::os::detail TLS pointer store to global offset via literal pool (0x00815DE0) |
| `0x00106570` | `func_00106570` | `ctr/nn_os` | 296 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (18 calls) |
| `0x00106588` | `func_00106588` | `ctr/nn_os` | 120 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (13 calls) |
| `0x001065CC` | `func_001065CC` | `ctr/nn_os` | 172 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (6 calls) |
| `0x00106694` | `func_00106694` | `ctr/nn_os` | 140 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x00106724` | `func_00106724` | `ctr/nn_os` | 52 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00106760` | `func_00106760` | `ctr/nn_os` | 200 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (13 calls) |
| `0x0010678C` | `func_0010678C` | `ctr/nn_os` | 16 B | `2_accessor` | 🟢 Matched (C/C++) | nn::os startup global signed byte reader via literal pool (0x00814E00) |
| `0x0010679C` | `func_0010679C` | `ctr/nn_os` | 348 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (42 calls) |
| `0x00106900` | `func_00106900` | `ctr/nn_os` | 52 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x0010693C` | `func_0010693C` | `ctr/nn_os` | 168 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (30 calls) |
| `0x001069E8` | `func_001069E8` | `ctr/nn_os` | 1704 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (122 calls, vtable) |
| `0x00106B64` | `func_00106B64` | `ctr/nn_os` | 14272 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (806 calls, vtable) |
| `0x0010AA84` | `func_0010AA84` | `ctr/svc` | 36 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x01 ControlMemory) |
| `0x0010AAA8` | `svcCreateEvent` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x21) |
| `0x0010AAC0` | `svcDuplicateHandle` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x38) |
| `0x0010B6D0` | `func_0010B6D0` | `engine/lfw` | 8 B | `1_leaf_stub` | 🟢 Matched (C/C++) | lfwCLoopEmpty virtual method (returns constant 0, table 0x00107488) |
| `0x0010B6D8` | `func_0010B6D8` | `engine/lfw` | 12 B | `2_accessor` | 🟢 Matched (C/C++) | lfwCLoopEmpty::GetClassName getter via literal pool (0x008602F8) |
| `0x0010B6E4` | `func_0010B6E4` | `engine/lfw` | 280 B | `4_cpp_vtable` | 🟡 In Review | lfwCLoop C++ class method (partially decompiled, ~82% match in decomp.me) |
| `0x0010B7FC` | `func_0010B7FC` | `engine/lfw` | 140 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | lfwCLoop hardware profile switch dispatch table |
| `0x0010B888` | `func_0010B888` | `engine/lfw` | 48 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | lfwCLoop state and channel reset sequence |
| `0x0010B8B8` | `func_0010B8B8` | `engine/lfw` | 156 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | lfwCLoop UTF-8 string stream decoding and registration buffer |
| `0x0010C894` | `func_0010C894` | `game/loops` | 12 B | `2_accessor` | 🟢 Matched (C/C++) | Game loop subsystem pointer getter via literal pool (0x0086C8CC) |
| `0x0011054C` | `func_0011054C` | `game/loops` | 24 B | `3_arithmetic_logic` | 🟢 Matched (C/C++) | Struct header reset (zeros 8 bytes, sets byte 0 to 0xFF) |
| `0x001128F8` | `func_001128F8` | `ctr/nn_y2r` | 148 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Y2R virtual dispatch for image conversion parameters |
| `0x0011298C` | `func_0011298C` | `ctr/nn_y2r` | 284 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Y2R image transformation and coordinate scaling sequence |
| `0x00112AA8` | `func_00112AA8` | `ctr/nn_y2r` | 96 B | `4_complex_leaf` | 🟢 Matched (C/C++) | Y2R channel state structure field zero-initialization |
| `0x00112B08` | `func_00112B08` | `ctr/nn_y2r` | 124 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Y2R channel cleanup reset invoking func_00113F80 and dispatch |
| `0x00112B84` | `func_00112B84` | `ctr/nn_y2r` | 236 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Y2R format handler and .xf stream processor |
| `0x00112CB0` | `func_00112CB0` | `ctr/nn_y2r` | 32 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Y2R slot configuration invoking func_0014A070 |
| `0x00112CD0` | `func_00112CD0` | `ctr/nn_y2r` | 12 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Y2R indexed slot calculation falling through to func_00112CDC |
| `0x00112CDC` | `func_00112CDC` | `ctr/nn_y2r` | 44 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Y2R slot configuration type 8 with NULL check invoking func_0014A070 |
| `0x00112D58` | `func_00112D58` | `ctr/nn_y2r` | 36 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Y2R slot configuration type 2 invoking func_0014A070 |
| `0x00112D8C` | `func_00112D8C` | `ctr/nn_y2r` | 20 B | `6_moderate_caller` | 🟢 Matched (C/C++) | Method chaining wrapper invoking func_0014A06C |
| `0x00112DA0` | `func_00112DA0` | `ctr/nn_y2r` | 192 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Y2R image conversion context setup and dispatch |
| `0x00112E60` | `func_00112E60` | `ctr/nn_y2r` | 16 B | `2_accessor` | 🟢 Matched (C/C++) | Y2R struct offset 8648 u16 reader |
| `0x00112E70` | `func_00112E70` | `ctr/nn_y2r` | 88 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Y2R format query and dimension retrieval invoking func_00116CB4 |
| `0x00112EC8` | `func_00112EC8` | `ctr/nn_y2r` | 28 B | `6_moderate_caller` | 🟢 Matched (C/C++) | Y2R mutex lock/unlock sequence on unk_00867CF8 |
| `0x00112EE4` | `func_00112EE4` | `ctr/nn_y2r` | 16 B | `6_moderate_caller` | 🟢 Matched (C/C++) | Y2R stack buffer query invoking func_002FDAC4 |
| `0x00112F58` | `func_00112F58` | `ctr/nn_y2r` | 120 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Y2R buffer structure initialization and alignment registration |
| `0x00112FF0` | `svcCreateTimer` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x2D) |
| `0x00113008` | `func_00113008` | `ctr/svc` | 36 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x08 CreateThread) |
| `0x001130CC` | `func_001130CC` | `ctr/nn_y2r` | 396 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Y2R VFP register context saving and parameter batch processing |
| `0x00113650` | `func_00113650` | `ctr/nn_y2r` | 52 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Y2R global flag 0x008150AC disable toggle |
| `0x00113684` | `func_00113684` | `ctr/nn_y2r` | 56 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Y2R global flag 0x008150AC enable toggle |
| `0x001136BC` | `func_001136BC` | `ctr/nn_y2r` | 68 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Y2R initialization check and configuration helper |
| `0x00113700` | `func_00113700` | `ctr/nn_y2r` | 64 B | `7_complex_caller` | 🟢 Matched (C/C++) | Y2R buffer deallocation sequence on unk_00814F28 |
| `0x00113740` | `func_00113740` | `ctr/nn_y2r` | 128 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Y2R buffer allocation and initialization on unk_00814F28 |
| `0x001137C0` | `func_001137C0` | `ctr/nn_y2r` | 20 B | `6_moderate_caller` | 🟢 Matched (C/C++) | Helper invoking func_00136154(&unk_0086A0A4) |
| `0x001137D8` | `func_001137D8` | `ctr/nn_y2r` | 48 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Y2R buffer validation sequence with unk_0086A0A4 |
| `0x00113808` | `func_00113808` | `ctr/nn_y2r` | 112 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Y2R state update and event clearance sequence (svc 0x19) |
| `0x00113878` | `func_00113878` | `ctr/nn_y2r` | 88 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Y2R microsecond conversion and dispatch invoking func_001468F0 |
| `0x001138D0` | `func_001138D0` | `ctr/nn_y2r` | 44 B | `7_complex_caller` | 🟢 Matched (C/C++) | Y2R error reporting thunk invoking func_0011F51C |
| `0x001138FC` | `func_001138FC` | `ctr/nn_y2r` | 392 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Y2R subsystem complete deinitialization and channel shutdown sequence |
| `0x00113A84` | `func_00113A84` | `ctr/nn_y2r` | 1148 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Y2R subsystem initialization sequence and hardware channel configuration |
| `0x00113F00` | `func_00113F00` | `ctr/nn_y2r` | 24 B | `7_complex_caller` | 🟢 Matched (C/C++) | Y2R initialization sequence invoking func_0011F46C func_0011FA98 |
| `0x00113F18` | `func_00113F18` | `ctr/nn_y2r` | 52 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Y2R finalize sequence invoking func_0011FABC func_0011FCFC |
| `0x00113F4C` | `func_00113F4C` | `ctr/nn_y2r` | 12 B | `7_complex_caller` | 🟢 Matched (C/C++) | Y2R tail-call thunk to func_0011FDAC with unk_008661EC |
| `0x00113F58` | `func_00113F58` | `ctr/nn_y2r` | 20 B | `2_accessor` | 🟢 Matched (C/C++) | Y2R global bit 3 flag getter via literal pool (0x008661EC) |
| `0x00113F70` | `func_00113F70` | `ctr/nn_y2r` | 12 B | `2_accessor` | 🟢 Matched (C/C++) | Y2R global float field getter via literal pool (0x00815090) |
| `0x00113F80` | `func_00113F80` | `ctr/nn_y2r` | 152 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Y2R hardware mode dispatch and channel reset sequence |
| `0x00127170` | `func_00127170` | `ctr/nn_os` | 152 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (3 subcalls) |
| `0x00127200` | `func_00127200` | `ctr/nn_os` | 204 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (12 calls) |
| `0x001272E8` | `func_001272E8` | `ctr/nn_os` | 220 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x001273CC` | `func_001273CC` | `ctr/nn_os` | 156 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x0012746C` | `func_0012746C` | `ctr/nn_os` | 40 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x001274A0` | `func_001274A0` | `ctr/nn_os` | 24 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::os atomic spinlock acquire loop (ldrex/strex synchronization) |
| `0x001274B8` | `func_001274B8` | `ctr/nn_os` | 92 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x00127520` | `func_00127520` | `ctr/nn_os` | 12 B | `2_accessor` | 🟢 Matched (C/C++) | CTR-SDK .text size / limit getter via literal pool (0x005F32AC) |
| `0x0012752C` | `func_0012752C` | `ctr/nn_os` | 156 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x001275D8` | `func_001275D8` | `ctr/nn_os` | 12 B | `2_accessor` | 🟢 Matched (C/C++) | CTR-SDK .text base VMA getter via literal pool (0x00100000) |
| `0x001275E4` | `func_001275E4` | `ctr/nn_os` | 36 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x0012760C` | `func_0012760C` | `ctr/nn_os` | 40 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x00127638` | `func_00127638` | `ctr/nn_os` | 124 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls, vtable) |
| `0x001276B4` | `func_001276B4` | `ctr/nn_os` | 96 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00127718` | `func_00127718` | `ctr/nn_os` | 372 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x0012788C` | `func_0012788C` | `ctr/nn_os` | 16 B | `2_accessor` | 🟢 Matched (C/C++) | nn::os global flag setter via literal pool (0x00828EEC) |
| `0x0012789C` | `func_0012789C` | `ctr/nn_os` | 184 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00127958` | `func_00127958` | `ctr/nn_os` | 52 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x00127994` | `func_00127994` | `ctr/nn_os` | 56 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x001279CC` | `func_001279CC` | `ctr/nn_os` | 40 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x00127ABC` | `func_00127ABC` | `ctr/nn_os` | 104 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00127B38` | `func_00127B38` | `ctr/nn_os` | 104 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00127BB8` | `func_00127BB8` | `ctr/nn_os` | 72 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00127C24` | `func_00127C24` | `ctr/nn_os` | 64 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x00127C6C` | `func_00127C6C` | `ctr/nn_os` | 40 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x00127C9C` | `func_00127C9C` | `ctr/nn_os` | 264 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (18 calls) |
| `0x00127DB8` | `func_00127DB8` | `ctr/nn_os` | 100 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (8 calls) |
| `0x00127E1C` | `func_00127E1C` | `ctr/nn_os` | 140 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00127EB0` | `func_00127EB0` | `ctr/nn_os` | 48 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00127EE0` | `func_00127EE0` | `ctr/nn_ndm` | 12 B | `2_accessor` | 🟢 Matched (C/C++) | nn::ndm global state offset reader via literal pool (0x00865F18) |
| `0x00127EEC` | `func_00127EEC` | `ctr/nn_ndm` | 12 B | `2_accessor` | 🟢 Matched (C/C++) | nn::ndm global state pointer getter via literal pool (0x00865F10) |
| `0x00127EF8` | `func_00127EF8` | `ctr/nn_os` | 52 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00127F2C` | `func_00127F2C` | `ctr/nn_os` | 124 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (12 calls) |
| `0x00127FB8` | `func_00127FB8` | `ctr/nn_os` | 80 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (6 calls) |
| `0x0012806C` | `func_0012806C` | `ctr/nn_os` | 224 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (13 calls) |
| `0x001280A8` | `func_001280A8` | `ctr/nn_ndm` | 24 B | `3_arithmetic_logic` | 🟢 Matched (C/C++) | nn::ndm bounds-checked struct array element indexer (stride 8, offset +0x0C) |
| `0x001280C0` | `func_001280C0` | `ctr/nn_os` | 36 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x001280EC` | `func_001280EC` | `ctr/nn_os` | 108 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (10 calls) |
| `0x00128158` | `func_00128158` | `ctr/nn_os` | 128 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (12 calls) |
| `0x001281D8` | `func_001281D8` | `ctr/nn_os` | 164 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (16 calls) |
| `0x0012827C` | `func_0012827C` | `ctr/nn_os` | 96 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (10 calls) |
| `0x001282DC` | `func_001282DC` | `ctr/nn_os` | 140 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (14 calls) |
| `0x00128368` | `func_00128368` | `ctr/nn_os` | 32 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x0012838C` | `func_0012838C` | `ctr/nn_os` | 124 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (16 calls) |
| `0x001283BC` | `func_001283BC` | `ctr/nn_os` | 96 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (12 calls) |
| `0x00128424` | `func_00128424` | `ctr/nn_os` | 80 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (12 calls) |
| `0x001284AC` | `func_001284AC` | `ctr/nn_os` | 52 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (3 subcalls) |
| `0x001284E4` | `func_001284E4` | `ctr/nn_applet` | 28 B | `2_accessor` | 🟢 Matched (C/C++) | nn::applet::CTR::IsApplication attribute check via literal pool (0x00814E00) |
| `0x00128544` | `func_00128544` | `ctr/nn_applet` | 20 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | nn::applet::detail::SetCallback2C |
| `0x00128558` | `func_00128558` | `ctr/nn_applet` | 16 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | nn::applet::detail::SetState10 |
| `0x00128568` | `func_00128568` | `ctr/nn_applet` | 16 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | nn::applet::detail::GetState0C |
| `0x00128578` | `func_00128578` | `ctr/nn_applet` | 16 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | nn::applet::detail::SetState0C |
| `0x00128588` | `func_00128588` | `ctr/nn_applet` | 20 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | nn::applet::detail::SetCallback20 |
| `0x0012859C` | `func_0012859C` | `ctr/nn_applet` | 20 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | nn::applet::detail::SetState08_1 |
| `0x001285B0` | `func_001285B0` | `ctr/nn_applet` | 16 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | nn::applet::detail::GetState08 |
| `0x001285C0` | `func_001285C0` | `ctr/nn_applet` | 20 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | nn::applet::detail::SetCallback24 |
| `0x001285D4` | `func_001285D4` | `ctr/nn_applet` | 20 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | nn::applet::detail::SetState08_0 |
| `0x001285E8` | `func_001285E8` | `ctr/nn_applet` | 16 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | nn::applet::detail::GetState0B |
| `0x0012CB00` | `func_0012CB00` | `engine/lxp` | 12 B | `2_accessor` | 🟢 Matched (C/C++) | Level-5 engine global singleton getter via literal pool (0x00868A9C) |
| `0x0012F190` | `svcExitThread` | `ctr/svc` | 8 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x09) |
| `0x0012F198` | `svcCreateResourceLimit` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x35) |
| `0x0012FEC0` | `func_0012FEC0` | `engine/lxp` | 8 B | `1_leaf_stub` | 🟢 Matched (C/C++) | lxpCMemory boolean true stub (returns constant 1) |
| `0x00130018` | `func_00130018` | `engine/lxp` | 8 B | `1_leaf_stub` | 🟢 Matched (C/C++) | lxpCMemory virtual boolean true stub (returns constant 1) |
| `0x001300B0` | `func_001300B0` | `engine/lxp` | 12 B | `2_accessor` | 🟢 Matched (C/C++) | lxpCMemory manager pointer getter via literal pool (0x00868F10) |
| `0x00136154` | `func_00136154` | `ctr/nn_dsp` | 176 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (27 calls, vtable) |
| `0x00136204` | `func_00136204` | `ctr/nn_dsp` | 136 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (8 calls) |
| `0x0013628C` | `thunk_FUN_0013457c` | `ctr/nn_dsp` | 4 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x00136290` | `func_00136290` | `ctr/nn_dsp` | 136 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (11 calls) |
| `0x00136318` | `func_00136318` | `ctr/nn_dsp` | 20 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00136330` | `func_00136330` | `ctr/nn_dsp` | 60 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x0013636C` | `func_0013636C` | `ctr/nn_dsp` | 32 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x0013638C` | `func_0013638C` | `ctr/nn_dsp` | 144 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (5 calls, vtable) |
| `0x00136420` | `func_00136420` | `ctr/nn_dsp` | 24 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00136438` | `func_00136438` | `ctr/nn_dsp` | 264 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (5 calls) |
| `0x00136594` | `func_00136594` | `ctr/nn_dsp` | 80 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm with loop |
| `0x001365E4` | `func_001365E4` | `ctr/nn_dsp` | 180 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x0013669C` | `func_0013669C` | `ctr/nn_dsp` | 224 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00136780` | `func_00136780` | `ctr/nn_dsp` | 16 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00136790` | `func_00136790` | `ctr/nn_dsp` | 108 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00136804` | `func_00136804` | `ctr/nn_dsp` | 48 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00136838` | `func_00136838` | `ctr/nn_dsp` | 216 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x00136920` | `func_00136920` | `ctr/nn_dsp` | 52 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (3 subcalls) |
| `0x00136958` | `func_00136958` | `ctr/nn_dsp` | 48 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (3 subcalls) |
| `0x0013698C` | `func_0013698C` | `ctr/nn_dsp` | 952 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (14 calls) |
| `0x00136D58` | `func_00136D58` | `ctr/nn_dsp` | 360 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (30 calls, vtable) |
| `0x00136EC4` | `func_00136EC4` | `ctr/nn_dsp` | 256 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (18 calls, vtable) |
| `0x00136FC4` | `func_00136FC4` | `ctr/nn_dsp` | 60 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00137054` | `func_00137054` | `ctr/nn_dsp` | 12 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00137064` | `func_00137064` | `ctr/nn_dsp` | 156 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (8 calls) |
| `0x00137114` | `func_00137114` | `ctr/nn_dsp` | 60 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00137158` | `func_00137158` | `ctr/nn_dsp` | 84 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (8 calls) |
| `0x001371B4` | `func_001371B4` | `ctr/nn_dsp` | 32 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x001371D4` | `func_001371D4` | `ctr/nn_dsp` | 84 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (2 calls, vtable) |
| `0x0013722C` | `func_0013722C` | `ctr/nn_dsp` | 184 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (8 calls) |
| `0x001372F8` | `func_001372F8` | `ctr/nn_dsp` | 96 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (6 calls) |
| `0x00137360` | `func_00137360` | `ctr/nn_dsp` | 124 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x001373F0` | `func_001373F0` | `ctr/nn_dsp` | 96 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (3 calls, vtable) |
| `0x00137458` | `func_00137458` | `ctr/nn_dsp` | 240 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (9 calls, vtable) |
| `0x00137524` | `func_00137524` | `ctr/nn_dsp` | 108 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (6 calls) |
| `0x001375A4` | `func_001375A4` | `ctr/nn_dsp` | 56 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x001375DC` | `func_001375DC` | `ctr/nn_dsp` | 32 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x001375FC` | `func_001375FC` | `ctr/nn_dsp` | 160 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (6 calls) |
| `0x0013769C` | `func_0013769C` | `ctr/nn_dsp` | 312 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm with loop |
| `0x001377D8` | `func_001377D8` | `ctr/nn_dsp` | 328 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x00137920` | `func_00137920` | `ctr/nn_dsp` | 16 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00137930` | `func_00137930` | `ctr/nn_dsp` | 32 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00137950` | `func_00137950` | `ctr/nn_dsp` | 284 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (13 calls) |
| `0x00137A0C` | `func_00137A0C` | `ctr/nn_dsp` | 16 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00137A1C` | `func_00137A1C` | `ctr/nn_dsp` | 88 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x00137A7C` | `func_00137A7C` | `ctr/nn_dsp` | 88 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00137AE0` | `func_00137AE0` | `ctr/nn_dsp` | 140 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (8 calls) |
| `0x00137B7C` | `func_00137B7C` | `ctr/nn_dsp` | 592 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (28 calls) |
| `0x00137DD0` | `func_00137DD0` | `ctr/nn_dsp` | 72 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x00137E20` | `func_00137E20` | `ctr/nn_dsp` | 56 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00137E60` | `func_00137E60` | `ctr/nn_dsp` | 148 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (16 calls) |
| `0x00137F18` | `func_00137F18` | `ctr/nn_dsp` | 52 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x00137F28` | `func_00137F28` | `ctr/nn_dsp` | 24 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00137F40` | `func_00137F40` | `ctr/nn_dsp` | 28 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00137F5C` | `func_00137F5C` | `ctr/nn_dsp` | 280 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x0013808C` | `func_0013808C` | `ctr/nn_dsp` | 100 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (12 calls) |
| `0x0013810C` | `func_0013810C` | `ctr/nn_dsp` | 24 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00138124` | `func_00138124` | `ctr/nn_dsp` | 160 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x001381D0` | `func_001381D0` | `ctr/nn_dsp` | 368 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00138344` | `func_00138344` | `ctr/nn_dsp` | 16 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00138354` | `func_00138354` | `ctr/nn_dsp` | 264 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (16 calls) |
| `0x00138478` | `func_00138478` | `ctr/nn_dsp` | 124 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (5 calls) |
| `0x001384AC` | `func_001384AC` | `ctr/nn_dsp` | 56 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x001384E8` | `func_001384E8` | `ctr/nn_dsp` | 160 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (14 calls) |
| `0x00138590` | `func_00138590` | `ctr/nn_dsp` | 64 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x001385D0` | `func_001385D0` | `ctr/nn_dsp` | 28 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (3 subcalls) |
| `0x001385EC` | `func_001385EC` | `ctr/nn_dsp` | 60 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x0013862C` | `func_0013862C` | `ctr/nn_dsp` | 52 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00138660` | `func_00138660` | `ctr/nn_dsp` | 40 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00138688` | `func_00138688` | `ctr/nn_dsp` | 72 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x001386D4` | `func_001386D4` | `ctr/nn_dsp` | 24 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x001386EC` | `func_001386EC` | `ctr/nn_dsp` | 52 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x0013873C` | `func_0013873C` | `ctr/nn_dsp` | 48 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00138770` | `func_00138770` | `ctr/nn_dsp` | 60 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x001387B0` | `func_001387B0` | `ctr/nn_dsp` | 48 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x001387E4` | `func_001387E4` | `ctr/nn_dsp` | 60 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00138824` | `func_00138824` | `ctr/nn_dsp` | 52 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00138858` | `func_00138858` | `ctr/nn_dsp` | 40 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00138880` | `func_00138880` | `ctr/nn_dsp` | 72 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x001388CC` | `func_001388CC` | `ctr/nn_dsp` | 32 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x001388EC` | `func_001388EC` | `ctr/nn_dsp` | 192 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (8 calls) |
| `0x001389BC` | `func_001389BC` | `ctr/nn_dsp` | 12 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x001389CC` | `func_001389CC` | `ctr/nn_dsp` | 76 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (6 calls) |
| `0x001389F4` | `func_001389F4` | `ctr/nn_dsp` | 60 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00138A30` | `func_00138A30` | `ctr/nn_dsp` | 40 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00138A80` | `func_00138A80` | `ctr/nn_dsp` | 12 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00138A90` | `func_00138A90` | `ctr/nn_dsp` | 12 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00138AA0` | `func_00138AA0` | `ctr/nn_dsp` | 8 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x00138AAC` | `func_00138AAC` | `ctr/nn_dsp` | 8 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x00138AB8` | `func_00138AB8` | `ctr/nn_dsp` | 148 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (6 calls) |
| `0x00138B58` | `func_00138B58` | `ctr/nn_dsp` | 8 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x00138B64` | `func_00138B64` | `ctr/nn_dsp` | 188 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (14 calls) |
| `0x00138C30` | `func_00138C30` | `ctr/nn_dsp` | 480 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (14 calls) |
| `0x00138E24` | `func_00138E24` | `ctr/nn_dsp` | 60 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00138E68` | `func_00138E68` | `ctr/nn_dsp` | 116 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00138EE4` | `func_00138EE4` | `ctr/nn_dsp` | 80 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00138F3C` | `func_00138F3C` | `ctr/nn_dsp` | 76 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00138F90` | `func_00138F90` | `ctr/nn_dsp` | 84 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00138FEC` | `func_00138FEC` | `ctr/nn_dsp` | 132 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x0013EC38` | `func_0013EC38` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x3C panic reason 4) |
| `0x0013EC48` | `svcBreak` | `ctr/svc` | 8 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x3C) |
| `0x0013EC50` | `func_0013EC50` | `ctr/svc` | 20 B | `1_leaf_stub` | 🟢 Matched (C/C++) | Thread yield stub via svc 0x0A (svcSleepThread(0)) |
| `0x0013EC5C` | `func_0013EC5C` | `ctr/svc` | 8 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x0A) |
| `0x0013EC64` | `svcWaitSynchronizationN` | `ctr/svc` | 36 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x25 WaitSynchronizationN) |
| `0x0013F29C` | `func_0013F29C` | `engine/core` | 12 B | `2_accessor` | 🟢 Matched (C/C++) | Level-5 engine subsystem pointer getter via literal pool (0x00867DA8) |
| `0x00151140` | `func_00151140` | `ctr/svc` | 1004 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x0015152C` | `func_0015152C` | `ctr/svc` | 252 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls, vtable) |
| `0x00151628` | `func_00151628` | `ctr/nn_math` | 28 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math 2D vector element-wise multiplication (VEC2Mul) |
| `0x00151644` | `func_00151644` | `ctr/nn_math` | 28 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math 2D vector element-wise addition (VEC2Add) |
| `0x00151660` | `func_00151660` | `ctr/svc` | 8 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x00151668` | `func_00151668` | `ctr/svc` | 88 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x001516C0` | `func_001516C0` | `ctr/svc` | 20 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x001516D4` | `func_001516D4` | `ctr/svc` | 136 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00151790` | `func_00151790` | `ctr/svc` | 140 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x0015181C` | `func_0015181C` | `ctr/svc` | 52 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00151850` | `func_00151850` | `ctr/svc` | 20 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00151864` | `func_00151864` | `ctr/svc` | 88 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00151914` | `func_00151914` | `ctr/svc` | 60 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00151950` | `func_00151950` | `ctr/svc` | 56 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00151988` | `func_00151988` | `ctr/svc` | 44 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00151A00` | `func_00151A00` | `ctr/svc` | 184 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00151AB8` | `func_00151AB8` | `ctr/svc` | 80 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00151B08` | `func_00151B08` | `ctr/svc` | 52 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00151B3C` | `func_00151B3C` | `ctr/svc` | 68 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00151B80` | `func_00151B80` | `ctr/svc` | 20 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00151B94` | `func_00151B94` | `ctr/svc` | 56 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x00151CA8` | `func_00151CA8` | `ctr/svc` | 20 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00151CBC` | `func_00151CBC` | `ctr/svc` | 72 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm |
| `0x00151D04` | `func_00151D04` | `ctr/nn_math` | 32 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math 2D vector linear interpolation (VEC2Lerp) |
| `0x00151D24` | `func_00151D24` | `ctr/nn_math` | 28 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math::ARMv6::VEC3AddAsm vector-vector addition |
| `0x00151D40` | `func_00151D40` | `ctr/nn_math` | 28 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math::ARMv6::VEC3SubAsm vector-vector subtraction |
| `0x00151D5C` | `func_00151D5C` | `ctr/nn_math` | 28 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math::ARMv6::VEC3MulAsm vector-vector multiplication |
| `0x00151D78` | `func_00151D78` | `ctr/nn_math` | 24 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math::ARMv6::VEC3AddAsm vector-scalar addition |
| `0x00151D90` | `func_00151D90` | `ctr/nn_math` | 24 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math::ARMv6::VEC3SubAsm vector-scalar subtraction |
| `0x00151DA8` | `func_00151DA8` | `ctr/nn_math` | 24 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math::ARMv6::VEC3MulAsm vector-scalar multiplication |
| `0x00151DC0` | `func_00151DC0` | `ctr/nn_math` | 40 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math 3D vector scalar triple product in registers (VEC3CrossDotReg) |
| `0x00151DE8` | `func_00151DE8` | `ctr/nn_math` | 52 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math 3D vector scalar triple product from pointers (VEC3CrossDot) |
| `0x00151E1C` | `func_00151E1C` | `ctr/nn_math` | 40 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math 3D vector linear interpolation (VEC3Lerp) |
| `0x00151E44` | `func_00151E44` | `ctr/nn_math` | 40 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math 3D vector cross product (VEC3Cross) |
| `0x00151E6C` | `func_00151E6C` | `ctr/nn_math` | 32 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math 4D vector addition (VEC4Add) |
| `0x00151E8C` | `func_00151E8C` | `ctr/nn_math` | 32 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math 4D vector subtraction (VEC4Sub) |
| `0x00151EAC` | `func_00151EAC` | `ctr/nn_math` | 32 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math 4D vector multiplication (VEC4Mul) |
| `0x00151ECC` | `func_00151ECC` | `ctr/nn_math` | 28 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math 4D vector scalar addition (VEC4AddScalar) |
| `0x00151EE8` | `func_00151EE8` | `ctr/nn_math` | 28 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math 4D vector scalar subtraction (VEC4SubScalar) |
| `0x00151F04` | `func_00151F04` | `ctr/nn_math` | 28 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math 4D vector scalar multiplication (VEC4MulScalar) |
| `0x00151F20` | `func_00151F20` | `ctr/nn_math` | 48 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math 4D vector linear interpolation (VEC4Lerp) |
| `0x00151F50` | `func_00151F50` | `ctr/nn_math` | 80 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | nn::math Quaternion Hamilton multiplication (QUATMul) |
| `0x00151FA0` | `svcCreateAddressArbiter` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x17) |
| `0x00151FB8` | `func_00151FB8` | `ctr/svc` | 4 B | `1_trivial` | ⚪ ASM Stub (Verified) | Constant return stub or leaf identity |
| `0x00151FBC` | `svcSleepThread` | `ctr/svc` | 8 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x28) |
| `0x00151FC4` | `svcGetThreadId` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x37) |
| `0x00151FE0` | `func_00151FE0` | `ctr/svc` | 80 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00152104` | `func_00152104` | `ctr/svc` | 116 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm with loop |
| `0x001521B0` | `func_001521B0` | `ctr/svc` | 384 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (20 calls) |
| `0x00152330` | `func_00152330` | `ctr/svc` | 1044 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm with loop |
| `0x00152748` | `func_00152748` | `ctr/svc` | 68 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x0015278C` | `func_0015278C` | `ctr/svc` | 24 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | Local arithmetic/bitwise computation |
| `0x001527A4` | `func_001527A4` | `ctr/svc` | 428 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00152950` | `func_00152950` | `ctr/svc` | 292 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (6 calls) |
| `0x00152A74` | `func_00152A74` | `ctr/svc` | 172 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00152B24` | `func_00152B24` | `ctr/svc` | 172 B | `6_moderate_caller` | ⚪ ASM Stub (Verified) | Moderate caller (2 subcalls) |
| `0x00152BD4` | `func_00152BD4` | `ctr/svc` | 168 B | `4_complex_leaf` | ⚪ ASM Stub (Verified) | Large leaf algorithm with loop |
| `0x00152C7C` | `func_00152C7C` | `ctr/svc` | 204 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (4 calls) |
| `0x00152C98` | `func_00152C98` | `ctr/svc` | 16 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00152CAC` | `func_00152CAC` | `ctr/svc` | 1468 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (29 calls, vtable) |
| `0x00152E2C` | `func_00152E2C` | `ctr/svc` | 20 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00152E44` | `func_00152E44` | `ctr/svc` | 12 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00152E50` | `func_00152E50` | `ctr/svc` | 20 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00152E68` | `func_00152E68` | `ctr/svc` | 20 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00152E98` | `func_00152E98` | `ctr/svc` | 336 B | `7_complex_caller` | ⚪ ASM Stub (Verified) | Complex caller (13 calls, vtable) |
| `0x0015BD4C` | `func_0015BD4C` | `ctr/svc` | 20 B | `2_simple_accessor` | ⚪ ASM Stub (Verified) | Single field getter/setter or global read |
| `0x00166948` | `svcArbitrateAddress` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x22 ArbitrateAddress) |
| `0x00171C78` | `func_00171C78` | `game/core` | 12 B | `2_accessor` | 🟢 Matched (C/C++) | Game subsystem global pointer getter via literal pool (0x0091B7B8) |
| `0x00175574` | `func_00175574` | `ctr/svc` | 32 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x0017656C` | `func_0017656C` | `game/core` | 4 B | `1_leaf_stub` | 🟢 Matched (C/C++) | Game subsystem leaf empty void stub function (bx lr) |
| `0x0018A714` | `svcCloseHandle` | `ctr/svc` | 8 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x23) |
| `0x0018A71C` | `func_0018A71C` | `ctr/svc` | 28 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x1E CreateMemoryBlock) |
| `0x0018A738` | `svcCreateMemoryBlock` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x13) |
| `0x0018A750` | `svcCreateThread` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x27) |
| `0x0018A768` | `svcGetHandleInfo` | `ctr/svc` | 28 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x29 GetHandleInfo) |
| `0x0018A784` | `svcControlMemory` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x0B) |
| `0x0018A868` | `svcWaitSynchronization1` | `ctr/svc` | 8 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x24) |
| `0x002C0DD4` | `func_002C0DD4` | `ctr/svc` | 36 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | CTR kernel syscall wrapper |
| `0x00301248` | `func_00301248` | `ctr/nn_nex` | 4 B | `1_leaf_stub` | 🟢 Matched (C/C++) | nn::nex leaf empty void stub function (bx lr) |
| `0x0031F1E8` | `_ZN2nn3nex7qResultaSERKS1_` | `ctr/nn_nex` | 12 B | `2_accessor` | 🟢 Matched (C/C++) | nn::nex::qResult::operator=(const qResult&) |
| `0x0031F1F4` | `_ZN2nn3nex7qResultC1Ev` | `ctr/nn_nex` | 16 B | `2_accessor` | 🟢 Match (Community Accepted) | nn::nex::qResult::qResult() |
| `0x0031F204` | `_ZN2nn3nex7qResultC1ERKS1_` | `ctr/nn_nex` | 12 B | `2_accessor` | 🟢 Matched (C/C++) | nn::nex::qResult::qResult(const qResult&) |
| `0x0031F210` | `_ZNK2nn3nex7qResult8getValueEv` | `ctr/nn_nex` | 16 B | `2_accessor` | 🟢 Matched (C/C++) | nn::nex::qResult::getValue() const |
| `0x0033B508` | `func_0033B508` | `ctr/svc` | 28 B | `3_arithmetic_logic` | ⚪ ASM Stub (Verified) | CTR kernel syscall wrapper |
| `0x00340CE8` | `_ZN2nn3nex10NexElementaSERKS1_` | `ctr/nn_nex` | 20 B | `2_accessor` | 🟢 Matched (C/C++) | nn::nex::NexElement::operator=(const NexElement&) |
| `0x00340CFC` | `_ZN2nn3nex10NexElementC1Eis` | `ctr/nn_nex` | 12 B | `2_accessor` | 🟢 Matched (C/C++) | nn::nex::NexElement::NexElement(s32, s16) |
| `0x00340D08` | `_ZN2nn3nex10NexElementC1Ev` | `ctr/nn_nex` | 16 B | `2_accessor` | 🟢 Matched (C/C++) | nn::nex::NexElement::NexElement() |
| `0x00340D18` | `_ZN2nn3nex10NexElementD1Ev` | `ctr/nn_nex` | 4 B | `1_leaf_stub` | 🟢 Matched (C/C++) | nn::nex::NexElement::~NexElement() |
| `0x00340D1C` | `_ZN2nn3nex10NexElementC1ERKS1_` | `ctr/nn_nex` | 20 B | `2_accessor` | 🟢 Matched (C/C++) | nn::nex::NexElement::NexElement(const NexElement&) |
| `0x00340E5C` | `_ZN2nn3nex21StationConnectionInfo11deserializeEPKh` | `ctr/nn_nex` | 72 B | `3_control_flow` | ⏳ Staged | nn::nex::StationConnectionInfo::deserialize(const u8*) |
| `0x00340EAC` | `_ZN2nn3nex21StationConnectionInfo7setPortEt` | `ctr/nn_nex` | 12 B | `2_accessor` | 🟢 Matched (C/C++) | nn::nex::StationConnectionInfo::setPort(u16) |
| `0x00340EB8` | `_ZN2nn3nex21StationConnectionInfo10setElementERKNS0_10NexElementE` | `ctr/nn_nex` | 20 B | `2_accessor` | 🟢 Matched (C/C++) | nn::nex::StationConnectionInfo::setElement(const NexElement&) |
| `0x00340ECC` | `_ZN2nn3nex21StationConnectionInfo5resetEv` | `ctr/nn_nex` | 20 B | `2_accessor` | 🟢 Matched (C/C++) | nn::nex::StationConnectionInfo::reset() |
| `0x00340EE8` | `_ZNK2nn3nex21StationConnectionInfo7compareERKS1_` | `ctr/nn_nex` | 136 B | `3_control_flow` | ⏳ Staged | nn::nex::StationConnectionInfo::compare(const StationConnectionInfo&) const |
| `0x005EE674` | `func_005EE674` | `ctr/svc` | 32 B | `5_simple_wrapper` | ⚪ ASM Stub (Verified) | Single function call wrapper / thunk |
| `0x005F015C` | `func_005F015C` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched (C/C++) | CTR kernel syscall wrapper stub (svc 0x28 GetSystemTick to pointer) |

<!-- MANIFEST_TABLE_END -->

---

## Architectural Layers & Didactic Decompilation Roadmap

Instead of sorting functions purely by byte size across the entire binary, the decompilation is organized into **three architectural layers** (`ctr`, `engine`, `game`), and within each layer candidates are ordered by **didactic complexity level** (from Level 1 leaf stubs up to Level 4 C++ vtables):

### Layer 1: Nintendo CTR-SDK & ARM Runtime (`src/ctr/`)
Standard Nintendo 3DS system libraries (`1.2.7.f-NINTENDO-CTR-SDK-v1`), kernel supervisor calls (`svc`), C/C++ runtime startup (`crt`), and `nn::*` modules (`nn::os`, `nn::fs`, `nn::ndm`, `nn::nex`, `nn::dsp`).

| Didactic Level | Virtual Address | Symbol | Module | Size | Status | Description |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **L1: Syscall Stub** | `0x00104778` | `svcExitProcess` | `ctr/svc` | 8 B | 🟢 Matched (C/C++) | Kernel syscall wrapper (`svc 0x03`) |
| **L1: Syscall Stub** | `0x00151FBC` | `svcSleepThread` | `ctr/svc` | 8 B | 🟢 Matched (C/C++) | Kernel syscall wrapper (`svc 0x28`) |
| **L1: Leaf Stub** | `0x00301248` | `func_00301248` | `ctr/nn_nex` | 4 B | 🟢 Matched (C/C++) | Empty void stub (`bx lr`) in `nn::nex` |
| **L2: OS Accessor** | `0x00104D18` | `func_00104D18` | `ctr/nn_os` | 16 B | 🟢 Matched (C/C++) | Global 8-bit flag setter (`0x00814E54`) |
| **L2: MMIO Reader** | `0x001063F4` | `func_001063F4` | `ctr/nn_os` | 16 B | 🟢 Matched (C/C++) | Reads CTR `SystemConfig` page (`0x1FF80040`) |
| **L2: OS Accessor** | `0x0010678C` | `func_0010678C` | `ctr/nn_os` | 16 B | 🟢 Matched (C/C++) | Signed byte reader (`0x00814E00`) |
| **L2: CRT Loop** | `0x00100024` | `clear_bss` | `ctr/crt` | 36 B | ⚪ ASM Stub (Verified) | Startup `.bss` zeroing loop (`0x00860934`–`0x0091B9BC`) |
| **L3: Synchronization** | `0x001274A0` | `func_001274A0` | `ctr/nn_os` | 24 B | ⚪ ASM Stub (Verified) | Atomic spinlock acquire loop (`ldrex`/`strex`) |
| **L3: Syscall + Stack** | `0x0010AAA8` | `svcCreateEvent` | `ctr/svc` | 24 B | 🟢 Matched (C/C++) | Kernel syscall wrapper with output pointer (`svc 0x21`) |
| **L3: Syscall + Stack** | `0x0010AAC0` | `svcDuplicateHandle` | `ctr/svc` | 24 B | 🟢 Matched (C/C++) | Kernel syscall wrapper (`svc 0x38`) |
| **L3: Array Indexer** | `0x001280A8` | `func_001280A8` | `ctr/nn_ndm` | 24 B | 🟢 Matched (C/C++) | Bounds-checked array element indexer (stride 8) |

### Layer 2: Level-5 Proprietary Engine (`src/engine/`)
Shared Level-5 middleware used across 3DS titles: **LFW** (*Level-5 Framework*: `lfwCObject`, `lfwCLoop`, `lfwCObj2DManager`, `lfwCObj3DManager`, `lfwCCameraManager`), **LXP** (*Level-5 Cross-Platform*: `lxpCMemory`, `lxpCStack`, `.fa` / `XPCK` archives), and **GDS** (*Generic Data Script*: `GDSFix`, `GDSSwitch`, `.cfg.bin` parsers).

| Didactic Level | Virtual Address | Symbol | Module | Size | Status | Description |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **L1: Virtual Stub** | `0x0010B6D0` | `func_0010B6D0` | `engine/lfw` | 8 B | 🟢 Matched (C/C++) | `lfwCLoopEmpty` virtual method (returns `0`, table `0x00107488`) |
| **L1: Virtual Stub** | `0x0012FEC0` | `func_0012FEC0` | `engine/lxp` | 8 B | 🟢 Matched (C/C++) | `lxpCMemory` boolean stub (returns `1`) |
| **L1: Virtual Stub** | `0x00130018` | `func_00130018` | `engine/lxp` | 8 B | 🟢 Matched (C/C++) | `lxpCMemory` virtual method (returns `1`, in 3 `.rodata` vtables) |
| **L2: RTTI Getter** | `0x0010B6D8` | `func_0010B6D8` | `engine/lfw` | 12 B | 🟢 Matched (C/C++) | `lfwCLoopEmpty::GetClassName` (`"lfwCLoopEmpty"` at `0x008602F8`) |
| **L2: Singleton Getter** | `0x0012CB00` | `func_0012CB00` | `engine/lxp` | 12 B | 🟢 Matched (C/C++) | Engine singleton getter (`0x00868A9C`, 10 callers) |
| **L2: Manager Getter** | `0x001300B0` | `func_001300B0` | `engine/lxp` | 12 B | 🟢 Matched (C/C++) | `lxpCMemory` manager pointer getter (`0x00868F10`) |
| **L3: Forwarding Thunk** | `0x00130D38` | `func_00130D38` | `engine/lxp` | 16 B | ⏳ Candidate | Null-checked method forwarding tail-call wrapper |
| **L4: C++ Class Method** | `0x0010B5D8` | `func_0010B5D8` | `engine/lfw` | 248 B | ⏳ Candidate | `lfwCLoopEmpty` factory / constructor (`0x00107484`) |
| **L4: C++ Class Method** | `0x0010B6E4` | `func_0010B6E4` | `engine/lfw` | 280 B | 🟡 In Review | `lfwCLoop` state update method with vtable dispatch |

### Layer 3: Yo-kai Watch 2 Game Logic (`src/game/`)
Game-specific state machines (`ywCLoopMain`, `ywCLoopRPG`, `ywCLoopBattle`, `ywCLoopMenu*`, `ywCLoopOrgeTime`), Yo-kai entities (`C$obj_yokai`), quests, watch map, and UI logic.

| Didactic Level | Virtual Address | Symbol | Module | Size | Status | Description |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **L1: Leaf Stub** | `0x0017656C` | `func_0017656C` | `game/core` | 4 B | 🟢 Matched (C/C++) | Empty void stub (`bx lr`) |
| **L1: Virtual Stub** | `0x0010CEE8` | `func_0010CEE8` | `game/loops` | 8 B | ⏳ Candidate | `ywCLoopRPG` virtual method (returns `0`, table `0x001074A0`) |
| **L1: Virtual Stub** | `0x0010CFF4` | `func_0010CFF4` | `game/loops` | 8 B | ⏳ Candidate | `ywCLoopMain` virtual method (returns `0`, table `0x00107494`) |
| **L2: RTTI Getter** | `0x0010CEF0` | `func_0010CEF0` | `game/loops` | 12 B | ⏳ Candidate | `ywCLoopRPG::GetClassName` (`"ywCLoopRPG"` at `0x0086048C`) |
| **L2: RTTI Getter** | `0x0010CFFC` | `func_0010CFFC` | `game/loops` | 12 B | ⏳ Candidate | `ywCLoopMain::GetClassName` (`"ywCLoopMain"` at `0x00860497`) |
| **L2: Pointer Getter** | `0x0010C894` | `func_0010C894` | `game/loops` | 12 B | 🟢 Matched (C/C++) | Game loop state pointer getter (`0x0086C8CC`) |
| **L2: Pointer Getter** | `0x00171C78` | `func_00171C78` | `game/core` | 12 B | 🟢 Matched (C/C++) | Global `.bss` state pointer getter (`0x0091B7B8`) |
| **L3: Struct Init** | `0x0011054C` | `func_0011054C` | `game/loops` | 24 B | 🟢 Matched (C/C++) | Struct header reset (zeros 8 bytes, sets byte 0 to `0xFF`) |

---

## 🎯 Target Classes Roadmap (C++ & Engine Structures)

In addition to individual atomic functions, the project organizes C++ reverse engineering into **Translation Units (TUs)** corresponding to complete classes, value types, and polymorphic state machines.

The entire catalog of **123 identified classes and structures** is categorized below by architectural layer and sorted in physical memory address order:

<!-- TARGET_CLASSES_TABLE_START -->

> **Total cataloged classes & structures: 123** (synchronized with [`config/classes_identified.csv`](config/classes_identified.csv), sorted in ascending address order).

### Layer 1: Nintendo CTR-SDK & ARM Runtime (CTR) (8 classes)

| Address | Class / Structure | Module | Base Class | Methods / Type | Status | Description |
| :--- | :--- | :---: | :--- | :---: | :---: | :--- |
| `0x00112E60` | `nn::y2r::Y2rObject` | `nn_y2r` | - | c_struct | 🟡 Partial | Y2R hardware converter object context |
| `0x00112E60` | `nn::y2r::Y2rSubContext` | `nn_y2r` | - | c_struct | 🟡 Partial | Y2R conversion channel sub-context descriptor |
| `0x001274A0` | `nn::os::SpinLock` | `nn_os` | - | c_struct | 🟡 Partial | Nintendo 3DS OS hardware atomic spinlock |
| `0x001280A8` | `nn::ndm::NdmContainer` | `nn_ndm` | - | c_struct | 🟡 Partial | NDM daemon indexed container header |
| `0x001280A8` | `nn::ndm::NdmElement8` | `nn_ndm` | - | c_struct | ⏳ Target | NDM daemon 8-byte entry element |
| `0x00340C60` | `nn::nex::qResult` | `nn_nex` | - | value_type | ⏳ Target | NEX error result code and status wrapper |
| `0x00340CE8` | `nn::nex::NexElement` | `nn_nex` | - | value_type | 🟢 Matched | Network stream element / station identifier (72 B, 5 methods) |
| `0x00340D30` | `nn::nex::StationURL` | `nn_nex` | - | value_type | ⏳ Target | NEX Rendez-Vous station connection URL descriptor |

### Layer 2: Level-5 Engine (LFW, LXP, LIZ, Core) (61 classes)

| Address | Class / Structure | Module | Base Class | Methods / Type | Status | Description |
| :--- | :--- | :---: | :--- | :---: | :---: | :--- |
| `0x00107478` | `LfwLoopClassInfo` | `lfw` | - | c_struct | ⏳ Target | Level-5 Framework loop state machine descriptor table |
| `0x001300B0` | `lxpCMemory` | `lxp` | - | engine_class | 🟡 Partial | Level-5 Cross-Platform memory manager |
| `0x007F16B8` | `liz::MemBase::ILj1ENS_8DontCopyEE` | `liz` | `liz::DontCopy` | interface | ⏳ Target | Abstract / RTTI interface descriptor |
| `0x007F16C4` | `liz::DontCopy` | `liz` | - | interface | ⏳ Target | Abstract / RTTI interface descriptor |
| `0x007F20D0` | `lxpCCamera` | `lxp` | - | 8 vmethods | ⏳ Target | Polymorphic C++ class (8 virtual methods) |
| `0x007F20F8` | `lxpCDrwRes` | `lxp` | - | 175 vmethods | ⏳ Target | Polymorphic C++ class (175 virtual methods) |
| `0x007F23BC` | `lxpCMemObj` | `lxp` | - | 3 vmethods | ⏳ Target | Polymorphic C++ class (3 virtual methods) |
| `0x007F23D0` | `lxpCObjDOF` | `lxp` | `lxpCObjColor` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007F2528` | `lfwCMessage` | `lfw` | `lxpCMessage` | 47 vmethods | ⏳ Target | Polymorphic C++ class (47 virtual methods) |
| `0x007F2600` | `lfwCObjLine` | `lfw` | `lxpCDrwRes` | 41 vmethods | ⏳ Target | Polymorphic C++ class (41 virtual methods) |
| `0x007F26AC` | `lxpCMessage` | `lxp` | - | 46 vmethods | ⏳ Target | Polymorphic C++ class (46 virtual methods) |
| `0x007F279C` | `lxpCObjBlur` | `lxp` | `lxpCDrwRes` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007F28A0` | `__lfwCObject` | `lfw` | - | 36 vmethods | ⏳ Target | Polymorphic C++ class (36 virtual methods) |
| `0x007F2938` | `lfwCObjImage` | `lfw` | `lxpCObjImage` | 70 vmethods | ⏳ Target | Polymorphic C++ class (70 virtual methods) |
| `0x007F2AC0` | `lxpCObjAnime` | `lxp` | `lxpCDrwRes` | 32 vmethods | ⏳ Target | Polymorphic C++ class (32 virtual methods) |
| `0x007F2B48` | `lxpCObjChara` | `lxp` | - | 33 vmethods | ⏳ Target | Polymorphic C++ class (33 virtual methods) |
| `0x007F2BE8` | `lxpCObjColor` | `lxp` | `lxpCDrwRes` | 34 vmethods | ⏳ Target | Polymorphic C++ class (34 virtual methods) |
| `0x007F2C78` | `lxpCObjImage` | `lxp` | `lxpCObjColor` | 36 vmethods | ⏳ Target | Polymorphic C++ class (36 virtual methods) |
| `0x007F2D10` | `lxpCObjMovie` | `lxp` | `lxpCObjImage` | 41 vmethods | ⏳ Target | Polymorphic C++ class (41 virtual methods) |
| `0x007F2DE4` | `lxpCResAnime` | `lxp` | `__lxpCResource` | 11 vmethods | ⏳ Target | Polymorphic C++ class (11 virtual methods) |
| `0x007F2E18` | `lxpCResChara` | `lxp` | `__lxpCResource` | 16 vmethods | ⏳ Target | Polymorphic C++ class (16 virtual methods) |
| `0x007F2E74` | `lxpCResModel` | `lxp` | `__lxpCResource` | 16 vmethods | ⏳ Target | Polymorphic C++ class (16 virtual methods) |
| `0x007F2ED0` | `lxpCResource` | `lxp` | `__lxpCResource` | 22 vmethods | ⏳ Target | Polymorphic C++ class (22 virtual methods) |
| `0x007F2F30` | `lfwCLoopEmpty` | `lfw` | `lfwCLoop` | 54 vmethods | 🟡 In Review | Polymorphic C++ class (54 virtual methods) |
| `0x007F3010` | `lxpCObjCanvas` | `lxp` | `lxpCObjImage` | 36 vmethods | ⏳ Target | Polymorphic C++ class (36 virtual methods) |
| `0x007F30A8` | `lxpCObjImage2` | `lxp` | `lxpCObjImage` | 36 vmethods | ⏳ Target | Polymorphic C++ class (36 virtual methods) |
| `0x007F3140` | `lxpCObjLocus1` | `lxp` | `__lxpCObjLocus` | 46 vmethods | ⏳ Target | Polymorphic C++ class (46 virtual methods) |
| `0x007F3200` | `lxpCObjLocus2` | `lxp` | `__lxpCObjLocus` | 123 vmethods | ⏳ Target | Polymorphic C++ class (123 virtual methods) |
| `0x007F33F4` | `__lxpCObjLocus` | `core` | `lxpCDrwRes` | 46 vmethods | ⏳ Target | Polymorphic C++ class (46 virtual methods) |
| `0x007F34B4` | `__lxpCResource` | `core` | - | 11 vmethods | ⏳ Target | Polymorphic C++ class (11 virtual methods) |
| `0x007F34E8` | `lfwCCamera_Dev` | `lfw` | `lxpCCameraControl` | 59 vmethods | ⏳ Target | Polymorphic C++ class (59 virtual methods) |
| `0x007F35DC` | `lfwCCamera_Fix` | `lfw` | `lxpCCameraControl` | 59 vmethods | ⏳ Target | Polymorphic C++ class (59 virtual methods) |
| `0x007F36D0` | `lfwCCamera_Mtn` | `lfw` | `lxpCCameraMotion` | 78 vmethods | ⏳ Target | Polymorphic C++ class (78 virtual methods) |
| `0x007F3810` | `lxpCObjCapture` | `lxp` | `lxpCDrwRes` | 33 vmethods | ⏳ Target | Polymorphic C++ class (33 virtual methods) |
| `0x007F389C` | `lxpCObjEasyDOF` | `lxp` | `lxpCObjImage` | 92 vmethods | ⏳ Target | Polymorphic C++ class (92 virtual methods) |
| `0x007F3A14` | `lfwCCamera_Move` | `lfw` | `lxpCCameraControl` | 103 vmethods | ⏳ Target | Polymorphic C++ class (103 virtual methods) |
| `0x007F3BB8` | `lxpCObjParticle` | `lxp` | - | 6 vmethods | ⏳ Target | Polymorphic C++ class (6 virtual methods) |
| `0x007F3C60` | `lxpCResParticle` | `lxp` | `__lxpCResource` | 99 vmethods | ⏳ Target | Polymorphic C++ class (99 virtual methods) |
| `0x007F3DF4` | `lfwCCamera_Dolly` | `lfw` | `lxpCCameraControl` | 59 vmethods | ⏳ Target | Polymorphic C++ class (59 virtual methods) |
| `0x007F3EE8` | `lfwCCamera_Orbit` | `lfw` | `lxpCCameraControl` | 115 vmethods | ⏳ Target | Polymorphic C++ class (115 virtual methods) |
| `0x007F40BC` | `lxpCCameraMotion` | `lxp` | `lxpCCameraControl` | 249 vmethods | ⏳ Target | Polymorphic C++ class (249 virtual methods) |
| `0x007F44A8` | `lxpCCameraControl` | `lxp` | `lxpCCamera` | 77 vmethods | ⏳ Target | Polymorphic C++ class (77 virtual methods) |
| `0x007F45E4` | `lxpCObjCharaMerge` | `lxp` | `lxpCDrwRes` | 78 vmethods | ⏳ Target | Polymorphic C++ class (78 virtual methods) |
| `0x007F4724` | `lxpCObjSimpleModel` | `lxp` | - | 32 vmethods | ⏳ Target | Polymorphic C++ class (32 virtual methods) |
| `0x007F4BC8` | `CLcs1` | `core` | `lxpCObjLocus1` | 46 vmethods | ⏳ Target | Polymorphic C++ class (46 virtual methods) |
| `0x007F4C88` | `CLcs2` | `core` | `lxpCObjLocus2` | 179 vmethods | ⏳ Target | Polymorphic C++ class (179 virtual methods) |
| `0x007F4F70` | `lfwCLoop` | `lfw` | `lxpCLoop` | 438 vmethods | ⏳ Target | Polymorphic C++ class (438 virtual methods) |
| `0x007F5650` | `lxpCLoop` | `lxp` | - | 23 vmethods | ⏳ Target | Polymorphic C++ class (23 virtual methods) |
| `0x007F5830` | `lfwCObj2D` | `lfw` | `__lfwCObject` | 16 vmethods | ⏳ Target | Polymorphic C++ class (16 virtual methods) |
| `0x007F5878` | `lfwCObj3D` | `lfw` | `__lfwCObject` | 30 vmethods | ⏳ Target | Polymorphic C++ class (30 virtual methods) |
| `0x007F590C` | `__cxxabiv1::__class_type_info` | `core` | - | 2 vmethods | ⏳ Target | Polymorphic C++ class (2 virtual methods) |
| `0x007F591C` | `__cxxabiv1::__si_class_type_info` | `core` | `__cxxabiv1::__class_type_info` | 2 vmethods | ⏳ Target | Polymorphic C++ class (2 virtual methods) |
| `0x007F592C` | `__cxxabiv1::__vmi_class_type_info` | `core` | `__cxxabiv1::__class_type_info` | 25 vmethods | ⏳ Target | Polymorphic C++ class (25 virtual methods) |
| `0x00800FD8` | `liz::ResBaseLXP` | `liz` | `liz::IResource` | 7 vmethods | ⏳ Target | Polymorphic C++ class (7 virtual methods) |
| `0x00800FFC` | `liz::ResAnimeLXP` | `liz` | `liz::IResource` | 7 vmethods | ⏳ Target | Polymorphic C++ class (7 virtual methods) |
| `0x00801020` | `liz::ResCharaLXP` | `liz` | `liz::IResource` | 7 vmethods | ⏳ Target | Polymorphic C++ class (7 virtual methods) |
| `0x00801044` | `liz::ResImageLXP` | `liz` | `liz::IResource` | 7 vmethods | ⏳ Target | Polymorphic C++ class (7 virtual methods) |
| `0x00801068` | `liz::ResModelLXP` | `liz` | `liz::IResource` | 7 vmethods | ⏳ Target | Polymorphic C++ class (7 virtual methods) |
| `0x0080108C` | `liz::ResObj2DLXP` | `liz` | `liz::IResource` | 15 vmethods | ⏳ Target | Polymorphic C++ class (15 virtual methods) |
| `0x008010D0` | `liz::IResource` | `liz` | `liz::MemBase::ILj1ENS_8DontCopyEE` | 7 vmethods | ⏳ Target | Polymorphic C++ class (7 virtual methods) |
| `0x008010F4` | `liz::ResSkyLXP` | `liz` | `liz::IResource` | 1252 vmethods | ⏳ Target | Polymorphic C++ class (1252 virtual methods) |

### Layer 3: Yo-kai Watch 2 Game Logic (YW2) (54 classes)

| Address | Class / Structure | Module | Base Class | Methods / Type | Status | Description |
| :--- | :--- | :---: | :--- | :---: | :---: | :--- |
| `0x00107478` | `yw::YwLoopHeader` | `loops` | - | c_struct | ⏳ Target | Game loop state machine descriptor header |
| `0x007F14AC` | `yw::ywIGDDInventory` | `core` | - | interface | ⏳ Target | Abstract / RTTI interface descriptor |
| `0x007F1604` | `yw::ywIGDDInventoryStackable` | `core` | `yw::ywIGDDInventory` | interface | ⏳ Target | Abstract / RTTI interface descriptor |
| `0x007FA598` | `yw::ywCLoopRPG` | `loops` | `yw::ywCLoop` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FA640` | `yw::ywCMessage` | `core` | `lfwCMessage` | 47 vmethods | ⏳ Target | Polymorphic C++ class (47 virtual methods) |
| `0x007FA77C` | `yw::ywCLoopMain` | `loops` | `yw::ywCLoop` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FA824` | `yw::ywCLoopMenu` | `loops` | `yw::ywCLoopSequence` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FA8CC` | `yw::ywCLoopRace` | `loops` | `yw::ywCLoop` | 60 vmethods | ⏳ Target | Polymorphic C++ class (60 virtual methods) |
| `0x007FA9C4` | `yw::ywCLoopEvent` | `loops` | `yw::ywCLoop` | 135 vmethods | ⏳ Target | Polymorphic C++ class (135 virtual methods) |
| `0x007FABE8` | `yw::ywCLoopBattle` | `loops` | `yw::ywCLoop` | 125 vmethods | ⏳ Target | Polymorphic C++ class (125 virtual methods) |
| `0x007FADE4` | `yw::ywCLoopCapsule` | `loops` | `yw::ywCLoopSequence` | 124 vmethods | ⏳ Target | Polymorphic C++ class (124 virtual methods) |
| `0x007FAFDC` | `yw::ywCLoopMenuItem` | `loops` | `yw::ywCLoopMenuScrollList` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FB084` | `yw::ywCLoopMenuName` | `loops` | `yw::ywCLoopMenu` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FB12C` | `yw::ywCLoopMenuShop` | `loops` | `yw::ywCLoopMenuScrollList` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FB1D4` | `yw::ywCLoopMenuWarp` | `loops` | `yw::ywCLoopMenuScrollList` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FB27C` | `yw::ywCLoopOrgeTime` | `loops` | `yw::ywCLoop` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FB324` | `yw::ywCLoopSequence` | `loops` | `yw::ywCLoop` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FB3CC` | `yw::ywCLoopWatchmap` | `loops` | `yw::ywCLoopSequence` | 191 vmethods | ⏳ Target | Polymorphic C++ class (191 virtual methods) |
| `0x007FB6D0` | `yw::ywCLoopMenuQuest` | `loops` | `yw::ywCLoopMenuScrollList` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FB778` | `yw::ywCLoopMenuTrade` | `loops` | `yw::ywCLoopMenuMember` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FB820` | `yw::ywCLoopMenuYSpot` | `loops` | `yw::ywCLoopMenuScrollList` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FB8C8` | `yw::ywCLoopMusicGame` | `loops` | `yw::ywCLoop` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FB970` | `yw::ywCLoopYokaispot` | `loops` | `yw::ywCLoopSequence` | 173 vmethods | ⏳ Target | Polymorphic C++ class (173 virtual methods) |
| `0x007FBC2C` | `yw::ywCLoopEnenTunnel` | `loops` | `yw::ywCLoop` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FBCD4` | `yw::ywCLoopFaceDetect` | `loops` | `yw::ywCLoopMenu` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FBD7C` | `yw::ywCLoopMenuMember` | `loops` | `yw::ywCLoopMenuScrollList` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FBE24` | `yw::ywCLoopMenuWanted` | `loops` | `yw::ywCLoopMenuScrollList` | 211 vmethods | ⏳ Target | Polymorphic C++ class (211 virtual methods) |
| `0x007FC178` | `yw::ywCLoopMenuCombine` | `loops` | `yw::ywCLoopMenuScrollList` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FC220` | `yw::ywCLoopMenuFilmApp` | `loops` | `yw::ywCLoopMenuScrollList` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FC2C8` | `yw::ywCLoopMenuLinkage` | `loops` | `yw::ywCLoopMenu` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FC370` | `yw::ywCLoopMenuLottery` | `loops` | `yw::ywCLoopMenu` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FC418` | `yw::ywCLoopMenuObserve` | `loops` | `yw::ywCLoopMenuMember` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FC4C0` | `yw::ywCLoopMenuScratch` | `loops` | `yw::ywCLoopMenu` | 101 vmethods | ⏳ Target | Polymorphic C++ class (101 virtual methods) |
| `0x007FC65C` | `yw::ywGDDInventorySoul` | `core` | `yw::ywIGDDInventory` | 152 vmethods | ⏳ Target | Polymorphic C++ class (152 virtual methods) |
| `0x007FC8C4` | `yw::ywCLoopMenuDownload` | `loops` | `yw::ywCLoopMenu` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FC96C` | `yw::ywCLoopMenuMatching` | `loops` | `yw::ywCLoopMenuScrollList` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FCA14` | `yw::ywCLoopMenuMovieApp` | `loops` | `yw::ywCLoopMenuScrollList` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FCABC` | `yw::ywCLoopMenuMusicApp` | `loops` | `yw::ywCLoopMenuScrollList` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FCB64` | `yw::ywCLoopMenuQuestSub` | `loops` | `yw::ywCLoopMenuScrollList` | 248 vmethods | ⏳ Target | Polymorphic C++ class (248 virtual methods) |
| `0x007FCF4C` | `yw::ywCLoopMenuEcommerce` | `loops` | `yw::ywCLoopMenu` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x007FCFF4` | `yw::ywCLoopMenuMapScroll` | `loops` | `yw::ywCLoopMenu` | 170 vmethods | ⏳ Target | Polymorphic C++ class (170 virtual methods) |
| `0x007FD2A4` | `yw::ywCLoopMenuScrollList` | `loops` | `yw::ywCLoopMenu` | 59 vmethods | ⏳ Target | Polymorphic C++ class (59 virtual methods) |
| `0x007FD398` | `yw::ywGDDInventoryConsume` | `core` | `yw::ywIGDDInventoryStackable` | 294 vmethods | ⏳ Target | Polymorphic C++ class (294 virtual methods) |
| `0x007FD838` | `yw::ywGDDInventoryEquipment` | `core` | `yw::ywIGDDInventoryStackable` | 8 vmethods | ⏳ Target | Polymorphic C++ class (8 virtual methods) |
| `0x007FD860` | `yw::ywGDDInventoryImportant` | `core` | `yw::ywIGDDInventory` | 141 vmethods | ⏳ Target | Polymorphic C++ class (141 virtual methods) |
| `0x007FDA9C` | `yw::ywCLoopMenuDataMigration` | `loops` | `yw::ywCLoopMenu` | 265 vmethods | ⏳ Target | Polymorphic C++ class (265 virtual methods) |
| `0x007FDEC8` | `yw::ywCLoopMenuTrueOrgeMatching` | `loops` | `yw::ywCLoopMenuMatching` | 85 vmethods | ⏳ Target | Polymorphic C++ class (85 virtual methods) |
| `0x007FE024` | `yw::ywCLoopMenuFriendBookRanking` | `loops` | `yw::ywCLoopMenuScrollList` | 411 vmethods | ⏳ Target | Polymorphic C++ class (411 virtual methods) |
| `0x007FE698` | `yw::ywCLoopMenuFriendBookFriendList` | `loops` | `yw::ywCLoopMenuScrollList` | 2281 vmethods | ⏳ Target | Polymorphic C++ class (2281 virtual methods) |
| `0x00800A44` | `yw::World::ywCCamera_Rpg` | `world` | `lxpCCameraControl` | 60 vmethods | ⏳ Target | Polymorphic C++ class (60 virtual methods) |
| `0x00800B3C` | `yw::World::ywCCamera_Battle` | `battle` | `yw::World::ywCCamera_Rpg` | 60 vmethods | ⏳ Target | Polymorphic C++ class (60 virtual methods) |
| `0x00800C34` | `yw::World::ywCCamera_Watchmap` | `world` | `yw::World::ywCCamera_Rpg` | 140 vmethods | ⏳ Target | Polymorphic C++ class (140 virtual methods) |
| `0x00800E6C` | `yw::ywCLoop` | `loops` | `lfwCLoop` | 40 vmethods | ⏳ Target | Polymorphic C++ class (40 virtual methods) |
| `0x00800F14` | `yw::ywCLoopQR` | `loops` | `yw::ywCLoopSequence` | 47 vmethods | ⏳ Target | Polymorphic C++ class (47 virtual methods) |


<!-- TARGET_CLASSES_TABLE_END -->

---

## Repository layout

```text
src/
├── ctr/         Layer 1: Nintendo CTR-SDK & ARM Runtime (crt/, svc/, nn/os/, nn/ndm/, nn/nex/)
├── engine/      Layer 2: Level-5 Engine (lfw/, lxp/, gds/, core/)
└── game/        Layer 3: Yo-kai Watch 2 Game Logic (loops/, core/)
include/
├── nn/          Nintendo CTR-SDK official headers (Result.h, Handle.h, svc/, os/, fs/, srv/, ndm/)
├── ctr/         CTR subsystem headers (nex.h)
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
make check            # Compiles and byte-compares candidate functions and stubs
make progress         # Audits progress metrics and synchronizes README.md
make report           # Generates reference objects and build/report.json via objdiff-cli
make classes          # Synchronizes config/classes_identified.csv from binary RTTI
```

The verification tool reports each routine with explicit status tags:
- `>>> MATCH (C) <<<`: Real decompiled C/C++ function compiling byte-for-byte identical to the retail binary.
- `>>> ASM STUB <<<`: Modular assembly stub (`.s`) verified bit-for-bit to guarantee zero regressions during the "Split & Replace" workflow.
- `>>> MATCH (COMMUNITY ACCEPTED) <<<`: Equivalent C implementation with acceptable compiler register allocation difference.
- `>>> REGRESSION / MISMATCH <<<`: Indicates a divergence against `extracted/code.raw.bin` that blocks matching.

---

## Credits & External References

- **Level-5 Inc.**: Developers of *Yo-kai Watch 2*.
- **[3dsdecomp/nnsdk](https://github.com/3dsdecomp/nnsdk)**: Community reverse-engineering and matching decompilation of the Nintendo 3DS SDK (`nnsdk`), providing the official `nn::` namespace definitions (`nn::Result`, `nn::Handle`, `nn::os`, `nn::svc`, `nn::fs`, `nn::srv`, `nn::ndm`) integrated in `include/nn/`.
- **[devkitPro / libctru](https://github.com/devkitPro/libctru)**: Open-source Nintendo 3DS user-space library and hardware service reference documentation.
- **Yokimitsuro ([khdays-decomp](https://github.com/Yokimitsuro/khdays-decomp))**: Decompilation guidance, repository design, and the progress reporting methodology that inspired this structure.
- **Jack Price-Burns ([Decomp Academy](https://decomp-academy.dev/))**: Interactive matching decompilation foundations.
- **[pyctr](https://github.com/ihaveamac/pyctr)**: 3DS container parsing and LZSS decompression tooling.
- **[decomp.dev](https://decomp.dev/)**: The community driving modern video game matching decompilation.
