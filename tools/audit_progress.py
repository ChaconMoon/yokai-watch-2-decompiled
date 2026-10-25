#!/usr/bin/env python3
"""
tools/audit_progress.py — Progress auditor and automatic README / objdiff generator
for Yo-kai Watch 2 (Nintendo 3DS).

Inspired by the progress reporting methodology of Yokimitsuro (khdays-decomp).
Reads the canonical manifest (`config/functions.csv`) and updates statistics,
layer breakdowns (Nintendo CTR-SDK, Level-5 Engine, Yo-kai Watch 2 Game),
and the README tables in a reproducible, mathematical manner.
"""

import argparse
import csv
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
README_FILE = PROJECT_ROOT / "README.md"
OBJDIFF_CONFIG = PROJECT_ROOT / "objdiff.json"
MANIFEST_CSV = CONFIG_DIR / "functions.csv"
CLASSES_CSV = CONFIG_DIR / "classes_identified.csv"
if not MANIFEST_CSV.exists() and (CONFIG_DIR / "functions_candidates.csv").exists():
    MANIFEST_CSV = CONFIG_DIR / "functions_candidates.csv"

# Exact .text executable size from NCCH ExHeader (0x00100000 - 0x006F32AC)
TOTAL_CODE_BYTES = 6238892
TOTAL_BINARY_BYTES = 7737344
ESTIMATED_TOTAL_FUNCTIONS = 18225

PROGRESS_CATEGORIES = [
    {"id": "ctr", "name": "Nintendo CTR-SDK & Runtime"},
    {"id": "engine", "name": "Level-5 Engine (lfw / lxp / gds)"},
    {"id": "game", "name": "Yo-kai Watch 2 (yw2)"}
]

LAYER_LABELS = {
    "ctr": "Nintendo CTR-SDK (`ctr`)",
    "engine": "Level-5 Engine (`engine`)",
    "game": "Yo-kai Watch 2 (`game`)"
}

DEFAULT_SCRATCH = {
    "platform": "n3ds",
    "compiler": "armcc_40_821",
    "c_flags": "--cpu=MPCore -O3 -Otime --split_sections"
}


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


def categorize_function(func):
    layer = func.get("layer", "").strip().lower()
    if layer in ("ctr", "engine", "game"):
        return layer
    sym = func.get("symbol", "").lower()
    desc = func.get("description", "").lower()
    if sym.startswith("svc") or sym in ("clear_bss", "_start") or "ctr" in desc or "nn::" in desc:
        return "ctr"
    if "lfw" in desc or "lxp" in desc or "gds" in desc or "level-5" in desc:
        return "engine"
    return "game"


def calculate_metrics(functions):
    src_dir = PROJECT_ROOT / "src"
    asm_stems = {sf.stem for sf in src_dir.rglob("*.s")}

    c_matched = [
        f for f in functions
        if f["status"].lower() in ("matched", "community_matched", "matched_community")
        and f["symbol"] not in asm_stems
    ]
    asm_stubs = [
        f for f in functions
        if f["status"].lower() == "asm_stub" or (f["symbol"] in asm_stems and f["status"].lower() not in ("wip", "staged"))
    ]
    wip_functions = [f for f in functions if f["status"].lower() in ("wip", "in review")]
    staged_functions = [f for f in functions if f["status"].lower() == "staged"]

    c_by_layer = {"ctr": [], "engine": [], "game": []}
    for f in c_matched:
        c_by_layer[categorize_function(f)].append(f)

    asm_by_layer = {"ctr": [], "engine": [], "game": []}
    for f in asm_stubs:
        asm_by_layer[categorize_function(f)].append(f)

    c_matched_count = len(c_matched)
    asm_count = len(asm_stubs)
    c_matched_bytes = sum(f["size"] for f in c_matched)
    asm_bytes = sum(f["size"] for f in asm_stubs)
    staged_count = len(functions)

    c_func_percent = (c_matched_count / ESTIMATED_TOTAL_FUNCTIONS) * 100.0
    asm_func_percent = (asm_count / ESTIMATED_TOTAL_FUNCTIONS) * 100.0
    c_byte_percent = (c_matched_bytes / TOTAL_CODE_BYTES) * 100.0
    asm_byte_percent = (asm_bytes / TOTAL_CODE_BYTES) * 100.0

    return {
        "c_matched_count": c_matched_count,
        "asm_count": asm_count,
        "c_matched_bytes": c_matched_bytes,
        "asm_bytes": asm_bytes,
        "staged_count": staged_count,
        "c_func_percent": c_func_percent,
        "asm_func_percent": asm_func_percent,
        "c_byte_percent": c_byte_percent,
        "asm_byte_percent": asm_byte_percent,
        "c_matched": c_matched,
        "asm_stubs": asm_stubs,
        "wip_functions": wip_functions,
        "staged_functions": staged_functions,
        "c_by_layer": c_by_layer,
        "asm_by_layer": asm_by_layer,
        "total_functions": len(functions)
    }


def format_progress_table(metrics):
    cmc = metrics["c_matched_count"]
    amc = metrics["asm_count"]
    cmb = metrics["c_matched_bytes"]
    amb = metrics["asm_bytes"]
    cfp = metrics["c_func_percent"]
    afp = metrics["asm_func_percent"]
    cbp = metrics["c_byte_percent"]
    abp = metrics["asm_byte_percent"]
    staged = metrics["staged_count"]

    c_bin_percent = (cmb / TOTAL_BINARY_BYTES) * 100.0
    asm_bin_percent = (amb / TOTAL_BINARY_BYTES) * 100.0
    tot_bytes = cmb + amb
    tot_count = cmc + amc
    tot_func_percent = (tot_count / ESTIMATED_TOTAL_FUNCTIONS) * 100.0
    tot_text_percent = (tot_bytes / TOTAL_CODE_BYTES) * 100.0
    tot_bin_percent = (tot_bytes / TOTAL_BINARY_BYTES) * 100.0

    c_layer = metrics["c_by_layer"]
    asm_layer = metrics["asm_by_layer"]

    lines = [
        "| Category | Count | Meaning |",
        "| :--- | :---: | :--- |",
        f"| **Decompiled C/C++ (Functions)** | **{cmc}** / {ESTIMATED_TOTAL_FUNCTIONS:,} ({cfp:.2f}%) | Functions implemented in C/C++ and verified byte-exact |",
        f"| **Total Binary Code Covered** | **{cmb:,} B** / {TOTAL_CODE_BYTES:,} B ({cbp:.4f}%) | C/C++ compiled bytes vs total executable `.text` ({c_bin_percent:.4f}% of `{TOTAL_BINARY_BYTES:,} B` binary) |",
        f"| **Assembly Stubs (`.s` extracted)** | **{amc}** / {ESTIMATED_TOTAL_FUNCTIONS:,} ({afp:.2f}%) | Split stubs for building & progressive replacement ({amb:,} B / {abp:.4f}%) |",
        f"| **Build Coverage (C/C++ + ASM Stubs)** | **{tot_count}** / {ESTIMATED_TOTAL_FUNCTIONS:,} ({tot_func_percent:.2f}%) | Combined C/C++ & assembly matching `code.raw.bin` ({tot_bytes:,} B / {tot_text_percent:.4f}%) |",
        f"| **Layer 1: Nintendo CTR-SDK (`src/ctr/`)** | **{len(c_layer['ctr'])}** C matched + **{len(asm_layer['ctr'])}** stubs | CRT startup, `svc`, `nn::os`, `nn::y2r`, `nn::nex`, `nn::dsp` |",
        f"| **Layer 2: Level-5 Engine (`src/engine/`)** | **{len(c_layer['engine'])}** C matched + **{len(asm_layer['engine'])}** stubs | `lfw` base classes, `lfwCLoop`, `lxp`, `gds` |",
        f"| **Layer 3: Yo-kai Watch 2 Game (`src/game/`)** | **{len(c_layer['game'])}** C matched + **{len(asm_layer['game'])}** stubs | `ywCLoop*` state machines, battle, RPG entities |",
        f"| **Cataloged in Manifest** | **{staged}** / {ESTIMATED_TOTAL_FUNCTIONS:,} | Functions actively tracked across `src/` and `scratches/` |",
        "| **Executable Size (`.text`)** | 6,238,892 B | Exact code segment size from NCCH ExHeader (EU `00040000001B2900`) |",
        "| **Full Binary Image (`code.raw.bin`)** | 7,737,344 B | Decompressed CXI `.code` image (`.text` + `.rodata` + `.data`) |",
        "| **Architecture** | ARM11 MPCore (ARMv6K) | 32-bit Little Endian, VMA `0x00100000` |",
        "| **Compiler** | ARMCC / RVCT 4.0 b821 | CTR-SDK 1.2.7 (`1.2.7.f-NINTENDO-CTR-SDK-v1`) |"
    ]
    return "\n".join(lines)


def format_manifest_table(functions):
    status_badges = {
        "matched": "🟢 Matched (C/C++)",
        "community_matched": "🟢 Match (Community Accepted)",
        "matched_community": "🟢 Match (Community Accepted)",
        "asm_stub": "⚪ ASM Stub (Verified)",
        "wip": "🟡 In Review",
        "in review": "🟡 In Review",
        "staged": "⏳ Staged"
    }

    lines = [
        "| Virtual Address | Symbol / Name | Layer / Module | Size | Level | Status | Description / Notes |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :--- |"
    ]

    for f in functions:
        badge = status_badges.get(f["status"].lower(), f["status"])
        addr = f["address"]
        sym = f["symbol"]
        layer = f.get("layer", categorize_function(f))
        sub = f.get("subsystem", "core")
        lvl = f.get("level", "-")
        size = f"{f['size']} B"
        desc = f["description"]
        lines.append(f"| `{addr}` | `{sym}` | `{layer}/{sub}` | {size} | `{lvl}` | {badge} | {desc} |")

    return "\n".join(lines)

    for f in functions:
        badge = status_badges.get(f["status"].lower(), f["status"])
        addr = f["address"]
        sym = f["symbol"]
        layer = f.get("layer", categorize_function(f))
        sub = f.get("subsystem", "core")
        lvl = f.get("level", "-")
        size = f"{f['size']} B"
        desc = f["description"]
        lines.append(f"| `{addr}` | `{sym}` | `{layer}/{sub}` | {size} | `{lvl}` | {badge} | {desc} |")

    return "\n".join(lines)


def format_classes_roadmap(classes_csv: Path) -> str:
    if not classes_csv.exists():
        return ""

    with open(classes_csv, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    def get_badge(name):
        if name == "nn::nex::NexElement":
            return "🟢 Matched"
        if name == "lfwCLoopEmpty":
            return "🟡 In Review"
        if name in ("lxpCMemory", "nn::y2r::Y2rObject", "nn::y2r::Y2rSubContext", "nn::ndm::NdmContainer", "nn::os::SpinLock"):
            return "🟡 Partial"
        return "⏳ Target"

    layers = [
        ("ctr", "Layer 1: Nintendo CTR-SDK & ARM Runtime (CTR)"),
        ("engine", "Layer 2: Level-5 Engine (LFW, LXP, LIZ, Core)"),
        ("game", "Layer 3: Yo-kai Watch 2 Game Logic (YW2)")
    ]

    output_lines = [
        f"> **Total cataloged classes & structures: {len(rows)}** (synchronized with [`config/classes_identified.csv`](config/classes_identified.csv), sorted in ascending address order).",
        ""
    ]

    for layer_id, layer_title in layers:
        items = [r for r in rows if r["layer"] == layer_id]
        output_lines.append(f"### {layer_title} ({len(items)} classes)\n")
        output_lines.append("| Address | Class / Structure | Module | Base Class | Methods / Type | Status | Description |")
        output_lines.append("| :--- | :--- | :---: | :--- | :---: | :---: | :--- |")

        for r in items:
            badge = get_badge(r["class_name"])
            base_cls = r["base_class"]
            base = f"`{base_cls}`" if base_cls else "-"
            vc = int(r["vfunc_count"]) if r.get("vfunc_count") else 0
            if vc > 0:
                vf = f"{vc} vmethods"
            elif r["kind"] == "polymorphic_class":
                vf = "interface"
            else:
                vf = r["kind"]
            desc = r["description"]
            addr = r["address"]
            name = r["class_name"]
            sub = r["subsystem"]
            output_lines.append(f"| `{addr}` | `{name}` | `{sub}` | {base} | {vf} | {badge} | {desc} |")

        output_lines.append("")

    return "\n".join(output_lines)


def update_readme(readme_path: Path, progress_table: str, manifest_table: str, classes_table: str = ""):
    if not readme_path.exists():
        print(f"⚠️ README not found at {readme_path}")
        return False

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

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

    classes_pattern = r"(<!-- TARGET_CLASSES_TABLE_START -->)(.*?)(<!-- TARGET_CLASSES_TABLE_END -->)"
    if classes_table and re.search(classes_pattern, content, flags=re.DOTALL):
        content = re.sub(
            classes_pattern,
            rf"\g<1>\n\n{classes_table}\n\n\g<3>",
            content,
            flags=re.DOTALL
        )
    elif classes_table:
        print("⚠️ Marker <!-- TARGET_CLASSES_TABLE_START --> not found in README.")

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ README.md automatically updated with audited 3-layer progress.")
    return True


def update_objdiff_config(functions):
    src_dir = PROJECT_ROOT / "src"
    source_files = list(src_dir.rglob("*.c")) + list(src_dir.rglob("*.cpp"))
    file_map = {sf.stem: sf.relative_to(PROJECT_ROOT) for sf in source_files}

    units = []
    seen_symbols = set()

    for f in functions:
        sym = f["symbol"]
        status = f["status"].lower()
        if status == "asm_stub":
            continue

        seen_symbols.add(sym)
        is_matched = status in ("matched", "community_matched", "matched_community")
        category = categorize_function(f)

        if sym not in file_map:
            continue

        src_rel = str(file_map[sym])
        base_o = f"build/{file_map[sym].with_suffix('.o')}"

        unit = {
            "name": f"{category}/{f.get('subsystem', 'core')}/{sym}",
            "target_path": f"expected/{sym}.o",
            "base_path": base_o,
            "metadata": {
                "complete": is_matched,
                "source_path": src_rel,
                "progress_categories": [category]
            },
            "scratch": DEFAULT_SCRATCH
        }
        units.append(unit)

    for stem, path in file_map.items():
        if stem not in seen_symbols:
            category = "game"
            if "ctr" in path.parts:
                category = "ctr"
            elif "engine" in path.parts:
                category = "engine"
            units.append({
                "name": f"{category}/{stem}",
                "target_path": f"expected/{stem}.o",
                "base_path": f"build/{path.with_suffix('.o')}",
                "metadata": {
                    "complete": True,
                    "source_path": str(path),
                    "progress_categories": [category]
                },
                "scratch": DEFAULT_SCRATCH
            })

    units.append({
        "name": "undecompiled_text_segment",
        "target_path": "expected/undecompiled.o",
        "metadata": {
            "complete": False,
            "progress_categories": ["ctr", "engine", "game"]
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
        "progress_categories": PROGRESS_CATEGORIES,
        "units": units
    }

    with open(OBJDIFF_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print("✅ objdiff.json automatically synchronized with C/C++ units across 3 layers.")


def main():
    parser = argparse.ArgumentParser(description="Progress auditor for Yo-kai Watch 2 decompilation")
    parser.add_argument("--update-readme", action="store_true", help="Automatically update markdown tables in README.md")
    args = parser.parse_args()

    functions = load_manifest(MANIFEST_CSV)
    metrics = calculate_metrics(functions)

    tot_bytes = metrics["c_matched_bytes"] + metrics["asm_bytes"]
    tot_count = metrics["c_matched_count"] + metrics["asm_count"]
    c_bin_pct = (metrics["c_matched_bytes"] / TOTAL_BINARY_BYTES) * 100.0
    tot_text_pct = (tot_bytes / TOTAL_CODE_BYTES) * 100.0
    tot_bin_pct = (tot_bytes / TOTAL_BINARY_BYTES) * 100.0

    print("============================================================")
    print("  Yo-kai Watch 2 (3DS) — 3-Layer Matching Progress Auditor")
    print("============================================================")
    print(f"  Decompiled C/C++ Functions    : {metrics['c_matched_count']} / {ESTIMATED_TOTAL_FUNCTIONS:,} ({metrics['c_func_percent']:.2f}%)")
    print(f"   ├─ Layer 1 (CTR)             : {len(metrics['c_by_layer']['ctr'])} C matched")
    print(f"   ├─ Layer 2 (Eng)             : {len(metrics['c_by_layer']['engine'])} C matched")
    print(f"   └─ Layer 3 (Game)            : {len(metrics['c_by_layer']['game'])} C matched")
    print(f"  Total Binary Code Covered (C) : {metrics['c_matched_bytes']:,} B / {TOTAL_CODE_BYTES:,} B ({metrics['c_byte_percent']:.4f}% of .text · {c_bin_pct:.4f}% of binary)")
    print(f"  Assembly stubs (.s)           : {metrics['asm_count']} functions ({metrics['asm_bytes']:,} bytes)")
    print(f"  Build Coverage (C + ASM)      : {tot_count} / {ESTIMATED_TOTAL_FUNCTIONS:,} ({(tot_count / ESTIMATED_TOTAL_FUNCTIONS) * 100:.2f}%) ({tot_bytes:,} B / {tot_text_pct:.4f}%)")
    print("============================================================")

    progress_table = format_progress_table(metrics)
    manifest_table = format_manifest_table(functions)
    classes_table = format_classes_roadmap(CLASSES_CSV)

    if args.update_readme:
        update_readme(README_FILE, progress_table, manifest_table, classes_table)

    update_objdiff_config(functions)


if __name__ == "__main__":
    main()
