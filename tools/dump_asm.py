#!/usr/bin/env python3
"""
tools/dump_asm.py — Dumps assembly of a function in ready-to-paste format
for decomp.me (relative offsets from 0 or plain instructions).

Usage:
    python tools/dump_asm.py 0x10B6D0 8            # ARM (default)
    python tools/dump_asm.py 0x100100 40 --thumb   # Thumb
    python tools/dump_asm.py 0x10B6D0 8 --plain    # Plain instructions with .global label
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BIN = PROJECT_ROOT / "extracted" / "code.raw.bin"
BASE = 0x00100000

LINE_RE = re.compile(r"^\s*([0-9a-f]+):\s+(?:[0-9a-f]{4,8}\s+)+\s*(.*)$")


def main():
    ap = argparse.ArgumentParser(description="Dump function assembly for decomp.me matching")
    ap.add_argument("address", type=lambda x: int(x, 0), help="Virtual start address (e.g. 0x10B6D0)")
    ap.add_argument("size", type=lambda x: int(x, 0), help="Size in bytes")
    ap.add_argument("--thumb", action="store_true", help="Disassemble as Thumb mode")
    ap.add_argument("--plain", action="store_true", help="Plain instructions only, without offset prefixes")
    ap.add_argument("--symbol", type=str, default=None, help="Function symbol name (emits .global and label)")
    args = ap.parse_args()

    symbol = args.symbol or f"func_{args.address:08X}"

    cmd = ["arm-none-eabi-objdump", "-b", "binary", "-m", "arm"]
    if args.thumb:
        cmd += ["-M", "force-thumb"]
    cmd += [
        "-D", f"--adjust-vma={BASE:#x}",
        f"--start-address={args.address:#x}",
        f"--stop-address={args.address + args.size:#x}",
        str(BIN),
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout

    if args.plain:
        print(f".global {symbol}")
        print(f"{symbol}:")

    for line in out.splitlines():
        m = LINE_RE.match(line)
        if not m:
            continue
        addr = int(m.group(1), 16)
        insn = re.sub(r"\s+@.*$", "", m.group(2)).replace("\t", " ").strip()
        if args.plain:
            print(f"    {insn}")
        else:
            print(f"{addr - args.address:>4x}:   {insn}")


if __name__ == "__main__":
    sys.exit(main())
