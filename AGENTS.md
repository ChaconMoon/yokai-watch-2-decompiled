# Instructions and Guidelines for Agents (AGENTS.md)

This repository is dedicated to the **matching decompilation** of *Yo-kai Watch 2: Psychic Specters* (*Mentespectros / Shin'uchi*) for the Nintendo 3DS (CTR).

---

## ⚠️ Strict User Rule (CRITICAL)

> **DO NOT return decompiled code (C / C++) to the user unless explicitly requested.**
> 
> - Do not write C reconstructions or pseudocode in responses unless the user expressly requests it (e.g., *"give me the C code for function X"*).
> - The agent's role must focus on:
>   - Explaining concepts and guiding workflows.
>   - Inspecting assembly, instructions, registers, and function calls via Ghidra / binutils.
>   - Dumping assembly (`tools/dump_asm.py`) formatted for `decomp.me`.
>   - Managing metrics, manifests (`config/functions.csv` / `config/functions_candidates.csv`), and repository tools.
>   - Assisting with compiler configurations, options, and flags.

### 📋 Required Format When Delivering Functions to Decompile

Whenever the user requests functions to decompile, deliver them one by one following this exact structure:

```markdown
### Function <N>: `<symbol_name>` (Address: `<0xADDRESS>`)
- **Size:** <N> bytes of code (+ <N> bytes of literal pool if applicable)
- **Type:** <Brief functional description: stub, global setter, offset read, virtual method call...>
- **Literal pool / Notes:** <Detail loaded RAM addresses, offsets, or constants>

```arm
<clean assembly instructions ready to paste into Target Assembly in decomp.me>
```
```

---

## Project Information & Architecture

- **Platform:** Nintendo 3DS (CTR)
- **Architecture:** ARM11 MPCore (`ARM:LE:32:v6` / ARMv6K, Little Endian)
- **Base Address (VMA):** `0x00100000`
- **Reference Binary:** `extracted/code.raw.bin` (7,737,344 bytes)
  - SHA-256 Hash: `b536dfce0a7138f2d5691532604d782b1ea3e20731120cc662baee118c370547`
- **Cataloged Functions:** 18,292 (detected via full analysis in Ghidra)
- **Target Compiler:** ARM C/C++ Compiler (ARMCC / RVCT 4.x / CTR-SDK 1.2.7)
- **Primary Game Language:** C++ (object-oriented, virtual vtables)

---

## Tooling & Environment

### 1. Ghidra & MCP Server
- **GhidraMCP** extension installed and listening at `http://127.0.0.1:8080/`.
- Enables querying Ghidra directly from the agent:
  - `get_program_info`
  - `disassemble_function`
  - `get_function_by_address`
  - `list_functions`, `list_segments`, `read_memory`, etc.

### 2. Local Scripts
- `tools/dump_asm.py`:
  - Dumps function disassembly with relative offsets from 0 or plain mode (`--plain`) to paste into `decomp.me`.
  - Supports ARM mode (default) and Thumb mode (`--thumb`).
- `tools/audit_progress.py`:
  - Reads candidate manifests and automatically updates `README.md` tables (`make progress`).
- `tools/extract_rom.py`:
  - Extracts and decompresses `code.raw.bin` from 3DS ROMs.
