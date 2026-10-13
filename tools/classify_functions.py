#!/usr/bin/env python3
"""
tools/classify_functions.py — Categorizes all functions in the catalog
by dependency (Leaf/Independent vs Non-Leaf) and difficulty level.
"""

import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
RAW_BIN = PROJECT_ROOT / "extracted" / "code.raw.bin"
IDENT_CSV = CONFIG_DIR / "ykw_2_identify_fuctions.csv"
OUT_CSV = CONFIG_DIR / "functions_classified.csv"
BASE_VMA = 0x00100000

def classify_catalog():
    if not RAW_BIN.exists():
        print(f"Error: {RAW_BIN} not found")
        return

    with open(RAW_BIN, "rb") as f:
        code = f.read()

    with open(IDENT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    classified = []

    for r in rows:
        try:
            addr = int(r["Location"], 16)
            size = int(r["Function Size"])
            name = r["Name"]
        except (ValueError, KeyError):
            continue

        if size < 4:
            continue

        offset = addr - BASE_VMA
        if offset < 0 or offset + size > len(code):
            continue

        fn_bytes = code[offset : offset + size]

        call_count = 0
        has_vtable = False
        has_loop = False

        for i in range(0, size - 3, 4):
            insn = int.from_bytes(fn_bytes[i:i+4], "little")
            
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
                # Sign extend 24-bit immediate
                if imm24 & 0x00800000:
                    offset_val = (imm24 - 0x01000000) * 4
                else:
                    offset_val = imm24 * 4
                target_addr = addr + i + 8 + offset_val
                
                # If target is outside the function, this is a tail call
                if not (addr <= target_addr < addr + size):
                    call_count += 1
                elif offset_val < 0:
                    has_loop = True

        is_leaf = (call_count == 0)

        # Determine difficulty level
        if is_leaf:
            if size <= 8:
                difficulty = "1_trivial"
                desc = "Constant return stub or leaf identity"
            elif size <= 20:
                difficulty = "2_simple_accessor"
                desc = "Single field getter/setter or global read"
            elif size <= 64:
                difficulty = "3_arithmetic_logic"
                desc = "Local arithmetic/bitwise computation"
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

        classified.append({
            "address": f"0x{addr:08X}",
            "symbol": name,
            "size": size,
            "is_leaf": "true" if is_leaf else "false",
            "calls": call_count,
            "has_vtable": "true" if has_vtable else "false",
            "has_loop": "true" if has_loop else "false",
            "difficulty": difficulty,
            "description": desc
        })

    # Sort: Leaf first, then by difficulty (1 to 7), then size, then address
    classified.sort(key=lambda x: (
        0 if x["is_leaf"] == "true" else 1,
        x["difficulty"],
        x["size"],
        int(x["address"], 16)
    ))

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["address", "symbol", "size", "is_leaf", "calls", "has_vtable", "has_loop", "difficulty", "description"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(classified)

    leaf_count = sum(1 for c in classified if c["is_leaf"] == "true")
    non_leaf_count = len(classified) - leaf_count

    print(f"Total cataloged functions: {len(classified)}")
    print(f" - Independent (Leaf) functions: {leaf_count}")
    print(f" - Dependent (Non-Leaf) functions: {non_leaf_count}")
    print(f"Output saved to: {OUT_CSV}")

if __name__ == "__main__":
    classify_catalog()
