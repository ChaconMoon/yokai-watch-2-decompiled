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
| **Real C-decompiled matched functions** | **20** / ~18,292 (0.11%) | Functions implemented in C and verified byte-exact (func_0010B6D0, func_0010B6D8, func_00104D18, func_001063F4, clear_bss, svcExitProcess, func_0017656C, func_00301248, func_0012FEC0, func_00130018, svcSleepThread, func_0010678C, func_0010C894, func_00127520, func_00127EEC, func_0012CB00, func_001300B0, func_0013F29C, func_00171C78, func_0011054C) |
| **Complete functions (C + verified original library assembly)** | **20** / ~18,292 (0.11%) | Real C, plus library functions whose original source is assembly |
| **Real C-decompiled matched bytes** | **252** / 7,737,344 bytes (0.0033%) | Real-C-only byte progress; `asm_stubs/`, inline ASM and `scratches/` are excluded |
| **Inline ASM / ASM stub matched functions** | **0** / ~18,292 | ASM implementations: library assembly and authorized inline exceptions |
| **SDK / library byte-match identifications** | **0** / ~18,292 | CTR-SDK / Nintendo library functions identified separately |
| **Named / mapped candidates** | **21** / ~18,292 | Functions cataloged in scratches with isolated disassembly |
| **Initialized DATA** | Staged | `.rodata` / `.data` relocation and literal pool mapping |
| **Total known functions** | ~18,292 | Estimated function count for the EU target |
| **Region** | EU (`00040000001B2900`) | Multi-5 (PAL v1.0) |
| **Architecture** | ARM11 MPCore (ARMv6K) | 32-bit Little Endian, VMA `0x00100000` |
| **Compiler** | ARMCC / RVCT 4.x | Target toolchain identification under verification |

<!-- PROGRESS_STATS_END -->

---

### Progress reporting policy

Only real C implementations are counted as C-decompiled progress. Assembly, whether a library's own or an authorized inline exception, is counted separately, and so is anything under `scratches/` or unverified headers.

---

## Target Candidates & Current Manifest

<!-- MANIFEST_TABLE_START -->

| Virtual Address | Symbol / Name | Size (bytes) | Status | Description / Notes |
| :--- | :--- | :---: | :---: | :--- |
| `0x0010B6D0` | `func_0010B6D0` | 8 B | 🟢 Matched | Leaf identity stub (returns constant 0) |
| `0x0010B6D8` | `func_0010B6D8` | 12 B | 🟢 Matched | Global pointer getter via literal pool (0x008602F8) |
| `0x00104D18` | `func_00104D18` | 16 B | 🟢 Matched | Global 8-bit flag setter (0x00814E54) |
| `0x001063F4` | `func_001063F4` | 16 B | 🟢 Matched | CTR OS SystemConfig block field reader (0x1FF80000 + 0x40) |
| `0x00100024` | `clear_bss` | 36 B | 🟢 Matched | CRT startup zeroing loop for .bss section |
| `0x00104778` | `svcExitProcess` | 8 B | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x03) |
| `0x0010B6E4` | `func_0010B6E4` | 280 B | 🟡 In Review | C++ class method (partially decompiled, ~82% match in decomp.me) |
| `0x0017656C` | `func_0017656C` | 4 B | 🟢 Matched | Leaf empty void stub function |
| `0x00301248` | `func_00301248` | 4 B | 🟢 Matched | Leaf empty void stub function |
| `0x0012FEC0` | `func_0012FEC0` | 8 B | 🟢 Matched | Leaf boolean true stub (returns constant 1) |
| `0x00130018` | `func_00130018` | 8 B | 🟢 Matched | Leaf boolean true stub (returns constant 1) |
| `0x00151FBC` | `svcSleepThread` | 8 B | 🟢 Matched | CTR kernel syscall wrapper stub (svc 0x28) |
| `0x0010678C` | `func_0010678C` | 16 B | 🟢 Matched | Global signed byte reader via literal pool (0x00814E00) |
| `0x0010C894` | `func_0010C894` | 12 B | 🟢 Matched | Global pointer getter via literal pool (0x0086C8CC) |
| `0x00127520` | `func_00127520` | 12 B | 🟢 Matched | Global pointer getter via literal pool (0x005F32AC) |
| `0x00127EEC` | `func_00127EEC` | 12 B | 🟢 Matched | Global pointer getter via literal pool (0x00865F10) |
| `0x0012CB00` | `func_0012CB00` | 12 B | 🟢 Matched | Global pointer getter via literal pool (0x00868A9C) |
| `0x001300B0` | `func_001300B0` | 12 B | 🟢 Matched | Global pointer getter via literal pool (0x00868F10) |
| `0x0013F29C` | `func_0013F29C` | 12 B | 🟢 Matched | Global pointer getter via literal pool (0x00867DA8) |
| `0x00171C78` | `func_00171C78` | 12 B | 🟢 Matched | Global pointer getter via literal pool (0x0091B7B8) |
| `0x0011054C` | `func_0011054C` | 24 B | 🟢 Matched | Struct header reset (zeros 8 bytes, sets byte 0 to 0xFF) |

<!-- MANIFEST_TABLE_END -->

---

## Decompilation Roadmap (Candidate Tiers)

The following candidates are organized by complexity tier from [`config/functions_classified.csv`](config/functions_classified.csv) to guide progressive bottom-up matching:

### Tier 1: Trivial Stubs (4–8 bytes)
Leaf identity routines, constant return stubs, and CTR-SDK syscall wrappers:

| Virtual Address | Symbol | Size | Description |
| :--- | :--- | :---: | :--- |
| `0x0017656C` | `FUN_0017656c` | 4 B | Empty void stub function (`bx lr`) |
| `0x00301248` | `FUN_00301248` | 4 B | Empty void stub function (`bx lr`) |
| `0x0012FEC0` | `FUN_0012fec0` | 8 B | Boolean true stub (returns constant 1) |
| `0x00130018` | `FUN_00130018` | 8 B | Boolean true stub (returns constant 1) |
| `0x00151FBC` | `svcSleepThread` | 8 B | CTR kernel syscall wrapper stub (`svc 0x28`) |

### Tier 2: Accessors & Global Getters (12–16 bytes)
Single-field object readers and global pointer accessors via literal pools:

| Virtual Address | Symbol | Size | Description |
| :--- | :--- | :---: | :--- |
| `0x0010678C` | `FUN_0010678c` | 16 B | Global signed byte reader via literal pool (`0x00814E00`) |
| `0x0010C894` | `FUN_0010c894` | 12 B | Global pointer getter via literal pool (`0x0086C8CC`) |
| `0x00127520` | `FUN_00127520` | 12 B | Global pointer getter via literal pool (`0x005F32AC`) |
| `0x00127EEC` | `FUN_00127eec` | 12 B | Global pointer getter via literal pool (`0x00865F10`) |
| `0x0012CB00` | `FUN_0012cb00` | 12 B | Global pointer getter via literal pool (`0x00868A9C`) |
| `0x001300B0` | `FUN_001300b0` | 12 B | Global pointer getter via literal pool (`0x00868F10`) |
| `0x0013F29C` | `FUN_0013f29c` | 12 B | Global pointer getter via literal pool (`0x00867DA8`) |
| `0x00171C78` | `FUN_00171c78` | 12 B | Global pointer getter via literal pool (`0x0091B7B8`) |

### Tier 3: Arithmetic, Logic & Object Structures (24 bytes)
Local computations, atomic synchronizations, array indexers, and syscall wrappers:

| Virtual Address | Symbol | Size | Description |
| :--- | :--- | :---: | :--- |
| `0x0011054C` | `FUN_0011054c` | 24 B | Struct header reset (zeros 8 bytes, sets byte 0 to 0xFF) |
| `0x001274A0` | `FUN_001274a0` | 24 B | Atomic spinlock acquire loop (`ldrex/strex` synchronization) |
| `0x001280A8` | `FUN_001280a8` | 24 B | Bounds-checked array element indexer with stride 8 |
| `0x00137F28` | `FUN_00137f28` | 24 B | Conditional struct field pair store (offset `+0x14`) |
| `0x001386D4` | `FUN_001386d4` | 24 B | Pointer null-check and boolean flag tester |
| `0x0010AAA8` | `svcCreateEvent` | 24 B | CTR kernel syscall wrapper stub (`svc 0x21`) |
| `0x0010AAC0` | `svcDuplicateHandle` | 24 B | CTR kernel syscall wrapper stub (`svc 0x38`) |

### Tier 4: Wrappers & Forwarding Thunks (16 bytes)
Null-checked method forwarding wrappers and tail calls:

| Virtual Address | Symbol | Size | Description |
| :--- | :--- | :---: | :--- |
| `0x00130D38` | `FUN_00130d38` | 16 B | Null-checked method forwarding tail-call wrapper |
| `0x00340858` | `FUN_00340858` | 16 B | Null-checked method forwarding tail-call wrapper |

---

## Repository layout

```text
src/             reconstructed C/C++ source code achieving 100% byte-match
include/         shared headers: basic types, CTR-SDK declarations, game structures
asm/             disassembled stubs and un-decompiled assembly slices
config/          target identity, memory map, linker scripts (.ld), symbols (syms.txt)
scratches/       isolated function matching scratchpads and experiments
tools/           ROM extraction (extract_rom.py), disassembly, and verification scripts
docs/            target architecture, AAPCS conventions, and reverse-engineering notes
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
