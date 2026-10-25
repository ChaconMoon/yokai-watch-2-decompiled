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
| **Real C-decompiled matched functions** | **65** / 18,225 (0.36%) | Functions implemented in C and verified byte-exact |
| **Complete functions (C + verified original library assembly)** | **74** / 18,225 (0.41%) | Real C (65) + CRT/SDK assembly routines (9: `clear_bss`, etc.) |
| **Real C-decompiled matched bytes** | **1108** / 6,238,892 bytes (0.0178%) | Real-C-only byte progress (1356 B including CRT assembly) |
| **Layer 1: Nintendo CTR-SDK & Runtime (`src/ctr/`)** | **63** matched (1232 B) | CRT startup, `svc` syscalls, `nn::os`, `nn::ndm`, `nn::nex` |
| **Layer 2: Level-5 Engine (`src/engine/`)** | **7** matched (72 B) | `lfw` (Framework), `lxp` (Cross-Platform), `gds` (Scripts) |
| **Layer 3: Yo-kai Watch 2 Game (`src/game/`)** | **4** matched (52 B) | `ywCLoop*` states, battle, RPG, menus, and entities |
| **Named / mapped candidates in manifest** | **78** / 18,225 | Functions actively tracked across `src/` and `scratches/` |
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
| `0x0010655C` | `func_0010655C` | `ctr/nn_os` | 20 B | `2_accessor` | 🟢 Matched | nn::os::detail TLS pointer store to global offset via literal pool (0x00815DE0) |
| `0x0010678C` | `func_0010678C` | `ctr/nn_os` | 16 B | `2_accessor` | 🟢 Matched | nn::os startup global signed byte reader via literal pool (0x00814E00) |
| `0x0010AA84` | `func_0010AA84` | `ctr/svc` | 36 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x01 ControlMemory) |
| `0x0010AAA8` | `svcCreateEvent` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x21) |
| `0x0010AAC0` | `svcDuplicateHandle` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x38) |
| `0x0010B6D0` | `func_0010B6D0` | `engine/lfw` | 8 B | `1_leaf_stub` | 🟢 Matched | lfwCLoopEmpty virtual method (returns constant 0, table 0x00107488) |
| `0x0010B6D8` | `func_0010B6D8` | `engine/lfw` | 12 B | `2_accessor` | 🟢 Matched | lfwCLoopEmpty::GetClassName getter via literal pool (0x008602F8) |
| `0x0010B6E4` | `func_0010B6E4` | `engine/lfw` | 280 B | `4_cpp_vtable` | 🟡 In Review | lfwCLoop C++ class method (partially decompiled, ~82% match in decomp.me) |
| `0x0010C894` | `func_0010C894` | `game/loops` | 12 B | `2_accessor` | 🟢 Matched | Game loop subsystem pointer getter via literal pool (0x0086C8CC) |
| `0x0011054C` | `func_0011054C` | `game/loops` | 24 B | `3_arithmetic_logic` | 🟢 Matched | Struct header reset (zeros 8 bytes, sets byte 0 to 0xFF) |
| `0x00112D8C` | `func_00112D8C` | `ctr/nn_y2r` | 20 B | `6_moderate_caller` | 🟢 Matched | Method chaining wrapper invoking func_0014A06C |
| `0x00112E60` | `func_00112E60` | `ctr/nn_y2r` | 16 B | `2_accessor` | 🟢 Matched | Y2R struct offset 8648 u16 reader |
| `0x00112FF0` | `svcCreateTimer` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x2D) |
| `0x00113008` | `func_00113008` | `ctr/svc` | 36 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x08 CreateThread) |
| `0x001137C0` | `func_001137C0` | `ctr/nn_y2r` | 20 B | `6_moderate_caller` | 🟢 Matched | Helper invoking func_00136154(&unk_0086A0A4) |
| `0x00113F58` | `func_00113F58` | `ctr/nn_y2r` | 20 B | `2_accessor` | 🟢 Matched | Y2R global bit 3 flag getter via literal pool (0x008661EC) |
| `0x00113F70` | `func_00113F70` | `ctr/nn_y2r` | 12 B | `2_accessor` | 🟢 Matched | Y2R global float field getter via literal pool (0x00815090) |
| `0x001274A0` | `func_001274A0` | `ctr/nn_os` | 24 B | `3_arithmetic_logic` | 🟡 In Review | nn::os atomic spinlock acquire loop (ldrex/strex synchronization) |
| `0x00127520` | `func_00127520` | `ctr/nn_os` | 12 B | `2_accessor` | 🟢 Matched | CTR-SDK .text size / limit getter via literal pool (0x005F32AC) |
| `0x001275D8` | `func_001275D8` | `ctr/nn_os` | 12 B | `2_accessor` | 🟢 Matched | CTR-SDK .text base VMA getter via literal pool (0x00100000) |
| `0x0012788C` | `func_0012788C` | `ctr/nn_os` | 16 B | `2_accessor` | 🟢 Matched | nn::os global flag setter via literal pool (0x00828EEC) |
| `0x00127EE0` | `func_00127EE0` | `ctr/nn_ndm` | 12 B | `2_accessor` | 🟢 Matched | nn::ndm global state offset reader via literal pool (0x00865F18) |
| `0x00127EEC` | `func_00127EEC` | `ctr/nn_ndm` | 12 B | `2_accessor` | 🟢 Matched | nn::ndm global state pointer getter via literal pool (0x00865F10) |
| `0x001280A8` | `func_001280A8` | `ctr/nn_ndm` | 24 B | `3_arithmetic_logic` | 🟢 Matched | nn::ndm bounds-checked struct array element indexer (stride 8, offset +0x0C) |
| `0x001284E4` | `func_001284E4` | `ctr/nn_applet` | 28 B | `2_accessor` | 🟢 Matched | nn::applet::CTR::IsApplication attribute check via literal pool (0x00814E00) |
| `0x0012CB00` | `func_0012CB00` | `engine/lxp` | 12 B | `2_accessor` | 🟢 Matched | Level-5 engine global singleton getter via literal pool (0x00868A9C) |
| `0x0012F190` | `svcExitThread` | `ctr/svc` | 8 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x09) |
| `0x0012F198` | `svcCreateResourceLimit` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x35) |
| `0x0012FEC0` | `func_0012FEC0` | `engine/lxp` | 8 B | `1_leaf_stub` | 🟢 Matched | lxpCMemory boolean true stub (returns constant 1) |
| `0x00130018` | `func_00130018` | `engine/lxp` | 8 B | `1_leaf_stub` | 🟢 Matched | lxpCMemory virtual boolean true stub (returns constant 1) |
| `0x001300B0` | `func_001300B0` | `engine/lxp` | 12 B | `2_accessor` | 🟢 Matched | lxpCMemory manager pointer getter via literal pool (0x00868F10) |
| `0x0013EC38` | `func_0013EC38` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x3C panic reason 4) |
| `0x0013EC48` | `svcBreak` | `ctr/svc` | 8 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x3C) |
| `0x0013EC50` | `func_0013EC50` | `ctr/svc` | 20 B | `1_leaf_stub` | 🟢 Matched | Thread yield stub via svc 0x0A (svcSleepThread(0)) |
| `0x0013EC5C` | `func_0013EC5C` | `ctr/svc` | 8 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x0A) |
| `0x0013EC64` | `svcWaitSynchronizationN` | `ctr/svc` | 36 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x25 WaitSynchronizationN) |
| `0x0013F29C` | `func_0013F29C` | `engine/core` | 12 B | `2_accessor` | 🟢 Matched | Level-5 engine subsystem pointer getter via literal pool (0x00867DA8) |
| `0x00151628` | `func_00151628` | `ctr/nn_math` | 28 B | `3_arithmetic_logic` | 🟢 Matched | nn::math 2D vector element-wise multiplication (VEC2Mul) |
| `0x00151644` | `func_00151644` | `ctr/nn_math` | 28 B | `3_arithmetic_logic` | 🟢 Matched | nn::math 2D vector element-wise addition (VEC2Add) |
| `0x00151D24` | `func_00151D24` | `ctr/nn_math` | 28 B | `3_arithmetic_logic` | 🟢 Matched | nn::math::ARMv6::VEC3AddAsm vector-vector addition |
| `0x00151D40` | `func_00151D40` | `ctr/nn_math` | 28 B | `3_arithmetic_logic` | 🟢 Matched | nn::math::ARMv6::VEC3SubAsm vector-vector subtraction |
| `0x00151D5C` | `func_00151D5C` | `ctr/nn_math` | 28 B | `3_arithmetic_logic` | 🟢 Matched | nn::math::ARMv6::VEC3MulAsm vector-vector multiplication |
| `0x00151D78` | `func_00151D78` | `ctr/nn_math` | 24 B | `3_arithmetic_logic` | 🟢 Matched | nn::math::ARMv6::VEC3AddAsm vector-scalar addition |
| `0x00151D90` | `func_00151D90` | `ctr/nn_math` | 24 B | `3_arithmetic_logic` | 🟢 Matched | nn::math::ARMv6::VEC3SubAsm vector-scalar subtraction |
| `0x00151DA8` | `func_00151DA8` | `ctr/nn_math` | 24 B | `3_arithmetic_logic` | 🟢 Matched | nn::math::ARMv6::VEC3MulAsm vector-scalar multiplication |
| `0x00151FA0` | `svcCreateAddressArbiter` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x17) |
| `0x00151FBC` | `svcSleepThread` | `ctr/svc` | 8 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x28) |
| `0x00151FC4` | `svcGetThreadId` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x37) |
| `0x00166948` | `svcArbitrateAddress` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x22 ArbitrateAddress) |
| `0x00171C78` | `func_00171C78` | `game/core` | 12 B | `2_accessor` | 🟢 Matched | Game subsystem global pointer getter via literal pool (0x0091B7B8) |
| `0x0017656C` | `func_0017656C` | `game/core` | 4 B | `1_leaf_stub` | 🟢 Matched | Game subsystem leaf empty void stub function (bx lr) |
| `0x0018A714` | `svcCloseHandle` | `ctr/svc` | 8 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x23) |
| `0x0018A71C` | `func_0018A71C` | `ctr/svc` | 28 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x1E CreateMemoryBlock) |
| `0x0018A738` | `svcCreateMemoryBlock` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x13) |
| `0x0018A750` | `svcCreateThread` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x27) |
| `0x0018A768` | `svcGetHandleInfo` | `ctr/svc` | 28 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x29 GetHandleInfo) |
| `0x0018A784` | `svcControlMemory` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x0B) |
| `0x0018A868` | `svcWaitSynchronization1` | `ctr/svc` | 8 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x24) |
| `0x00301248` | `func_00301248` | `ctr/nn_nex` | 4 B | `1_leaf_stub` | 🟢 Matched | nn::nex leaf empty void stub function (bx lr) |
| `0x0031F1E8` | `_ZN2nn3nex7qResultaSERKS1_` | `ctr/nn_nex` | 12 B | `2_accessor` | 🟢 Matched | nn::nex::qResult::operator=(const qResult&) |
| `0x0031F1F4` | `_ZN2nn3nex7qResultC1Ev` | `ctr/nn_nex` | 16 B | `2_accessor` | 🟢 Match (Community Accepted) | nn::nex::qResult::qResult() |
| `0x0031F204` | `_ZN2nn3nex7qResultC1ERKS1_` | `ctr/nn_nex` | 12 B | `2_accessor` | 🟢 Matched | nn::nex::qResult::qResult(const qResult&) |
| `0x0031F210` | `_ZNK2nn3nex7qResult8getValueEv` | `ctr/nn_nex` | 16 B | `2_accessor` | 🟢 Matched | nn::nex::qResult::getValue() const |
| `0x00340CE8` | `_ZN2nn3nex10NexElementaSERKS1_` | `ctr/nn_nex` | 20 B | `2_accessor` | 🟢 Matched | nn::nex::NexElement::operator=(const NexElement&) |
| `0x00340CFC` | `_ZN2nn3nex10NexElementC1Eis` | `ctr/nn_nex` | 12 B | `2_accessor` | 🟢 Matched | nn::nex::NexElement::NexElement(s32, s16) |
| `0x00340D08` | `_ZN2nn3nex10NexElementC1Ev` | `ctr/nn_nex` | 16 B | `2_accessor` | 🟢 Matched | nn::nex::NexElement::NexElement() |
| `0x00340D18` | `_ZN2nn3nex10NexElementD1Ev` | `ctr/nn_nex` | 4 B | `1_leaf_stub` | 🟢 Matched | nn::nex::NexElement::~NexElement() |
| `0x00340D1C` | `_ZN2nn3nex10NexElementC1ERKS1_` | `ctr/nn_nex` | 20 B | `2_accessor` | 🟢 Matched | nn::nex::NexElement::NexElement(const NexElement&) |
| `0x00340E5C` | `_ZN2nn3nex21StationConnectionInfo11deserializeEPKh` | `ctr/nn_nex` | 72 B | `3_control_flow` | ⏳ Staged | nn::nex::StationConnectionInfo::deserialize(const u8*) |
| `0x00340EAC` | `_ZN2nn3nex21StationConnectionInfo7setPortEt` | `ctr/nn_nex` | 12 B | `2_accessor` | 🟢 Matched | nn::nex::StationConnectionInfo::setPort(u16) |
| `0x00340EB8` | `_ZN2nn3nex21StationConnectionInfo10setElementERKNS0_10NexElementE` | `ctr/nn_nex` | 20 B | `2_accessor` | 🟢 Matched | nn::nex::StationConnectionInfo::setElement(const NexElement&) |
| `0x00340ECC` | `_ZN2nn3nex21StationConnectionInfo5resetEv` | `ctr/nn_nex` | 20 B | `2_accessor` | 🟢 Matched | nn::nex::StationConnectionInfo::reset() |
| `0x00340EE8` | `_ZNK2nn3nex21StationConnectionInfo7compareERKS1_` | `ctr/nn_nex` | 136 B | `3_control_flow` | ⏳ Staged | nn::nex::StationConnectionInfo::compare(const StationConnectionInfo&) const |
| `0x005F015C` | `func_005F015C` | `ctr/svc` | 24 B | `1_leaf_stub` | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x28 GetSystemTick to pointer) |

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
| **L3: Syscall + Stack** | `0x0010AAA8` | `svcCreateEvent` | `ctr/svc` | 24 B | 🟢 Matched | Kernel syscall wrapper with output pointer (`svc 0x21`) |
| **L3: Syscall + Stack** | `0x0010AAC0` | `svcDuplicateHandle` | `ctr/svc` | 24 B | 🟢 Matched | Kernel syscall wrapper (`svc 0x38`) |
| **L3: Array Indexer** | `0x001280A8` | `func_001280A8` | `ctr/nn_ndm` | 24 B | 🟢 Matched | Bounds-checked array element indexer (stride 8) |

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
make check            # Compiles and byte-compares candidate functions
```

A green `>>> MATCH <<<` means your C reproduces the original binary exactly, instruction for instruction.

---

## Credits & External References

- **Level-5 Inc.**: Developers of *Yo-kai Watch 2*.
- **[3dsdecomp/nnsdk](https://github.com/3dsdecomp/nnsdk)**: Community reverse-engineering and matching decompilation of the Nintendo 3DS SDK (`nnsdk`), providing the official `nn::` namespace definitions (`nn::Result`, `nn::Handle`, `nn::os`, `nn::svc`, `nn::fs`, `nn::srv`, `nn::ndm`) integrated in `include/nn/`.
- **[devkitPro / libctru](https://github.com/devkitPro/libctru)**: Open-source Nintendo 3DS user-space library and hardware service reference documentation.
- **Yokimitsuro ([khdays-decomp](https://github.com/Yokimitsuro/khdays-decomp))**: Decompilation guidance, repository design, and the progress reporting methodology that inspired this structure.
- **Jack Price-Burns ([Decomp Academy](https://decomp-academy.dev/))**: Interactive matching decompilation foundations.
- **[pyctr](https://github.com/ihaveamac/pyctr)**: 3DS container parsing and LZSS decompression tooling.
- **[decomp.dev](https://decomp.dev/)**: The community driving modern video game matching decompilation.
