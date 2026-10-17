#!/usr/bin/env python3
"""
tools/classify_functions.py — Categorizes all valid .text functions in the catalog
by Architectural Layer (Nintendo CTR-SDK, Level-5 Engine, Yo-kai Watch 2 Game),
Subsystem, Dependency (Leaf vs Non-Leaf), and Didactic Difficulty Level.

Also cleans false-positive functions outside the ExHeader .text segment
(0x00100000 - 0x006F32AC).
"""

import csv
import struct
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
RAW_BIN = PROJECT_ROOT / "extracted" / "code.raw.bin"
IDENT_CSV = CONFIG_DIR / "ykw_2_identify_fuctions.csv"
OUT_CSV = CONFIG_DIR / "functions_classified.csv"

BASE_VMA = 0x00100000
TEXT_END_VMA = 0x006F32AC  # Exact .text end from NCCH ExHeader


def infer_layer_and_subsystem(addr: int, name: str, has_svc: bool, calls_1ff8: bool) -> tuple[str, str]:
    """
    Assigns a function to one of the 3 core architectural layers:
      - 'ctr':    Nintendo CTR-SDK & ARM C/C++ Runtime
      - 'engine': Level-5 Proprietary Engine (lfw, lxp, gds)
      - 'game':   Yo-kai Watch 2 Game Logic (yw2)
    """
    low_name = name.lower()
    if low_name.startswith("svc") or has_svc:
        return ("ctr", "svc")
    if calls_1ff8:
        return ("ctr", "nn_os")

    # 1. Early CRT Startup & ARM C/C++ Runtime (Thumb / AEABI) + CTR-SDK core init
    if 0x00100000 <= addr < 0x00104770:
        return ("ctr", "crt")
    if 0x00104770 <= addr < 0x00107400:
        return ("ctr", "nn_os")

    # 2. Level-5 Framework Base Loop (lfwCLoopEmpty) vs Yo-kai Watch 2 Loops (ywCLoop*)
    if 0x0010B500 <= addr < 0x0010C800:
        return ("engine", "lfw")
    if 0x0010C800 <= addr < 0x00112500:
        return ("game", "loops")

    # 3. CTR-SDK Hardware & OS Services (y2r, camera, ndm, synchronization)
    if 0x00112500 <= addr < 0x00114000:
        return ("ctr", "nn_y2r")
    if 0x00124000 <= addr < 0x00126800:
        return ("engine", "lfw")
    if 0x00127000 <= addr < 0x00128500:
        return ("ctr", "nn_os")

    # 4. Level-5 Cross-Platform (lxpCMemory, containers, allocators)
    if 0x0012A000 <= addr < 0x00136000:
        return ("engine", "lxp")

    # 5. CTR-SDK Audio / DSP / SRV / Kernel wrappers
    if 0x00136000 <= addr < 0x00139000:
        return ("ctr", "nn_dsp")
    if 0x00139000 <= addr < 0x00142000:
        return ("engine", "core")
    if 0x00151000 <= addr < 0x00153000:
        return ("ctr", "svc")

    # 6. Level-5 Engine Middleware (lxpCStack, FA archives, rendering)
    if 0x00200000 <= addr < 0x00260000:
        return ("engine", "lxp")

    # 7. CTR-SDK System Applets, AM, NIM, CECD & NEX Networking
    if 0x00280000 <= addr < 0x00300000:
        return ("ctr", "nn_cecd")
    if 0x00300000 <= addr < 0x00370000:
        return ("ctr", "nn_nex")

    # 8. Level-5 GDS Script & Resource Configs vs Game Logic
    if 0x00580000 <= addr < TEXT_END_VMA:
        return ("engine", "core")

    return ("game", "core")


def classify_catalog():
    if not RAW_BIN.exists():
        print(f"Error: {RAW_BIN} not found")
        return

    with open(RAW_BIN, "rb") as f:
        code = f.read()

    with open(IDENT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames_ident = reader.fieldnames
        rows = list(reader)

    valid_ident_rows = []
    classified = []
    removed_rodata_count = 0

    for r in rows:
        try:
            addr = int(r["Location"], 16)
            size = int(r["Function Size"])
            name = r["Name"]
        except (ValueError, KeyError):
            continue

        # Filter out false positives in .rodata / .data (>= 0x006F32AC)
        if addr < BASE_VMA or addr >= TEXT_END_VMA:
            removed_rodata_count += 1
            continue

        valid_ident_rows.append(r)

        if size < 4:
            continue

        offset = addr - BASE_VMA
        if offset < 0 or offset + size > len(code):
            continue

        fn_bytes = code[offset : offset + size]

        call_count = 0
        has_vtable = False
        has_loop = False
        has_svc = False
        calls_1ff8 = False

        for i in range(0, size - 3, 4):
            insn = struct.unpack_from("<I", fn_bytes, i)[0]

            # Unconditional SVC: 0xEF0000xx (with syscall <= 0x80)
            if (insn & 0xFFFFFF00) == 0xEF000000 and (insn & 0xFF) <= 0x80 and size <= 36:
                has_svc = True

            # Check literal pool reference to 0x1FF80000
            if (insn & 0xFFFF0000) == 0x1FF80000:
                calls_1ff8 = True

            # bl in ARM: (insn >> 24) & 0x0F == 0x0B
            if (insn >> 24) & 0x0F == 0x0B:
                call_count += 1
            # blx imm (0xFA/0xFB)
            elif (insn >> 24) in (0xFA, 0xFB):
                call_count += 1
            # blx reg: 0x012fff3x
            elif (insn & 0x0FFFFFF0) == 0x012FFF30:
                call_count += 1
                has_vtable = True

            # Detect branches (b / b<cond>)
            if (insn >> 24) & 0x0E == 0x0A:
                imm24 = insn & 0x00FFFFFF
                if imm24 & 0x00800000:
                    offset_val = (imm24 - 0x01000000) * 4
                else:
                    offset_val = imm24 * 4
                target_addr = addr + i + 8 + offset_val

                if not (addr <= target_addr < addr + size):
                    call_count += 1
                elif offset_val < 0:
                    has_loop = True

        is_leaf = (call_count == 0)

        if is_leaf:
            if size <= 8:
                difficulty = "1_trivial"
                desc = "Constant return stub or leaf identity" if not has_svc else "CTR kernel syscall wrapper stub"
            elif size <= 20:
                difficulty = "2_simple_accessor"
                desc = "Single field getter/setter or global read"
            elif size <= 64:
                difficulty = "3_arithmetic_logic"
                desc = "Local arithmetic/bitwise computation" if not has_svc else "CTR kernel syscall wrapper"
            else:
                difficulty = "4_complex_leaf"
                desc = "Large leaf algorithm" + (" with loop" if has_loop else "")
        else:
            if call_count == 1:
                difficulty = "5_simple_wrapper"
                desc = "Single function call wrapper / thunk"
            elif call_count <= 3 and not has_vtable:
                difficulty = "6_moderate_caller"
                desc = f"Moderate caller ({call_count} subcalls)"
            else:
                difficulty = "7_complex_caller"
                desc = f"Complex caller ({call_count} calls" + (", vtable" if has_vtable else "") + ")"

        layer, subsystem = infer_layer_and_subsystem(addr, name, has_svc, calls_1ff8)

        classified.append({
            "address": f"0x{addr:08X}",
            "symbol": name,
            "size": size,
            "layer": layer,
            "subsystem": subsystem,
            "is_leaf": "true" if is_leaf else "false",
            "calls": call_count,
            "has_vtable": "true" if has_vtable else "false",
            "has_loop": "true" if has_loop else "false",
            "difficulty": difficulty,
            "description": desc
        })

    # Clean ykw_2_identify_fuctions.csv if any false-positive .rodata rows were present
    if removed_rodata_count > 0 and fieldnames_ident:
        with open(IDENT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames_ident)
            writer.writeheader()
            writer.writerows(valid_ident_rows)
        print(f"Cleaned {removed_rodata_count} false-positive .rodata entries from {IDENT_CSV.name}")

    # Sort by Layer (ctr -> engine -> game), then Leaf first, then difficulty, then size, then address
    layer_order = {"ctr": 0, "engine": 1, "game": 2}
    classified.sort(key=lambda x: (
        layer_order.get(x["layer"], 9),
        0 if x["is_leaf"] == "true" else 1,
        x["difficulty"],
        x["size"],
        int(x["address"], 16)
    ))

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "address", "symbol", "size", "layer", "subsystem",
            "is_leaf", "calls", "has_vtable", "has_loop", "difficulty", "description"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(classified)

    leaf_count = sum(1 for c in classified if c["is_leaf"] == "true")
    non_leaf_count = len(classified) - leaf_count
    by_layer = {}
    for c in classified:
        by_layer[c["layer"]] = by_layer.get(c["layer"], 0) + 1

    print(f"Total valid .text functions cataloged: {len(classified)} (in 0x00100000 - 0x006F32AC)")
    print(f" - Nintendo CTR-SDK & Runtime (ctr): {by_layer.get('ctr', 0):,}")
    print(f" - Level-5 Engine (engine)         : {by_layer.get('engine', 0):,}")
    print(f" - Yo-kai Watch 2 Game (game)      : {by_layer.get('game', 0):,}")
    print(f" - Independent (Leaf) functions    : {leaf_count:,}")
    print(f" - Dependent (Non-Leaf) functions  : {non_leaf_count:,}")
    print(f"Output saved to: {OUT_CSV}")


if __name__ == "__main__":
    classify_catalog()
