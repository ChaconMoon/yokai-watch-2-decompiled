#!/usr/bin/env python3
"""
tools/extract_ctr_stubs.py — Automated extraction of CTR-SDK core stubs (.s)
for Yo-kai Watch 2 (Nintendo 3DS).

Extracts and verifies modular assembly stubs (.s) for core Layer 1 subsystems:
  - src/ctr/svc/   (Supervisor calls)
  - src/ctr/nn/os/ (Operating System)
  - src/ctr/crt/   (C Runtime & startup)
  - src/ctr/nn/dsp/(Audio DSP)

Follows the "Split & Replace" methodology (khdays-decomp): every stub is
verified byte-exact against extracted/code.raw.bin upon extraction.
"""

import csv
import os
import re
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_BIN = PROJECT_ROOT / "extracted" / "code.raw.bin"
CONFIG_DIR = PROJECT_ROOT / "config"
CLASSIFIED_CSV = CONFIG_DIR / "functions_classified.csv"
FUNCTIONS_CSV = CONFIG_DIR / "functions.csv"

sys.path.append(str(PROJECT_ROOT / "tools"))
import check_match

CONDITIONS = ["eq", "ne", "cs", "cc", "mi", "pl", "vs", "vc", "hi", "ls", "ge", "lt", "gt", "le"]

def fix_arm_ual(line):
    parts = line.split(maxsplit=1)
    if not parts:
        return line
    op = parts[0].lower()
    rest = parts[1] if len(parts) > 1 else ""

    for cond in CONDITIONS:
        for base in ["mov", "sub", "add", "and", "orr", "eor", "lsl", "lsr", "asr", "ror", "bic", "adc", "sbc", "rsb"]:
            if op == f"{base}s{cond}":
                op = f"{base}{cond}s"
                return f"    {op} {rest}"
        for base in ["ldr", "str"]:
            for sz in ["h", "sh", "b", "sb", "d"]:
                if op == f"{base}{sz}{cond}":
                    op = f"{base}{cond}{sz}"
                    return f"    {op} {rest}"
        for base in ["ldm", "stm"]:
            for mode in ["ia", "ib", "da", "db"]:
                if op == f"{base}{mode}{cond}":
                    op = f"{base}{cond}{mode}"
                    return f"    {op} {rest}"
    return line


def get_subsystem_dir(subsystem):
    if subsystem == "svc":
        return PROJECT_ROOT / "asm" / "ctr" / "svc"
    elif subsystem == "crt":
        return PROJECT_ROOT / "asm" / "ctr" / "crt"
    elif subsystem == "nn_os":
        return PROJECT_ROOT / "asm" / "ctr" / "nn" / "os"
    elif subsystem == "nn_dsp":
        return PROJECT_ROOT / "asm" / "ctr" / "nn" / "dsp"
    elif subsystem == "nn_y2r":
        return PROJECT_ROOT / "asm" / "ctr" / "nn" / "y2r"
    elif subsystem == "nn_applet":
        return PROJECT_ROOT / "asm" / "ctr" / "nn" / "applet"
    elif subsystem == "nn_ndm":
        return PROJECT_ROOT / "asm" / "ctr" / "nn" / "ndm"
    elif subsystem == "nn_math":
        return PROJECT_ROOT / "asm" / "ctr" / "nn" / "math"
    else:
        return PROJECT_ROOT / "asm" / "ctr" / "nn" / subsystem.replace("nn_", "")


def assemble_and_verify(s_content, addr, size, raw_bytes):
    with tempfile.NamedTemporaryFile("w", suffix=".s", delete=False) as tf:
        tf.write(s_content)
        s_path = tf.name

    o_path = s_path + ".o"
    try:
        as_res = subprocess.run(
            ["arm-none-eabi-as", "-mcpu=mpcore", "-mfpu=vfpv2", s_path, "-o", o_path],
            capture_output=True,
            text=True
        )
        if as_res.returncode != 0:
            return False, as_res.stderr.strip()

        actual = check_match.extract_section_bytes(Path(o_path))
        raw_offset = addr - 0x00100000
        expected = raw_bytes[raw_offset : raw_offset + size]

        relocs = check_match.get_relocations_from_elf(Path(o_path))
        reloc_bytes = set()
        for r in relocs:
            for b in range(4):
                reloc_bytes.add(r["offset"] + b)

        comp_len = min(len(actual), len(expected))
        diffs = [
            i for i in range(comp_len)
            if i not in reloc_bytes and actual[i] != expected[i]
        ]
        is_ok = (len(actual) == len(expected)) and (len(diffs) == 0)
        return is_ok, f"{len(diffs)} byte differences" if not is_ok else "ok"
    finally:
        Path(s_path).unlink(missing_ok=True)
        Path(o_path).unlink(missing_ok=True)


def build_byte_fallback(sym, addr, size, desc, raw_bytes):
    raw_offset = addr - 0x00100000
    slice_bytes = raw_bytes[raw_offset : raw_offset + size]
    
    # Format into .word directives if multiple of 4, else .byte
    body_lines = []
    if size % 4 == 0:
        for i in range(0, size, 4):
            w = struct.unpack_from("<I", slice_bytes, i)[0]
            body_lines.append(f"    .word 0x{w:08X}")
    else:
        for i in range(0, size, 16):
            chunk = slice_bytes[i : i + 16]
            hex_str = ", ".join(f"0x{b:02X}" for b in chunk)
            body_lines.append(f"    .byte {hex_str}")

    return f"""/*
 * @brief {sym}
 * @address 0x{addr:08X}
 * {desc}
 */
    .arm
    .section .text
    .global {sym}
    .type {sym}, %function

{sym}:
""" + "\n".join(body_lines) + f"""

    .size {sym}, . - {sym}
"""


def extract_subsystems(target_subsystems):
    if not RAW_BIN.exists():
        print(f"❌ Error: {RAW_BIN} not found.", file=sys.stderr)
        return 1

    with open(RAW_BIN, "rb") as f:
        raw_bytes = f.read()

    # Load existing symbols in src/
    src_dir = PROJECT_ROOT / "src"
    existing_files = {p.stem: p for p in src_dir.rglob("*.*")}

    # Read classified functions
    with open(CLASSIFIED_CSV, "r", encoding="utf-8") as f:
        classified = list(csv.DictReader(f))

    # Read existing manifest
    manifest_rows = []
    manifest_symbols = set()
    if FUNCTIONS_CSV.exists():
        with open(FUNCTIONS_CSV, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                manifest_rows.append(row)
                manifest_symbols.add(row["symbol"])

    to_process = [
        r for r in classified
        if r["layer"] == "ctr" and r["subsystem"] in target_subsystems
    ]

    print(f"Targeting subsystems: {', '.join(target_subsystems)}")
    print(f"Total candidate functions: {len(to_process)}")

    extracted_count = 0
    clean_asm_count = 0
    fallback_count = 0
    skipped_count = 0

    for f in to_process:
        addr = int(f["address"], 16)
        size = int(f["size"])
        sub = f["subsystem"]
        sym = f["symbol"]
        desc = f.get("description", "CTR-SDK routine")
        lvl = f.get("difficulty", "1_trivial")

        if sym.startswith("FUN_"):
            sym = f"func_{addr:08X}"

        # Check if already present
        if sym in existing_files or f"func_{addr:08X}" in existing_files:
            skipped_count += 1
            continue

        target_dir = get_subsystem_dir(sub)
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / f"{sym}.s"

        # 1. Try dumping clean assembly
        dump_cmd = [
            sys.executable,
            str(PROJECT_ROOT / "tools" / "dump_asm.py"),
            f"0x{addr:08X}",
            str(size),
            "--plain",
            "--symbol",
            sym
        ]
        res = subprocess.run(dump_cmd, capture_output=True, text=True)
        s_content = None

        if res.returncode == 0:
            norm_lines = []
            for line in res.stdout.splitlines():
                line = fix_arm_ual(line)
                if line.strip() == "nop":
                    norm_lines.append("    mov r0, r0")
                else:
                    norm_lines.append(line)

            candidate_s = f"""/*
 * @brief {sym}
 * @address 0x{addr:08X}
 * {desc}
 */
    .arm
    .section .text
    .global {sym}
    .type {sym}, %function

{sym}:
""" + "\n".join(norm_lines) + f"""

    .size {sym}, . - {sym}
"""
            ok, msg = assemble_and_verify(candidate_s, addr, size, raw_bytes)
            if ok:
                s_content = candidate_s
                clean_asm_count += 1

        # 2. If clean assembly failed or mismatched, use byte-exact fallback
        if s_content is None:
            s_content = build_byte_fallback(sym, addr, size, desc, raw_bytes)
            ok, msg = assemble_and_verify(s_content, addr, size, raw_bytes)
            if not ok:
                print(f"❌ Critical error assembling fallback for {sym} ({addr:08X}): {msg}")
                continue
            fallback_count += 1

        target_file.write_text(s_content, encoding="utf-8")
        extracted_count += 1
        existing_files[sym] = target_file

        # Add to manifest
        if sym not in manifest_symbols:
            manifest_rows.append({
                "address": f"0x{addr:08X}",
                "symbol": sym,
                "size": str(size),
                "layer": "ctr",
                "subsystem": sub,
                "level": lvl,
                "status": "asm_stub",
                "description": desc
            })
            manifest_symbols.add(sym)

    # Sort manifest by address
    manifest_rows.sort(key=lambda r: int(r["address"], 16))

    with open(FUNCTIONS_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["address", "symbol", "size", "layer", "subsystem", "level", "status", "description"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(manifest_rows)

    print("============================================================")
    print("  CTR-SDK Core Stubs Extraction Summary")
    print("============================================================")
    print(f"  Total processed  : {extracted_count + skipped_count}")
    print(f"  Already existing : {skipped_count}")
    print(f"  Newly extracted  : {extracted_count}")
    print(f"   ├─ Clean asm    : {clean_asm_count}")
    print(f"   └─ Byte-exact fb: {fallback_count}")
    print("============================================================")
    return 0


if __name__ == "__main__":
    targets = ["svc", "nn_os", "crt", "nn_dsp"]
    if len(sys.argv) > 1:
        targets = sys.argv[1:]
    sys.exit(extract_subsystems(targets))

