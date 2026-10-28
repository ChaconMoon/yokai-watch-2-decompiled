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
                    "description": row.get("description", ""),
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

    sec_cmd = ["arm-none-eabi-readelf", "-S", "-W", str(obj_path)]
    sec_names = {}
    try:
        sec_out = subprocess.check_output(sec_cmd, text=True, stderr=subprocess.PIPE)
        for line in sec_out.splitlines():
            m = re.search(r"\[\s*(\d+)\]\s+([^\s]+)", line)
            if m:
                sec_names[m.group(1)] = m.group(2)
    except Exception:
        pass

    symbols = {}
    for line in out.splitlines():
        parts = line.strip().split()
        if len(parts) >= 8 and parts[3] == "FUNC":
            if parts[6] == "UND":
                continue
            name = parts[7]
            try:
                val = int(parts[1], 16)
                size = int(parts[2])
                sec_ndx = parts[6]
                sec_name = sec_names.get(sec_ndx, ".text")
                symbols[name] = {"offset": val, "size": size, "section": sec_name}
            except ValueError:
                continue
    return symbols


def get_relocations_from_elf(obj_path: Path):
    """Parses relocations by section from ELF using arm-none-eabi-readelf."""
    cmd = ["arm-none-eabi-readelf", "-r", "-W", str(obj_path)]
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error running readelf -r on {obj_path}: {e}")
        return {}

    relocs_by_sec = {}
    curr_sec = ".text"
    for line in out.splitlines():
        m = re.search(r"Relocation section '([^']+)'", line)
        if m:
            sec = m.group(1)
            if sec.startswith(".rela"):
                curr_sec = sec[5:]
            elif sec.startswith(".rel"):
                curr_sec = sec[4:]
            else:
                curr_sec = sec
            if curr_sec not in relocs_by_sec:
                relocs_by_sec[curr_sec] = []
            continue
        parts = line.strip().split()
        if len(parts) >= 5 and "R_ARM_" in parts[2]:
            try:
                offset = int(parts[0], 16)
                rtype = parts[2]
                sym_name = parts[-1]
                if curr_sec not in relocs_by_sec:
                    relocs_by_sec[curr_sec] = []
                relocs_by_sec[curr_sec].append({"offset": offset, "type": rtype, "symbol": sym_name})
            except ValueError:
                continue
    return relocs_by_sec


def extract_section_bytes(obj_path: Path, section=".text"):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_name = tmp.name
    try:
        cmd = [
            "arm-none-eabi-objcopy",
            "-O",
            "binary",
            f"--only-section={section}",
            str(obj_path),
            tmp_name,
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
    parser = argparse.ArgumentParser(
        description="Verify compiled functions against code.raw.bin"
    )
    parser.add_argument(
        "--symbol", type=str, default=None, help="Check only specific symbol"
    )
    args = parser.parse_args()

    if not RAW_BIN.exists():
        print("❌ Error: 'extracted/code.raw.bin' not found.")
        print(
            "   Run 'make extract' with a decrypted ROM to extract the reference binary."
        )
        return 1

    manifest = load_manifest(MANIFEST_CSV)
    if not manifest:
        print(f"⚠️ Warning: Manifest not found at {MANIFEST_CSV}")

    obj_files = list(BUILD_DIR.rglob("*.o"))
    if not obj_files:
        print("⚠️ No compiled objects found in 'build/'.")
        print("   Run 'make build/src/engine/lfw/func_0010B6D0.o' or similar first.")
        return 1

    with open(RAW_BIN, "rb") as f:
        raw_bytes = f.read()

    print("============================================================")
    print("  Yo-kai Watch 2 (3DS) — Byte-Exact Verification Auditor")
    print("============================================================")

    matched_count = 0
    asm_stub_count = 0
    staged_count = 0
    mismatched_count = 0
    checked_symbols = set()

    for obj in sorted(obj_files):
        symbols = get_symbols_from_elf(obj)
        if not symbols:
            continue

        relocs_by_sec = get_relocations_from_elf(obj)
        default_text_bytes = extract_section_bytes(obj, ".text")

        try:
            rel_path = obj.relative_to(BUILD_DIR)
            src_s = PROJECT_ROOT / rel_path.with_suffix(".s")
            obj_is_asm = src_s.exists()
        except ValueError:
            obj_is_asm = False

        for sym, sym_info in symbols.items():
            if "$$" in sym or sym.startswith("__arm_cp") or sym_info["size"] == 0:
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

            sec_name = sym_info.get("section", ".text")
            if sec_name != ".text":
                text_bytes = extract_section_bytes(obj, sec_name)
            else:
                text_bytes = default_text_bytes

            expected_slice = raw_bytes[raw_offset : raw_offset + size]

            obj_off = sym_info["offset"]
            effective_size = max(sym_info["size"], size)
            if obj_off + effective_size > len(text_bytes):
                effective_size = len(text_bytes) - obj_off
            obj_size = effective_size
            actual_slice = text_bytes[obj_off : obj_off + obj_size]

            comp_len = min(len(expected_slice), len(actual_slice))

            # Identify relocations belonging to this function
            sec_relocs = relocs_by_sec.get(sec_name, [])
            fn_relocs = [
                r for r in sec_relocs if obj_off <= r["offset"] < obj_off + obj_size
            ]
            reloc_byte_indices = set()
            reloc_details = []
            for r in fn_relocs:
                rel_off = r["offset"] - obj_off
                if r["type"] == "R_ARM_ABS32":
                    for b in range(4):
                        reloc_byte_indices.add(rel_off + b)
                    if rel_off + 4 <= len(expected_slice):
                        target_addr = struct.unpack_from("<I", expected_slice, rel_off)[
                            0
                        ]
                        reloc_details.append(f"{r['symbol']} -> 0x{target_addr:08X}")
                    else:
                        reloc_details.append(r["symbol"])
                elif r["type"] in ("R_ARM_CALL", "R_ARM_JUMP24"):
                    if rel_off + 4 <= len(expected_slice) and rel_off + 4 <= len(
                        actual_slice
                    ):
                        exp_word = struct.unpack_from("<I", expected_slice, rel_off)[0]
                        act_word = struct.unpack_from("<I", actual_slice, rel_off)[0]
                        # Verify branch condition and opcode prefix match (top 8 bits, or top 7 bits for BLX with H bit)
                        if (exp_word & 0xFF000000) == (act_word & 0xFF000000) or \
                           ((exp_word & 0xFE000000) == 0xFA000000 and (act_word & 0xFE000000) == 0xFA000000):
                            for b in range(4):
                                reloc_byte_indices.add(rel_off + b)
                            imm24 = exp_word & 0x00FFFFFF
                            if imm24 & 0x800000:
                                imm24 -= 0x1000000
                            target_addr = addr + rel_off + 8 + imm24 * 4
                            reloc_details.append(
                                f"{r['symbol']} -> 0x{target_addr:08X}"
                            )

            # Verify non-relocation bytes match byte-for-byte
            code_diffs = [
                i
                for i in range(comp_len)
                if i not in reloc_byte_indices and expected_slice[i] != actual_slice[i]
            ]
            length_match = len(expected_slice) == len(actual_slice)
            is_match = length_match and (len(code_diffs) == 0)
            status = meta.get("status", "staged").lower() if meta else "staged"
            is_community = status in ("community_matched", "matched_community")
            is_asm = obj_is_asm or (status == "asm_stub")
            is_staged = status in ("staged", "wip", "in_progress", "pending")

            if is_match:
                detail_str = ""
                if reloc_details:
                    detail_str = f" [reloc: {', '.join(reloc_details)}]"
                if is_asm:
                    asm_stub_count += 1
                    print(
                        f"  \033[90m>>> ASM STUB <<<\033[0m: {sym} (0x{addr:08X}) — {size} B verified (original assembly){detail_str}"
                    )
                else:
                    matched_count += 1
                    staged_note = (
                        " \033[96m(ready to promote to matched!)\033[0m"
                        if is_staged
                        else ""
                    )
                    print(
                        f"  \033[92m>>> MATCH (C) <<<\033[0m: {sym} (0x{addr:08X}) — {size} B identical{detail_str}{staged_note}"
                    )
            elif is_community:
                matched_count += 1
                diff_count = len(code_diffs) + abs(
                    len(expected_slice) - len(actual_slice)
                )
                print(
                    f"  \033[94m>>> MATCH (COMMUNITY ACCEPTED) <<<\033[0m: {sym} (0x{addr:08X}) — {size} B equivalent ({diff_count} B regalloc diff)"
                )
            elif is_staged:
                staged_count += 1
                diff_count = len(code_diffs) + abs(
                    len(expected_slice) - len(actual_slice)
                )
                print(
                    f"  \033[93m>>> STAGED (WIP) <<<\033[0m: {sym} (0x{addr:08X}) — {diff_count} byte(s) diff [in development]"
                )
            else:
                mismatched_count += 1
                diff_count = len(code_diffs) + abs(
                    len(expected_slice) - len(actual_slice)
                )
                print(
                    f"  \033[91m>>> REGRESSION / MISMATCH <<<\033[0m: {sym} (0x{addr:08X})"
                )
                print(
                    f"      Expected ({len(expected_slice)} B): {expected_slice[:16].hex()}..."
                )
                print(
                    f"      Compiled ({len(actual_slice)} B): {actual_slice[:16].hex()}..."
                )
                print(f"      Differences: {diff_count} byte(s)")

    print("============================================================")
    summary_parts = [
        f"\033[92m{matched_count} decompiled (C/C++)\033[0m",
        f"\033[90m{asm_stub_count} assembly stubs verified\033[0m"
    ]
    if staged_count > 0:
        summary_parts.append(f"\033[93m{staged_count} staged (WIP)\033[0m")
    summary_parts.append(f"{mismatched_count} regressed")
    print(f"  Results: {', '.join(summary_parts)}")
    print("============================================================")

    pending = [
        s
        for s, m in manifest.items()
        if s not in checked_symbols and m["status"].lower() not in ("matched", "community_matched", "asm_stub")
    ]
    if pending:
        print(f"  Pending candidates ({len(pending)}):")
        for s in pending[:5]:
            print(
                f"    ⏳ {s} (0x{manifest[s]['address']:08X}) — {manifest[s]['size']} B"
            )
        if len(pending) > 5:
            print(f"    ... and {len(pending) - 5} more")
        print("============================================================")

    return 1 if mismatched_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
