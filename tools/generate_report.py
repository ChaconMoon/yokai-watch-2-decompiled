#!/usr/bin/env python3
"""
tools/generate_report.py — Generates a comprehensive decompilation progress report
in the standard objdiff-cli format (version 2), perfectly compatible with decomp.dev,
frogress, and matching the exact schema used in reference projects (like Animal Crossing).
"""

import csv
import json
from pathlib import Path
import re
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
MANIFEST_CSV = CONFIG_DIR / "functions.csv"
CLASSIFIED_CSV = CONFIG_DIR / "functions_classified.csv"
MEMORY_MAP_JSON = CONFIG_DIR / "memory_map.json"
SRC_DIR = PROJECT_ROOT / "src"
BUILD_DIR = PROJECT_ROOT / "build"
REPORT_OUTPUT = BUILD_DIR / "report.json"

# Canonical Memory Map Constants (from ExHeader)
BASE_VMA = 0x00100000
TOTAL_CODE_BYTES = 6238892      # .text segment size
TOTAL_RODATA_BYTES = 1147948    # .rodata segment size
TOTAL_DATA_BYTES = 342324       # .data segment size
TOTAL_BSS_BYTES = 766088        # .bss segment size
TOTAL_ALL_DATA_BYTES = TOTAL_RODATA_BYTES + TOTAL_DATA_BYTES + TOTAL_BSS_BYTES  # 2,256,360 B
TOTAL_FUNCTIONS_EXPECTED = 18225

# Demangling cache for performance
_DEMANGLE_CACHE = {}

def demangle(sym: str) -> str:
    if sym in _DEMANGLE_CACHE:
        return _DEMANGLE_CACHE[sym]
    if sym.startswith("_Z"):
        try:
            res = subprocess.run(["c++filt", sym], capture_output=True, text=True, check=True)
            dem = res.stdout.strip()
            _DEMANGLE_CACHE[sym] = dem
            return dem
        except Exception:
            pass
    _DEMANGLE_CACHE[sym] = sym
    return sym


def load_all_functions():
    """Loads all functions, prioritizing config/functions.csv and completing with functions_classified.csv."""
    funcs_by_addr = {}

    # 1. Load cataloged functions (active in progress tracking)
    if MANIFEST_CSV.exists():
        with open(MANIFEST_CSV, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                addr_hex = row.get("address", "").strip()
                if not addr_hex:
                    continue
                try:
                    addr_int = int(addr_hex, 16)
                    size = int(row.get("size", 0))
                except ValueError:
                    continue

                funcs_by_addr[addr_int] = {
                    "address": addr_int,
                    "address_hex": f"0x{addr_int:08X}",
                    "symbol": row.get("symbol", "").strip(),
                    "size": size,
                    "layer": row.get("layer", "game").strip().lower(),
                    "subsystem": row.get("subsystem", "core").strip(),
                    "status": row.get("status", "asm_stub").strip().lower(),
                    "description": row.get("description", "").strip()
                }

    # 2. Complete remaining functions from functions_classified.csv
    if CLASSIFIED_CSV.exists():
        with open(CLASSIFIED_CSV, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                addr_hex = row.get("address", "").strip()
                if not addr_hex:
                    continue
                try:
                    addr_int = int(addr_hex, 16)
                    size = int(row.get("size", 0))
                except ValueError:
                    continue

                if addr_int not in funcs_by_addr:
                    funcs_by_addr[addr_int] = {
                        "address": addr_int,
                        "address_hex": f"0x{addr_int:08X}",
                        "symbol": row.get("symbol", "").strip() or f"func_{addr_int:08X}",
                        "size": size,
                        "layer": row.get("layer", "game").strip().lower(),
                        "subsystem": row.get("subsystem", "core").strip(),
                        "status": "asm_stub",
                        "description": row.get("description", "").strip()
                    }

    return sorted(funcs_by_addr.values(), key=lambda x: x["address"])


def find_source_files():
    """Maps symbols to their actual source files in src/."""
    file_map = {}
    if SRC_DIR.exists():
        for path in list(SRC_DIR.rglob("*.c")) + list(SRC_DIR.rglob("*.cpp")):
            stem = path.stem
            rel = str(path.relative_to(PROJECT_ROOT))
            file_map[stem] = rel
    return file_map


def build_measures_dict(total_code, matched_code, total_data, matched_data, total_fns, matched_fns, total_units, complete_units):
    matched_code_pct = (matched_code / total_code * 100.0) if total_code > 0 else 0.0
    matched_data_pct = (matched_data / total_data * 100.0) if total_data > 0 else (100.0 if total_data == 0 else 0.0)
    matched_fns_pct = (matched_fns / total_fns * 100.0) if total_fns > 0 else 0.0

    return {
        "fuzzy_match_percent": round(matched_code_pct, 6),
        "total_code": str(total_code),
        "matched_code": str(matched_code),
        "matched_code_percent": round(matched_code_pct, 6),
        "total_data": str(total_data),
        "matched_data": str(matched_data),
        "matched_data_percent": round(matched_data_pct, 6),
        "total_functions": int(total_fns),
        "matched_functions": int(matched_fns),
        "matched_functions_percent": round(matched_fns_pct, 6),
        "complete_code": "0",
        "complete_code_percent": 0.0,
        "complete_data": "0",
        "complete_data_percent": 0.0,
        "total_units": int(total_units),
        "complete_units": int(complete_units)
    }


def assign_target_unit(fn: dict) -> str:
    """Pre-groups functions into canonical target C/C++ compilation units (.cpp / .c)."""
    sym = fn["symbol"]
    layer = fn["layer"]
    subsys = fn["subsystem"]
    dem = demangle(sym)

    # 1. Game Loops: match specific C++ loop class names
    if subsys == "loops" or layer == "game":
        m = re.match(r"^(ywCLoop[A-Za-z0-9]+)::", dem)
        if m:
            return f"src/game/loops/{m.group(1)}.cpp"
        if subsys == "loops":
            return "src/game/loops/ywCLoop.cpp"

    # 2. CTR: nn::nex classes
    if subsys == "nn_nex":
        m = re.match(r"^nn::nex::([A-Za-z0-9]+)::", dem)
        if m:
            return f"src/ctr/nn/nex/{m.group(1)}.cpp"
        return "src/ctr/nn/nex/nex.cpp"

    # 3. CTR: standard subsystems
    if subsys == "nn_applet":
        return "src/ctr/nn/applet/applet.cpp"
    if subsys == "nn_dsp":
        return "src/ctr/nn/dsp/dsp.cpp"
    if subsys == "nn_os":
        return "src/ctr/nn/os/os.cpp"
    if subsys == "nn_y2r":
        return "src/ctr/nn/y2r/y2r.cpp"
    if subsys == "nn_ndm":
        return "src/ctr/nn/ndm/ndm.cpp"
    if subsys == "nn_math":
        return "src/ctr/nn/math/math.cpp"
    if subsys == "nn_cecd":
        return "src/ctr/nn/cecd/cecd.cpp"
    if subsys == "svc":
        return "src/ctr/svc/svc.c"
    if subsys == "crt":
        return "src/ctr/crt/crt.c"

    # 4. Engine subsystems
    if layer == "engine":
        if subsys == "lfw":
            return "src/engine/lfw/lfwCLoop.cpp"
        if subsys == "lxp":
            return "src/engine/lxp/lxp.cpp"
        return "src/engine/core/core.cpp"

    # 5. Default fallback
    return f"src/{layer}/{subsys}/{subsys}.cpp"


def main():
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    all_funcs = load_all_functions()

    # Track matched status
    matched_statuses = ("matched", "community_matched", "matched_community")

    # Pre-group all functions by their target translation unit (.cpp / .c)
    units_map = {}
    for fn in all_funcs:
        unit_path = assign_target_unit(fn)
        if unit_path not in units_map:
            units_map[unit_path] = []
        units_map[unit_path].append(fn)

    # Calculate global metrics
    matched_funcs_list = [f for f in all_funcs if f["status"] in matched_statuses]
    total_code_matched = sum(f["size"] for f in matched_funcs_list)
    total_matched_functions_count = len(matched_funcs_list)

    # Layer breakdowns
    layer_stats = {
        "ctr": {"code": 0, "matched_code": 0, "fns": 0, "matched_fns": 0, "units": 0, "complete_units": 0},
        "engine": {"code": 0, "matched_code": 0, "fns": 0, "matched_fns": 0, "units": 0, "complete_units": 0},
        "game": {"code": 0, "matched_code": 0, "fns": 0, "matched_fns": 0, "units": 0, "complete_units": 0},
    }

    report_units = []

    # 1. Unit: extracted_data (matching Animal Crossing reference layout)
    data_unit = {
        "name": "extracted_data",
        "measures": {
            "fuzzy_match_percent": 0.0,
            "total_code": "0",
            "matched_code": "0",
            "matched_code_percent": 0.0,
            "total_data": str(TOTAL_ALL_DATA_BYTES),
            "matched_data": "0",
            "matched_data_percent": 0.0,
            "total_functions": 0,
            "matched_functions": 0,
            "matched_functions_percent": 0.0,
            "complete_code": "0",
            "complete_code_percent": 0.0,
            "complete_data": "0",
            "complete_data_percent": 0.0,
            "total_units": 1,
            "complete_units": 0
        },
        "sections": [
            {"name": ".rodata", "size": str(TOTAL_RODATA_BYTES), "fuzzy_match_percent": 0.0},
            {"name": ".data", "size": str(TOTAL_DATA_BYTES), "fuzzy_match_percent": 0.0},
            {"name": ".bss", "size": str(TOTAL_BSS_BYTES), "fuzzy_match_percent": 0.0}
        ],
        "functions": [],
        "metadata": {
            "progress_categories": ["codebin"],
            "auto_generated": False
        }
    }
    report_units.append(data_unit)

    # Calculate total code accounted across grouped units
    total_grouped_code = sum(sum(f["size"] for f in fns) for fns in units_map.values())
    unmapped_code_slack = max(0, TOTAL_CODE_BYTES - total_grouped_code)

    # 2. Add each pre-grouped C++ / C compilation unit
    for unit_path, fns in sorted(units_map.items()):
        unit_code = sum(f["size"] for f in fns)
        unit_matched_code = sum(f["size"] for f in fns if f["status"] in matched_statuses)
        unit_fns_count = len(fns)
        unit_matched_fns = len([f for f in fns if f["status"] in matched_statuses])

        # Absorb unmapped binary remainder into game/core/core.cpp so total_code reaches exact 6,238,892 B
        if unit_path == "src/game/core/core.cpp" and unmapped_code_slack > 0:
            unit_code += unmapped_code_slack

        is_complete = (unit_matched_code == unit_code and unit_code > 0)

        layer = fns[0]["layer"] if fns else "game"
        if layer not in layer_stats:
            layer = "game"

        layer_stats[layer]["code"] += unit_code
        layer_stats[layer]["matched_code"] += unit_matched_code
        layer_stats[layer]["fns"] += unit_fns_count
        layer_stats[layer]["matched_fns"] += unit_matched_fns
        layer_stats[layer]["units"] += 1
        if is_complete:
            layer_stats[layer]["complete_units"] += 1

        fn_entries = []
        for fn in fns:
            vma = fn["address"]
            addr_rel = vma - BASE_VMA
            is_m = fn["status"] in matched_statuses
            pct = 100.0 if is_m else 0.0

            fn_entries.append({
                "name": fn["symbol"],
                "size": str(fn["size"]),
                "fuzzy_match_percent": pct,
                "metadata": {
                    "demangled_name": demangle(fn["symbol"]),
                    "virtual_address": str(vma)
                },
                "address": str(addr_rel)
            })

        unit_exists_on_disk = (PROJECT_ROOT / unit_path).exists()
        unit_obj = {
            "name": unit_path,
            "measures": build_measures_dict(
                total_code=unit_code,
                matched_code=unit_matched_code,
                total_data=0,
                matched_data=0,
                total_fns=unit_fns_count,
                matched_fns=unit_matched_fns,
                total_units=1,
                complete_units=1 if is_complete else 0
            ),
            "sections": [
                {
                    "name": ".text",
                    "size": str(unit_code),
                    "fuzzy_match_percent": round((unit_matched_code / unit_code * 100.0), 6) if unit_code > 0 else 0.0
                }
            ],
            "functions": fn_entries,
            "metadata": {
                "progress_categories": [layer, "codebin"],
                "auto_generated": not unit_exists_on_disk,
                "source_path": unit_path
            }
        }
        report_units.append(unit_obj)

    total_units_count = len(report_units)
    complete_units_count = sum(1 for u in report_units if u["measures"]["complete_units"] > 0)

    # Top-level measures
    global_measures = build_measures_dict(
        total_code=TOTAL_CODE_BYTES,
        matched_code=total_code_matched,
        total_data=TOTAL_ALL_DATA_BYTES,
        matched_data=0,
        total_fns=TOTAL_FUNCTIONS_EXPECTED,
        matched_fns=total_matched_functions_count,
        total_units=total_units_count,
        complete_units=complete_units_count
    )

    # Categories array (version 2)
    categories = [
        {
            "id": "codebin",
            "name": "code.bin (all)",
            "measures": global_measures
        },
        {
            "id": "ctr",
            "name": "Nintendo CTR-SDK (ctr)",
            "measures": build_measures_dict(
                total_code=layer_stats["ctr"]["code"],
                matched_code=layer_stats["ctr"]["matched_code"],
                total_data=0,
                matched_data=0,
                total_fns=layer_stats["ctr"]["fns"],
                matched_fns=layer_stats["ctr"]["matched_fns"],
                total_units=layer_stats["ctr"]["units"],
                complete_units=layer_stats["ctr"]["complete_units"]
            )
        },
        {
            "id": "engine",
            "name": "Level-5 Engine (lfw / lxp / gds)",
            "measures": build_measures_dict(
                total_code=layer_stats["engine"]["code"],
                matched_code=layer_stats["engine"]["matched_code"],
                total_data=0,
                matched_data=0,
                total_fns=layer_stats["engine"]["fns"],
                matched_fns=layer_stats["engine"]["matched_fns"],
                total_units=layer_stats["engine"]["units"],
                complete_units=layer_stats["engine"]["complete_units"]
            )
        },
        {
            "id": "game",
            "name": "Yo-kai Watch 2 (Game Logic)",
            "measures": build_measures_dict(
                total_code=layer_stats["game"]["code"],
                matched_code=layer_stats["game"]["matched_code"],
                total_data=0,
                matched_data=0,
                total_fns=layer_stats["game"]["fns"],
                matched_fns=layer_stats["game"]["matched_fns"],
                total_units=layer_stats["game"]["units"],
                complete_units=layer_stats["game"]["complete_units"]
            )
        }
    ]

    report = {
        "version": 2,
        "measures": global_measures,
        "categories": categories,
        "units": report_units
    }

    with open(REPORT_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(report, f, separators=(',', ':'))

    print(f"✅ build/report.json generated successfully in objdiff-cli v2 format ({len(report_units)} units, {total_matched_functions_count}/{TOTAL_FUNCTIONS_EXPECTED} functions matched).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
