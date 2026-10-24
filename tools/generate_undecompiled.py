#!/usr/bin/env python3
"""
tools/generate_undecompiled.py — Generates a target object representing
the remaining undecompiled code of the .text segment (6,238,892 bytes across 18,225 functions).

Ensures that objdiff and decomp.dev report accurate progress percentages
relative to the full .text executable segment from the NCCH ExHeader.
"""

import csv
from pathlib import Path
import subprocess
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
MANIFEST = CONFIG_DIR / "functions.csv"
EXPECTED_DIR = PROJECT_ROOT / "expected"
TARGET_OBJ = EXPECTED_DIR / "undecompiled.o"

# Exact .text executable size from NCCH ExHeader (0x00100000 - 0x006F32AC)
TOTAL_GAME_CODE_BYTES = 6238892


def get_current_matched_bytes():
    total_sz = 0
    if MANIFEST.exists():
        with open(MANIFEST, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("status", "").strip().lower() in ("matched", "community_matched", "matched_community"):
                    try:
                        total_sz += int(row.get("size", 0))
                    except ValueError:
                        pass
    return total_sz


def main():
    EXPECTED_DIR.mkdir(parents=True, exist_ok=True)

    matched_sz = get_current_matched_bytes()
    remaining_sz = max(0, TOTAL_GAME_CODE_BYTES - matched_sz)

    s_content = f""".arm
.section .text, "ax", %progbits
.global undecompiled_code
.type undecompiled_code, %function
undecompiled_code:
    .space {remaining_sz}
.size undecompiled_code, . - undecompiled_code
"""

    with tempfile.NamedTemporaryFile("w", suffix=".s", delete=False) as tf:
        tf.write(s_content)
        temp_s = tf.name

    try:
        cmd = ["arm-none-eabi-as", "-mcpu=mpcore", temp_s, "-o", str(TARGET_OBJ)]
        subprocess.check_call(cmd)
        print(f"✓ Generated {TARGET_OBJ.name}: {remaining_sz:,} bytes undecompiled (total .text: {TOTAL_GAME_CODE_BYTES:,} B)")
    finally:
        Path(temp_s).unlink(missing_ok=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
