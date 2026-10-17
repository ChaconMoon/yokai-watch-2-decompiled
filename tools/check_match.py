#!/usr/bin/env python3
"""
tools/check_match.py — Byte-exact matching verification tool
for Yo-kai Watch 2 (Nintendo 3DS).

Compares compiled ELF object files (.o) against the original retail
executable (extracted/code.raw.bin) at image base 0x00100000.
"""

import argparse
import csv
import os
import re
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASE_VMA = 0x00100000
RAW_BIN = PROJECT_ROOT / "extracted" / "code.raw.bin"
CONFIG_DIR = PROJECT_ROOT / "config"
BUILD_DIR = PROJECT_ROOT / "build"

MANIFEST_CSV = CONFIG_DIR / "functions.csv"
if not MANIFEST_CSV.exists() and (CONFIG_DIR / "functions_candidates.csv").exists():
    MANIFEST_CSV = CONFIG_DIR / "functions_candidates.csv"


def load_manifest(csv_path: Path):
    manifest = {}
    if not csv_path.exists():
        return manifest

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                addr = int(row["address"], 0)
                size = int(row["size"])
                manifest[row["symbol"]] = {
                    "address": addr,
                    "size": size,
                    "status": row.get("status", "staged"),
                    "description": row.get("description", "")
                }
            except (ValueError, KeyError):
                continue
    return manifest


def get_symbols_from_elf(obj_path: Path):
    """Parses FUNC symbols from ELF object file using arm-none-eabi-readelf."""
    cmd = ["arm-none-eabi-readelf", "-s", "-W", str(obj_path)]
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error running readelf on {obj_path}: {e}")
        return {}

    symbols = {}
    for line in out.splitlines():
        parts = line.strip().split()
        if len(parts) >= 8 and parts[3] == "FUNC":
            name = parts[7]
            try:
                val = int(parts[1], 16)
                size = int(parts[2])
                symbols[name] = {"offset": val, "size": size}
            except ValueError:
                continue
    return symbols


def get_relocations_from_elf(obj_path: Path):
    """Parses relocations from .rel.text or .rela.text using arm-none-eabi-readelf."""
    cmd = ["arm-none-eabi-readelf", "-r", "-W", str(obj_path)]
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error running readelf -r on {obj_path}: {e}")
        return []

    relocs = []
    for line in out.splitlines():
        parts = line.strip().split()
        if len(parts) >= 5 and "R_ARM_" in parts[2]:
            try:
                offset = int(parts[0], 16)
                rtype = parts[2]
                sym_name = parts[-1]
                relocs.append({
                    "offset": offset,
                    "type": rtype,
                    "symbol": sym_name
                })
            except ValueError:
                continue
    return relocs


def extract_section_bytes(obj_path: Path, section=".text"):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_name = tmp.name
    try:
        cmd = [
            "arm-none-eabi-objcopy",
            "-O", "binary",
            f"--only-section={section}",
            str(obj_path),
            tmp_name
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0 or not os.path.exists(tmp_name):
            return b""
        with open(tmp_name, "rb") as f:
            return f.read()
    finally:
        if os.path.exists(tmp_name):
            os.remove(tmp_name)


def main():
    parser = argparse.ArgumentParser(description="Verify compiled functions against code.raw.bin")
    parser.add_argument("--symbol", type=str, default=None, help="Check only specific symbol")
    args = parser.parse_args()

    if not RAW_BIN.exists():
        print("❌ Error: 'extracted/code.raw.bin' not found.")
        print("   Run 'make extract' with a decrypted ROM to extract the reference binary.")
        return 1

    manifest = load_manifest(MANIFEST_CSV)
    if not manifest:
        print(f"⚠️ Warning: Manifest not found at {MANIFEST_CSV}")

    obj_files = list(BUILD_DIR.rglob("*.o"))
    if not obj_files:
        print("⚠️ No compiled objects found in 'build/'.")
        print("   Run 'make build/src/system/func_0010B6D0.o' or similar first.")
        return 1

    with open(RAW_BIN, "rb") as f:
        raw_bytes = f.read()

    print("============================================================")
    print("  Yo-kai Watch 2 (3DS) — Byte-Exact Verification Auditor")
    print("============================================================")

    matched_count = 0
    staged_count = 0
    mismatched_count = 0
    checked_symbols = set()

    for obj in sorted(obj_files):
        symbols = get_symbols_from_elf(obj)
        if not symbols:
            continue

        relocs = get_relocations_from_elf(obj)
        text_bytes = extract_section_bytes(obj, ".text")

        for sym, sym_info in symbols.items():
            if "$$" in sym or sym.startswith("__arm_cp"):
                continue
            if args.symbol and sym != args.symbol:
                continue

            checked_symbols.add(sym)
            meta = manifest.get(sym)

            if not meta:
                m = re.match(r"func_([0-9a-fA-F]{8})", sym)
                if m:
                    addr = int(m.group(1), 16)
                    size = sym_info["size"]
                else:
                    print(f"  ⚠️ Skipping {sym}: not in manifest and no address in name")
                    continue
            else:
                addr = meta["address"]
                size = meta["size"]

            raw_offset = addr - BASE_VMA
            if raw_offset < 0 or raw_offset + size > len(raw_bytes):
                print(f"  ❌ {sym}: Address 0x{addr:08X} out of binary bounds!")
                mismatched_count += 1
                continue

            expected_slice = raw_bytes[raw_offset : raw_offset + size]

            obj_off = sym_info["offset"]
            obj_size = sym_info["size"]
            actual_slice = text_bytes[obj_off : obj_off + obj_size]

            comp_len = min(len(expected_slice), len(actual_slice))

            # Identify relocations belonging to this function
            fn_relocs = [r for r in relocs if obj_off <= r["offset"] < obj_off + obj_size]
            reloc_byte_indices = set()
            reloc_details = []
            for r in fn_relocs:
                rel_off = r["offset"] - obj_off
                if r["type"] == "R_ARM_ABS32":
                    for b in range(4):
                        reloc_byte_indices.add(rel_off + b)
                    if rel_off + 4 <= len(expected_slice):
                        target_addr = struct.unpack_from("<I", expected_slice, rel_off)[0]
                        reloc_details.append(f"{r['symbol']} -> 0x{target_addr:08X}")
                    else:
                        reloc_details.append(r["symbol"])

            # Verify non-relocation bytes match byte-for-byte
            code_diffs = [
                i for i in range(comp_len)
                if i not in reloc_byte_indices and expected_slice[i] != actual_slice[i]
            ]
            length_match = (len(expected_slice) == len(actual_slice))
            is_match = length_match and (len(code_diffs) == 0)
            status = meta.get("status", "staged").lower() if meta else "staged"
            is_staged = status in ("staged", "wip", "in_progress")

            if is_match:
                matched_count += 1
                detail_str = ""
                if reloc_details:
                    detail_str = f" [reloc: {', '.join(reloc_details)}]"
                staged_note = " \033[96m(ready to promote to matched!)\033[0m" if is_staged else ""
                print(f"  \033[92m>>> MATCH <<<\033[0m: {sym} (0x{addr:08X}) — {size} B identical{detail_str}{staged_note}")
            elif is_staged:
                staged_count += 1
                diff_count = len(code_diffs) + abs(len(expected_slice) - len(actual_slice))
                print(f"  \033[93m>>> STAGED (WIP) <<<\033[0m: {sym} (0x{addr:08X}) — {diff_count} byte(s) diff [in development]")
            else:
                mismatched_count += 1
                diff_count = len(code_diffs) + abs(len(expected_slice) - len(actual_slice))
                print(f"  \033[91m>>> REGRESSION / MISMATCH <<<\033[0m: {sym} (0x{addr:08X})")
                print(f"      Expected ({len(expected_slice)} B): {expected_slice[:16].hex()}...")
                print(f"      Compiled ({len(actual_slice)} B): {actual_slice[:16].hex()}...")
                print(f"      Differences: {diff_count} byte(s)")

    print("============================================================")
    summary_parts = [f"{matched_count} matched"]
    if staged_count > 0:
        summary_parts.append(f"{staged_count} staged (WIP)")
    summary_parts.append(f"{mismatched_count} regressed")
    print(f"  Results: {', '.join(summary_parts)}")
    print("============================================================")

    pending = [s for s, m in manifest.items() if s not in checked_symbols and m["status"].lower() != "matched"]
    if pending:
        print(f"  Pending candidates ({len(pending)}):")
        for s in pending[:5]:
            print(f"    ⏳ {s} (0x{manifest[s]['address']:08X}) — {manifest[s]['size']} B")
        if len(pending) > 5:
            print(f"    ... and {len(pending) - 5} more")
        print("============================================================")

    return 1 if mismatched_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
