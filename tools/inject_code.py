#!/usr/bin/env python3
"""
tools/inject_code.py — Injects compiled functions into a 3DS executable (code.bin).

Takes the reference binary (extracted/code.raw.bin), overwrites the machine code
for all matched/staged functions with their newly compiled versions from build/,
and generates a bootable 'build/code.bin' ready for Citra or Luma3DS.
"""

import argparse
import csv
import os
from pathlib import Path
import struct
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASE_VMA = 0x00100000
RAW_BIN = PROJECT_ROOT / "extracted" / "code.raw.bin"
CONFIG_DIR = PROJECT_ROOT / "config"
BUILD_DIR = PROJECT_ROOT / "build"
MANIFEST_CSV = CONFIG_DIR / "functions.csv"
OUTPUT_BIN = BUILD_DIR / "code.bin"


def get_symbols_from_elf(obj_path: Path):
    cmd = ["arm-none-eabi-readelf", "-s", "-W", str(obj_path)]
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.PIPE)
    except Exception:
        return {}

    symbols = {}
    for line in out.splitlines():
        parts = line.strip().split()
        if len(parts) >= 8 and parts[3] == "FUNC":
            name = parts[7]
            try:
                symbols[name] = {"offset": int(parts[1], 16), "size": int(parts[2])}
            except ValueError:
                continue
    return symbols


def get_relocations_from_elf(obj_path: Path):
    cmd = ["arm-none-eabi-readelf", "-r", "-W", str(obj_path)]
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.PIPE)
    except Exception:
        return []

    relocs = []
    for line in out.splitlines():
        parts = line.strip().split()
        if len(parts) >= 5 and "R_ARM_" in parts[2]:
            try:
                relocs.append({
                    "offset": int(parts[0], 16),
                    "type": parts[2],
                    "symbol": parts[-1]
                })
            except ValueError:
                continue
    return relocs


def extract_section_bytes(obj_path: Path, section=".text"):
    cmd = ["arm-none-eabi-objcopy", "-O", "binary", f"--only-section={section}", str(obj_path), "/dev/stdout"]
    try:
        res = subprocess.run(cmd, capture_output=True, check=True)
        return res.stdout
    except Exception:
        return b""


def main():
    parser = argparse.ArgumentParser(description="Inject compiled C functions into code.bin")
    parser.add_argument("--output", type=str, default=str(OUTPUT_BIN), help="Path to output code.bin")
    parser.add_argument("--include-wip", action="store_true", help="Also inject staged/WIP functions")
    args = parser.parse_args()

    if not RAW_BIN.exists():
        print(f"❌ Error: Reference binary '{RAW_BIN}' not found.")
        return 1

    with open(RAW_BIN, "rb") as f:
        patched_data = bytearray(f.read())

    manifest = {}
    if MANIFEST_CSV.exists():
        with open(MANIFEST_CSV, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    manifest[row["symbol"]] = {
                        "address": int(row["address"], 0),
                        "size": int(row["size"]),
                        "status": row.get("status", "staged")
                    }
                except (ValueError, KeyError):
                    continue

    obj_files = list(BUILD_DIR.rglob("*.o"))
    if not obj_files:
        print("⚠️ No compiled objects found in build/. Run 'make' first.")
        return 1

    injected_count = 0
    injected_bytes = 0

    print("============================================================")
    print("  Yo-kai Watch 2 (3DS) — Executable Code Injector")
    print("============================================================")

    for obj in sorted(obj_files):
        symbols = get_symbols_from_elf(obj)
        if not symbols:
            continue

        relocs = get_relocations_from_elf(obj)
        text_bytes = extract_section_bytes(obj, ".text")
        if not text_bytes:
            continue

        for sym, sym_info in symbols.items():
            meta = manifest.get(sym)
            if not meta:
                continue

            if (
                not args.include_wip
                and meta["status"].lower() not in ("matched", "community_matched", "matched_community")
            ):
                continue

            addr = meta["address"]
            size = meta["size"]
            offset_in_bin = addr - BASE_VMA

            if offset_in_bin < 0 or offset_in_bin + size > len(patched_data):
                print(f"  ⚠️ Skipping {sym}: address 0x{addr:08X} out of binary bounds")
                continue

            obj_off = sym_info["offset"]
            obj_size = sym_info["size"]
            fn_bytes = bytearray(text_bytes[obj_off : obj_off + obj_size])

            # For relocations: preserve target reference address from raw binary
            for r in relocs:
                if obj_off <= r["offset"] < obj_off + obj_size:
                    rel_local = r["offset"] - obj_off
                    if rel_local + 4 <= len(fn_bytes):
                        orig_val = patched_data[offset_in_bin + rel_local : offset_in_bin + rel_local + 4]
                        fn_bytes[rel_local : rel_local + 4] = orig_val

            # Overwrite binary slice
            patched_data[offset_in_bin : offset_in_bin + len(fn_bytes)] = fn_bytes
            injected_count += 1
            injected_bytes += len(fn_bytes)
            print(f"  💉 Injected {sym} (0x{addr:08X}) — {len(fn_bytes)} bytes")

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(patched_data)

    print("============================================================")
    print(f"✅ Generated: {out_path} ({len(patched_data):,} bytes)")
    print(f"   Injected functions: {injected_count} ({injected_bytes} bytes)")
    print("============================================================")
    print("\n🎮 Cómo probarlo en Citra / Lime3DS:")
    print("  1. Abre Citra y haz clic derecho en 'Yo-kai Watch 2: Mentespectros'.")
    print("  2. Selecciona 'Abrir ubicación de mods' (Open Mods Location).")
    print("  3. Crea dentro una carpeta llamada 'exefs' (si no existe).")
    print(f"  4. Copia '{out_path}' a esa carpeta como 'code.bin'.")
    print("  5. ¡Inicia el juego en Citra! Citra cargará tu código compilado.")
    print("============================================================")
    return 0


if __name__ == "__main__":
    sys.exit(main())
