# Yo-kai Watch 2: Psychic Specters — Decompilation

A work-in-progress matching decompilation of *Yo-kai Watch 2: Psychic Specters* (*Mentespectros / Shin'uchi*, Level-5, 2014–2017) for the Nintendo 3DS.

The goal is C source that recompiles to a binary byte-for-byte identical to the original game code.

Part of the **#DecompilandoEn358Dias** challenge.

---

## Disclaimer

This repository does **NOT** contain the game ROM, any game assets, or any of the original binary/assembly. An existing, legally-obtained copy of the game is required to extract and build it.

This repository is a **matching decompilation only**. It does not contain or produce a playable build or any redistributable game binary, and building it requires an original, legally-obtained copy of the game.

All trademarks, characters, and the original game are property of Level-5 Inc. and Nintendo.

---

## Status

Initial exploratory passes on the EU (`00040000001B2900`) ARM11 executable (`code.raw.bin`, 7,737,344 bytes, image base `0x00100000`).

The current objective is establishing a reproducible verification pipeline, matching the first batch of atomic leaf functions, and classifying library vs game engine routines.

Progress is split into categories so that assembly is never counted as C decompilation:

<!-- PROGRESS_STATS_START -->

| Category | Count | Meaning |
| :--- | :---: | :--- |
| **Real C-decompiled matched functions** | **6** / ~18,292 (0.03%) | Functions implemented in C and verified byte-exact (func_0010B6D0, func_0010B6D8, func_00104D18, func_001063F4, clear_bss, svcExitProcess) |
| **Complete functions (C + verified original library assembly)** | **6** / ~18,292 (0.03%) | Real C, plus library functions whose original source is assembly |
| **Real C-decompiled matched bytes** | **96** / 7,737,344 bytes (0.0012%) | Real-C-only byte progress; `asm_stubs/`, inline ASM and `scratches/` are excluded |
| **Inline ASM / ASM stub matched functions** | **0** / ~18,292 | ASM implementations: library assembly and authorized inline exceptions |
| **SDK / library byte-match identifications** | **0** / ~18,292 | CTR-SDK / Nintendo library functions identified separately |
| **Named / mapped candidates** | **7** / ~18,292 | Functions cataloged in scratches with isolated disassembly |
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

<!-- MANIFEST_TABLE_END -->

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
