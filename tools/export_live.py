#!/usr/bin/env python3
"""
tools/export_live.py — Export current working status and decompilation metrics
to lightweight JSON and TXT files for stream overlays, dashboards, and integrations.

Outputs:
  - live.json: Full structured metadata (current function, layer, progress %, timestamp)
  - live.txt:  Single-line text formatted for OBS Text Sources and stream banners
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
MANIFEST_CSV = CONFIG_DIR / "functions.csv"
CURRENT_TASK_FILE = PROJECT_ROOT / ".current_task"

OUT_JSON = PROJECT_ROOT / "live.json"
OUT_TXT = PROJECT_ROOT / "live.txt"

TOTAL_CODE_BYTES = 6238892
TOTAL_BINARY_BYTES = 7737344
ESTIMATED_TOTAL_FUNCTIONS = 18225

LAYER_NAMES = {
    "ctr": "Nintendo CTR-SDK",
    "engine": "Level-5 Engine (lfw/lxp/gds)",
    "game": "Yo-kai Watch 2 Game Logic"
}


def load_manifest():
    functions = []
    if not MANIFEST_CSV.exists():
        return functions
    with open(MANIFEST_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                r["size"] = int(r["size"])
            except ValueError:
                r["size"] = 0
            functions.append(r)
    return functions


def detect_active_symbol(functions, override_symbol=None):
    if override_symbol:
        return override_symbol

    if CURRENT_TASK_FILE.exists():
        try:
            with open(CURRENT_TASK_FILE, "r", encoding="utf-8") as f:
                sym = f.read().strip()
                if sym:
                    return sym
        except OSError:
            pass

    # Check git modified / untracked files in src/
    try:
        import subprocess
        git_out = subprocess.check_output(
            ["git", "status", "--porcelain", "src/"],
            cwd=str(PROJECT_ROOT),
            text=True
        )
        for line in git_out.splitlines():
            m = re.search(r"(func_[0-9a-fA-F]{8}|[a-zA-Z0-9_]+)\.c", line)
            if m:
                cand = m.group(1)
                # verify it's in manifest
                for fn in functions:
                    if fn["symbol"] == cand:
                        return cand
    except Exception:
        pass

    # Fallback to last WIP function in functions.csv (most recently assigned)
    wips = [f for f in functions if f["status"].lower() in ("wip", "in review")]
    if wips:
        return wips[-1]["symbol"]

    return None


def compute_status(functions, symbol_name=None, custom_task=None):
    src_dir = PROJECT_ROOT / "src"
    asm_stems = {sf.stem for sf in src_dir.rglob("*.s")}

    c_matched = [
        f for f in functions
        if f["status"].lower() in ("matched", "community_matched")
        and f["symbol"] not in asm_stems
    ]

    layer_counts = {"ctr": 0, "engine": 0, "game": 0}
    for f in c_matched:
        l = f.get("layer", "game").lower()
        if l in layer_counts:
            layer_counts[l] += 1
        else:
            layer_counts["game"] += 1

    matched_count = len(c_matched)
    matched_bytes = sum(f["size"] for f in c_matched)
    pct_funcs = (matched_count / ESTIMATED_TOTAL_FUNCTIONS) * 100.0
    pct_bytes = (matched_bytes / TOTAL_CODE_BYTES) * 100.0

    current = None
    if symbol_name:
        for f in functions:
            if f["symbol"] == symbol_name or f["address"].lower() == symbol_name.lower():
                current = f
                break

    if current:
        symbol = current["symbol"]
        address = current["address"]
        layer = current.get("layer", "ctr")
        subsystem = current.get("subsystem", "core")
        desc = current.get("description", "")
        size = current["size"]
        layer_name = LAYER_NAMES.get(layer, layer)
        task_title = custom_task or f"{symbol} ({address})"
        stream_text = f"Yo-kai Watch 2 Decomp | {task_title} | {layer}/{subsystem} | {matched_count}/{ESTIMATED_TOTAL_FUNCTIONS:,} ({pct_funcs:.2f}%)"
    else:
        symbol = None
        address = None
        layer = None
        subsystem = None
        desc = custom_task or "Investigando binario / matching"
        size = 0
        layer_name = ""
        task_title = desc
        stream_text = f"Yo-kai Watch 2 Decomp | {task_title} | {matched_count}/{ESTIMATED_TOTAL_FUNCTIONS:,} ({pct_funcs:.2f}%)"

    now_iso = datetime.now().astimezone().isoformat()

    live_data = {
        "project": {
            "name": "Yo-kai Watch 2: Psychic Specters",
            "japanese_title": "妖怪ウォッチ2 真打",
            "platform": "Nintendo 3DS (CTR)",
            "title_id": "00040000001B2900",
            "region": "EUR (CTR-P-BYPP)"
        },
        "status": "decompiling" if current else "researching",
        "current_task": {
            "symbol": symbol,
            "address": address,
            "layer": layer,
            "layer_name": layer_name,
            "subsystem": subsystem,
            "size_bytes": size,
            "description": desc,
            "display_title": task_title
        },
        "progress": {
            "functions_matched": matched_count,
            "functions_total": ESTIMATED_TOTAL_FUNCTIONS,
            "functions_percent": round(pct_funcs, 2),
            "code_bytes_matched": matched_bytes,
            "code_bytes_total": TOTAL_CODE_BYTES,
            "code_bytes_percent": round(pct_bytes, 4),
            "layers": layer_counts
        },
        "stream_label": stream_text,
        "updated_at": now_iso
    }

    return live_data, stream_text


def main():
    parser = argparse.ArgumentParser(description="Export live status for stream overlays")
    parser.add_argument("--symbol", help="Set active function symbol or address")
    parser.add_argument("--task", help="Custom task description (e.g. 'Auditoría de vtables')")
    parser.add_argument("--save", action="store_true", help="Persist symbol to .current_task")
    args = parser.parse_args()

    functions = load_manifest()
    active_sym = detect_active_symbol(functions, override_symbol=args.symbol)

    if args.symbol and (args.save or True):
        with open(CURRENT_TASK_FILE, "w", encoding="utf-8") as f:
            f.write(args.symbol + "\n")

    data, stream_text = compute_status(functions, symbol_name=active_sym, custom_task=args.task)

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write(stream_text + "\n")

    print(f"📡 Estado en directo exportado:")
    print(f"   -> JSON: {OUT_JSON}")
    print(f"   -> TXT : {OUT_TXT}")
    print(f"   [Label]: \"{stream_text}\"")


if __name__ == "__main__":
    main()
