#!/usr/bin/env python3
"""
tools/generate_expected.py — Generates expected target object files (.o)
for all cataloged functions from extracted/code.raw.bin.

These expected object files are required by objdiff and decomp.dev to compute
diffs and progress statistics without needing the full copyrighted retail ROM.
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
DUMP_SCRIPT = PROJECT_ROOT / "tools" / "dump_asm.py"


def main():
    if not MANIFEST.exists():
        print(f"❌ Error: Manifest '{MANIFEST}' not found.", file=sys.stderr)
        return 1

    EXPECTED_DIR.mkdir(parents=True, exist_ok=True)

    print("============================================================")
    print("  Yo-kai Watch 2 (3DS) — Expected Objects Generator")
    print("============================================================")

    generated = 0
    errors = 0

    with open(MANIFEST, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sym = row.get("symbol", "").strip()
            addr = row.get("address", "").strip()
            if not sym or not addr:
                continue

            out_o = EXPECTED_DIR / f"{sym}.o"

            dump_cmd = [sys.executable, str(DUMP_SCRIPT), addr, "--plain", "--symbol", sym]
            res = subprocess.run(dump_cmd, capture_output=True, text=True)
            if res.returncode != 0:
                print(f"  ❌ Failed to dump {sym} ({addr}): {res.stderr.strip()}")
                errors += 1
                continue

            asm_body = res.stdout.strip()
            s_content = f""".arm
.section .text, "ax", %progbits
.global {sym}
.type {sym}, %function
{asm_body}
.size {sym}, . - {sym}
"""

            with tempfile.NamedTemporaryFile("w", suffix=".s", delete=False) as tf:
                tf.write(s_content)
                temp_s = tf.name

            try:
                as_cmd = ["arm-none-eabi-as", "-mcpu=mpcore", "-mfpu=vfpv2", temp_s, "-o", str(out_o)]
                as_res = subprocess.run(as_cmd, capture_output=True, text=True)
                if as_res.returncode != 0:
                    print(f"  ❌ Failed to assemble {sym}: {as_res.stderr.strip()}")
                    errors += 1
                else:
                    generated += 1
                    print(f"  ✓ Generated: expected/{sym}.o")
            finally:
                Path(temp_s).unlink(missing_ok=True)

    # Consolidated C++ Translation Units (multi-function .cpp files)
    consolidated_tus = {
        "NexElement": [
            ("0x00340CE8", "_ZN2nn3nex10NexElementaSERKS1_"),
            ("0x00340CFC", "_ZN2nn3nex10NexElementC1Eis"),
            ("0x00340D08", "_ZN2nn3nex10NexElementC1Ev"),
            ("0x00340D18", "_ZN2nn3nex10NexElementD1Ev"),
            ("0x00340D1C", "_ZN2nn3nex10NexElementC1ERKS1_"),
        ]
    }

    for tu_name, tu_funcs in consolidated_tus.items():
        out_o = EXPECTED_DIR / f"{tu_name}.o"
        s_parts = ['.arm\n.section .text, "ax", %progbits\n']

        tu_ok = True
        for addr, sym in tu_funcs:
            dump_cmd = [sys.executable, str(DUMP_SCRIPT), addr, "--plain", "--symbol", sym]
            res = subprocess.run(dump_cmd, capture_output=True, text=True)
            if res.returncode != 0:
                print(f"  ❌ Failed to dump {sym} ({addr}) for TU {tu_name}: {res.stderr.strip()}")
                tu_ok = False
                break
            asm_body = res.stdout.strip()
            s_parts.append(f".global {sym}\n.type {sym}, %function\n{sym}:\n{asm_body}\n.size {sym}, . - {sym}\n")

        if tu_ok:
            s_content = "\n".join(s_parts)
            with tempfile.NamedTemporaryFile("w", suffix=".s", delete=False) as tf:
                tf.write(s_content)
                temp_s = tf.name
            try:
                as_cmd = ["arm-none-eabi-as", "-mcpu=mpcore", "-mfpu=vfpv2", temp_s, "-o", str(out_o)]
                as_res = subprocess.run(as_cmd, capture_output=True, text=True)
                if as_res.returncode != 0:
                    print(f"  ❌ Failed to assemble TU {tu_name}: {as_res.stderr.strip()}")
                    errors += 1
                else:
                    generated += 1
                    print(f"  ✓ Generated consolidated TU: expected/{tu_name}.o")
            finally:
                Path(temp_s).unlink(missing_ok=True)
        else:
            errors += 1

    print("============================================================")
    print(f"  Finished: {generated} generated, {errors} errors.")
    print("============================================================")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

