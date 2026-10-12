#!/usr/bin/env python3
"""
tools/audit_progress.py — Progress auditor and automatic README generator
for Yo-kai Watch 2 (Nintendo 3DS).

Inspired by the progress reporting methodology of Yokimitsuro (khdays-decomp).
Reads the canonical manifest (`config/functions.csv` or `config/functions_candidates.csv`)
and updates statistics and the README table in a reproducible, mathematical manner.
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
README_FILE = PROJECT_ROOT / "README.md"
OBJDIFF_CONFIG = PROJECT_ROOT / "objdiff.json"
MANIFEST_CSV = CONFIG_DIR / "functions.csv"
if not MANIFEST_CSV.exists() and (CONFIG_DIR / "functions_candidates.csv").exists():
    MANIFEST_CSV = CONFIG_DIR / "functions_candidates.csv"

TOTAL_CODE_BYTES = 7737344  # Total executable size of code.raw.bin (7.73 MB)

ESTIMATED_TOTAL_FUNCTIONS = 18292  # Detected via Ghidra analysis


def load_manifest(csv_path: Path):
    functions = []
    if not csv_path.exists():
        print(f"⚠️ Manifest not found at {csv_path}")
        return functions

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row["size"] = int(row["size"])
            except ValueError:
                row["size"] = 0
            functions.append(row)
    return functions


def calculate_metrics(functions):
    matched_functions = [f for f in functions if f["status"].lower() == "matched"]
    wip_functions = [f for f in functions if f["status"].lower() in ("wip", "in review")]
    staged_functions = [f for f in functions if f["status"].lower() == "staged"]

    matched_count = len(matched_functions)
    matched_bytes = sum(f["size"] for f in matched_functions)
    staged_count = len(functions)

    func_percent = (matched_count / ESTIMATED_TOTAL_FUNCTIONS) * 100.0
    byte_percent = (matched_bytes / TOTAL_CODE_BYTES) * 100.0

    return {
        "matched_count": matched_count,
        "matched_bytes": matched_bytes,
        "staged_count": staged_count,
        "func_percent": func_percent,
        "byte_percent": byte_percent,
        "matched_functions": matched_functions,
        "wip_functions": wip_functions,
        "staged_functions": staged_functions,
        "total_functions": len(functions)
    }


def format_progress_table(metrics):
    mc = metrics["matched_count"]
    mb = metrics["matched_bytes"]
    fp = metrics["func_percent"]
    bp = metrics["byte_percent"]
    staged = metrics["staged_count"]

    matched_details = f"({', '.join(f['symbol'] for f in metrics['matched_functions'])})" if mc > 0 else "None yet"

    lines = [
        "| Category | Count | Meaning |",
        "| :--- | :---: | :--- |",
        f"| **Real C-decompiled matched functions** | **{mc}** / ~{ESTIMATED_TOTAL_FUNCTIONS:,} ({fp:.2f}%) | Functions implemented in C and verified byte-exact {matched_details} |",
        f"| **Complete functions (C + verified original library assembly)** | **{mc}** / ~{ESTIMATED_TOTAL_FUNCTIONS:,} ({fp:.2f}%) | Real C, plus library functions whose original source is assembly |",
        f"| **Real C-decompiled matched bytes** | **{mb}** / {TOTAL_CODE_BYTES:,} bytes ({bp:.4f}%) | Real-C-only byte progress; `asm_stubs/`, inline ASM and `scratches/` are excluded |",
        f"| **Inline ASM / ASM stub matched functions** | **0** / ~{ESTIMATED_TOTAL_FUNCTIONS:,} | ASM implementations: library assembly and authorized inline exceptions |",
        f"| **SDK / library byte-match identifications** | **0** / ~{ESTIMATED_TOTAL_FUNCTIONS:,} | CTR-SDK / Nintendo library functions identified separately |",
        f"| **Named / mapped candidates** | **{staged}** / ~{ESTIMATED_TOTAL_FUNCTIONS:,} | Functions cataloged in scratches with isolated disassembly |",
        "| **Initialized DATA** | Staged | `.rodata` / `.data` relocation and literal pool mapping |",
        f"| **Total known functions** | ~{ESTIMATED_TOTAL_FUNCTIONS:,} | Estimated function count for the EU target |",
        "| **Region** | EU (`00040000001B2900`) | Multi-5 (PAL v1.0) |",
        "| **Architecture** | ARM11 MPCore (ARMv6K) | 32-bit Little Endian, VMA `0x00100000` |",
        "| **Compiler** | ARMCC / RVCT 4.x | Target toolchain identification under verification |"
    ]
    return "\n".join(lines)


def format_manifest_table(functions):
    status_badges = {
        "matched": "🟢 Matched",
        "wip": "🟡 In Review",
        "in review": "🟡 In Review",
        "staged": "⏳ Staged"
    }

    lines = [
        "| Virtual Address | Symbol / Name | Size (bytes) | Status | Description / Notes |",
        "| :--- | :--- | :---: | :---: | :--- |"
    ]

    for f in functions:
        badge = status_badges.get(f["status"].lower(), f["status"])
        addr = f["address"]
        sym = f["symbol"]
        size = f"{f['size']} B"
        desc = f["description"]
        lines.append(f"| `{addr}` | `{sym}` | {size} | {badge} | {desc} |")

    return "\n".join(lines)


def update_readme(readme_path: Path, progress_table: str, manifest_table: str):
    if not readme_path.exists():
        print(f"⚠️ README not found at {readme_path}")
        return False

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace progress stats table
    stats_pattern = r"(<!-- PROGRESS_STATS_START -->)(.*?)(<!-- PROGRESS_STATS_END -->)"
    if re.search(stats_pattern, content, flags=re.DOTALL):
        content = re.sub(
            stats_pattern,
            rf"\g<1>\n\n{progress_table}\n\n\g<3>",
            content,
            flags=re.DOTALL
        )
    else:
        print("⚠️ Marker <!-- PROGRESS_STATS_START --> not found in README.")

    # Replace manifest table
    manifest_pattern = r"(<!-- MANIFEST_TABLE_START -->)(.*?)(<!-- MANIFEST_TABLE_END -->)"
    if re.search(manifest_pattern, content, flags=re.DOTALL):
        content = re.sub(
            manifest_pattern,
            rf"\g<1>\n\n{manifest_table}\n\n\g<3>",
            content,
            flags=re.DOTALL
        )
    else:
        print("⚠️ Marker <!-- MANIFEST_TABLE_START --> not found in README.")

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ README.md automatically updated with audited progress.")
    return True


def update_objdiff_config(functions):
    src_dir = PROJECT_ROOT / "src"
    source_files = list(src_dir.rglob("*.c")) + list(src_dir.rglob("*.cpp"))
    file_map = {sf.stem: sf.relative_to(PROJECT_ROOT) for sf in source_files}

    units = []
    for f in functions:
        sym = f["symbol"]
        status = f["status"].lower()
        is_matched = (status == "matched")

        if sym in file_map:
            src_rel = str(file_map[sym])
            base_o = f"build/{file_map[sym].with_suffix('.o')}"
        elif is_matched:
            src_rel = f"src/system/{sym}.c"
            base_o = f"build/src/system/{sym}.o"
        else:
            continue

        units.append({
            "name": sym,
            "target_path": f"expected/{sym}.o",
            "base_path": base_o,
            "source_path": src_rel,
            "metadata": {
                "complete": is_matched
            }
        })

    config = {
        "$schema": "https://raw.githubusercontent.com/encounter/objdiff/main/config.schema.json",
        "min_version": "2.0.0",
        "custom_make": "make",
        "build_target": False,
        "build_base": True,
        "watch_patterns": [
            "src/**/*.c",
            "src/**/*.cpp",
            "include/**/*.h"
        ],
        "units": units
    }

    with open(OBJDIFF_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print("✅ objdiff.json automatically synchronized.")


def main():
    parser = argparse.ArgumentParser(description="Progress auditor for Yo-kai Watch 2 decompilation")
    parser.add_argument("--update-readme", action="store_true", help="Automatically update markdown tables in README.md")
    args = parser.parse_args()

    functions = load_manifest(MANIFEST_CSV)
    metrics = calculate_metrics(functions)

    print("============================================================")
    print("  Yo-kai Watch 2 (3DS) — Matching Progress Auditor")
    print("============================================================")
    print(f"  Matched functions  : {metrics['matched_count']} / ~{ESTIMATED_TOTAL_FUNCTIONS:,} ({metrics['func_percent']:.2f}%)")
    print(f"  Matched C bytes    : {metrics['matched_bytes']} / {TOTAL_CODE_BYTES:,} bytes ({metrics['byte_percent']:.4f}%)")
    print(f"  Cataloged candidates: {metrics['staged_count']} functions")
    print("============================================================")

    progress_table = format_progress_table(metrics)
    manifest_table = format_manifest_table(functions)

    if args.update_readme:
        update_readme(README_FILE, progress_table, manifest_table)

    update_objdiff_config(functions)


if __name__ == "__main__":
    main()

