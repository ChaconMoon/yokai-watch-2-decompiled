# Nintendo 3DS (ARM11 MPCore / RVCT 4.0 b821) ABI & Decompilation Patterns

This reference guide accompanies the `decomp-analysis` skill and can be reused across any Nintendo 3DS decompilation project.

---

## 1. ARMv6K / AAPCS Calling Convention (3DS Standard)

| Register | Role | Callee-Saved? | Notes |
| :--- | :--- | :---: | :--- |
| `r0` | Argument 0 / `this` pointer / Return value (32-bit) | No | In C++ non-static methods, `r0` is always `this`. |
| `r1` | Argument 1 / Return value high word (64-bit) | No | Used alongside `r0` for `u64` / `s64` returns. |
| `r2` | Argument 2 | No | Scratch register if not used as parameter. |
| `r3` | Argument 3 | No | Scratch register if not used as parameter. |
| `r4`–`r11` | Local variables (`v1`–`v8`) | **Yes** | Must be preserved across calls (`push {r4, ..., lr}`). |
| `r12` (`ip`) | Intra-procedure scratch register | No | Used by linker veneers and immediate calculations. |
| `r13` (`sp`) | Stack Pointer | **Yes** | 8-byte aligned at public function boundaries. |
| `r14` (`lr`) | Link Register | No | Holds return address; leaf functions return via `bx lr`. |
| `r15` (`pc`) | Program Counter | — | In ARM state, `[pc, #imm]` reads from `insn_addr + 8 + imm`. |

---

## 2. Canonical Fixed-Width Types (`include/types.h`)

Never use raw `int`, `short`, `char`, `unsigned int`, or `float` in decompiled headers or implementations. Always use the canonical 3DS types:

| ASM Load / Store | Width | Signedness | Canonical Type |
| :--- | :---: | :---: | :--- |
| `ldrb` / `strb` | 8-bit | Unsigned | `u8` (or `bool`) |
| `ldrsb` | 8-bit | Signed | `s8` |
| `ldrh` / `strh` | 16-bit | Unsigned | `u16` |
| `ldrsh` | 16-bit | Signed | `s16` |
| `ldr` / `str` | 32-bit | Unsigned / Signed / Pointer | `u32`, `s32`, or `Type *` |
| `ldrd` / `strd` | 64-bit | Unsigned / Signed | `u64` or `s64` |
| `vldr.32` / `vstr.32` | 32-bit | IEEE-754 Float | `f32` |
| `vldr.64` / `vstr.64` | 64-bit | IEEE-754 Double | `f64` |

---

## 3. ARMCC (RVCT 4.0 b821) C++ ABI & Mangling Rules

Nintendo 3DS SDK (`CTR-SDK`) and Level-5 titles compile C++ using **ARM C/C++ Compiler (RVCT 4.0)**, which follows the **Itanium C++ ABI** with 32-bit ARM specifics:

- **Prefix**: `_ZN` for nested names (`_ZNK` for `const` methods).
- **Namespace & Class Scopes**: Each identifier is prefixed by its decimal character length:
  - `nn::nex::StationConnectionInfo` $\rightarrow$ `2nn3nex21StationConnectionInfo`
- **Constructors & Destructors**:
  - `C1`: Complete object constructor (returns `this` in `r0` in ARM EABI).
  - `C2`: Base object subobject constructor.
  - `D0`: Deleting destructor (calls `operator delete`).
  - `D1`: Complete object destructor.
  - `D2`: Base object destructor.
- **Operators**:
  - `aS`: `operator=`
  - `eq`: `operator==`
  - `ne`: `operator!=`
  - `lt`: `operator<`
- **Substitution Compression**:
  - `S_`: First substitution entity (e.g., top-level namespace `nn`)
  - `S0_`: Second entity (e.g., `nn::nex`)
  - `S1_`: Third entity (e.g., `nn::nex::StationConnectionInfo`)
  - `RKS1_`: `const ClassName &` (`R` = reference, `K` = const, `S1_` = class type)

---

## 4. Common 3DS Memory Regions

| Address Range | Region | Description |
| :--- | :--- | :--- |
| `0x00100000` – `0x009FFFFF` | Process Image (`.text`, `.rodata`, `.data`, `.bss`) | Main executable mapped from ExeFS `code.bin`. |
| `0x08000000` – `0x0FFFFFFF` | Linear Heap / App Heap | Main application heap managed via `svcControlMemory`. |
| `0x1FF80000` – `0x1FF81FFF` | `CFG_MEM` (Shared Config Page) | Read-only kernel/OS configuration page (`nn::os`). |
| `0xFFFF8001` | `CUR_PROCESS_HANDLE` | Pseudo-handle for the current 3DS process. |
| `0xFFFF8000` | `CUR_THREAD_HANDLE` | Pseudo-handle for the current 3DS thread. |

