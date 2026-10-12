#!/usr/bin/env python3
"""
tools/dump_asm.py — Dumps assembly of a function in ready-to-paste format
for decomp.me (relative offsets from 0 or plain instructions).

Usage:
    python tools/dump_asm.py 0x10B6D8             # Auto-detects size and literal pool
    python tools/dump_asm.py func_0010B6D8        # Lookup by symbol
    python tools/dump_asm.py 0x10B6D8 12          # Explicit size
    python tools/dump_asm.py 0x10B6D8 --plain     # Plain assembly ready for decomp.me
    python tools/dump_asm.py 0x100100 40 --thumb  # Thumb mode
"""

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
BIN = PROJECT_ROOT / "extracted" / "code.raw.bin"
BASE = 0x00100000

LINE_RE = re.compile(r"^\s*([0-9a-fA-F]+):\s+([0-9a-fA-F]{4,8})\s+(.*)$")


def find_function_meta(target: str):
    """Looks up address, size, and symbol name in manifests."""
    target_clean = target.strip()
    target_addr = None
    target_sym = None

    if target_clean.lower().startswith("0x"):
        try:
            target_addr = int(target_clean, 16)
        except ValueError:
            pass
    elif re.match(r"^[0-9a-fA-F]{6,8}$", target_clean):
        try:
            target_addr = int(target_clean, 16)
        except ValueError:
            pass
    else:
        target_sym = target_clean

    # Search candidates and canonical manifests
    for manifest_name in ["functions_candidates.csv", "functions.csv"]:
        manifest_path = CONFIG_DIR / manifest_name
        if manifest_path.exists():
            with open(manifest_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        addr = int(row["address"], 0)
                        size = int(row["size"])
                        sym = row["symbol"]
                    except (ValueError, KeyError):
                        continue
                    if (target_addr is not None and addr == target_addr) or (target_sym is not None and sym == target_sym):
                        return addr, size, sym

    # Search full Ghidra catalog
    ident_path = CONFIG_DIR / "ykw_2_identify_fuctions.csv"
    if ident_path.exists():
        with open(ident_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                addr_str = row.get("Location", "")
                if addr_str:
                    try:
                        addr = int(addr_str, 16)
                        name = row.get("Name", "")
                        size = int(row.get("Function Size", "0"))
                    except ValueError:
                        continue
                    if (target_addr is not None and addr == target_addr) or (target_sym is not None and name == target_sym):
                        return addr, size, name

    if target_addr is not None:
        return target_addr, None, f"func_{target_addr:08X}"
    return None, None, target_clean


def main():
    ap = argparse.ArgumentParser(description="Dump function assembly for decomp.me matching")
    ap.add_argument("target", help="Virtual address (e.g. 0x10B6D8) or symbol name (e.g. func_0010B6D8)")
    ap.add_argument("size", nargs="?", type=lambda x: int(x, 0), default=None, help="Size in bytes (optional if in manifest)")
    ap.add_argument("--thumb", action="store_true", help="Disassemble as Thumb mode")
    ap.add_argument("--plain", action="store_true", help="Plain instructions only without offset prefixes")
    ap.add_argument("--symbol", type=str, default=None, help="Explicit function symbol name override")
    args = ap.parse_args()

    if not BIN.exists():
        print(f"❌ Error: Reference binary not found at '{BIN}'. Run 'make extract' first.", file=sys.stderr)
        return 1

    addr, meta_size, sym = find_function_meta(args.target)
    if addr is None:
        print(f"❌ Error: Could not determine address for '{args.target}'.", file=sys.stderr)
        return 1

    size = args.size if args.size is not None else meta_size
    if size is None or size <= 0:
        print(f"❌ Error: Function size unknown for 0x{addr:08X}. Please specify size: python tools/dump_asm.py 0x{addr:08X} <size>", file=sys.stderr)
        return 1

    symbol = args.symbol or sym or f"func_{addr:08X}"

    cmd = ["arm-none-eabi-objdump", "-b", "binary", "-m", "arm"]
    if args.thumb:
        cmd += ["-M", "force-thumb"]
    cmd += [
        "-D", f"--adjust-vma={BASE:#x}",
        f"--start-address={addr:#x}",
        f"--stop-address={addr + size:#x}",
        str(BIN),
    ]

    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running arm-none-eabi-objdump: {e}", file=sys.stderr)
        return 1

    # First pass: identify literal pool addresses referenced via PC-relative loads
    pool_targets = set()
    parsed_lines = []
    for line in out.splitlines():
        m = LINE_RE.match(line)
        if not m:
            continue
        line_addr = int(m.group(1), 16)
        hexval = m.group(2)
        rest = m.group(3)

        # Detect literal pool targets in objdump comments (e.g. '@ 0x10b6e0' or '@ 10b6e0')
        comment_m = re.search(r"@\s*(?:0x)?([0-9a-fA-F]+)", rest)
        if comment_m:
            try:
                target_ref = int(comment_m.group(1), 16)
                if addr <= target_ref < addr + size:
                    pool_targets.add(target_ref)
            except ValueError:
                pass
        parsed_lines.append((line_addr, hexval, rest))

    if args.plain:
        print(f"{symbol}:")

    for line_addr, hexval, rest in parsed_lines:
        insn = re.sub(r"\s+@.*$", "", rest).replace("\t", " ").strip()
        if line_addr in pool_targets:
            insn = f".word 0x{hexval.upper()}"

        if args.plain:
            print(f"    {insn}")
        else:
            print(f"{line_addr - addr:>4x}:   {insn}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
