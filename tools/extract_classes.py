#!/usr/bin/env python3
"""
tools/extract_classes.py — Extracts and catalogs all identifiable C++ classes,
vtables, loop state machines, and CTR/Engine/Game structures from code.raw.bin.
Outputs: config/classes_identified.csv (sorted strictly by hexadecimal address).
"""

import csv
import os
import re
import struct
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_BIN = PROJECT_ROOT / "extracted" / "code.raw.bin"
OUTPUT_CSV = PROJECT_ROOT / "config" / "classes_identified.csv"

BASE_VMA = 0x00100000
TEXT_START = 0x00100000
TEXT_END = 0x006F32AC
RO_START = 0x006F4000
RO_END = 0x0080C42C
DATA_START = 0x0080D000
DATA_END = 0x00860934

with open(RAW_BIN, "rb") as f:
    data = f.read()

def read_u32(vma):
    off = vma - BASE_VMA
    if 0 <= off <= len(data) - 4:
        return struct.unpack("<I", data[off:off+4])[0]
    return None

def read_str(vma, max_len=128):
    off = vma - BASE_VMA
    if 0 <= off < len(data):
        end = data.find(b"\x00", off)
        if end != -1 and end - off <= max_len:
            try:
                return data[off:end].decode("ascii")
            except Exception:
                return None
    return None

def demangle(name):
    if not name:
        return ""
    if name.endswith("E") and name.startswith("N"):
        inner = name[1:-1]
        parts = []
        pos = 0
        while pos < len(inner):
            digits = re.match(r"^(\d+)", inner[pos:])
            if not digits:
                parts.append(inner[pos:])
                break
            n = int(digits.group(1))
            pos += len(digits.group(1))
            parts.append(inner[pos:pos+n])
            pos += n
        return "::".join(parts)
    digits = re.match(r"^(\d+)", name)
    if digits:
        n = int(digits.group(1))
        return name[len(digits.group(1)):len(digits.group(1))+n]
    return name

def determine_layer_subsystem(class_name):
    cn = class_name.lower()
    if cn.startswith("nn::") or cn.startswith("nex") or "ctr" in cn or "y2r" in cn or "ndm" in cn:
        if "nex" in cn:
            return "ctr", "nn_nex"
        elif "y2r" in cn:
            return "ctr", "nn_y2r"
        elif "ndm" in cn:
            return "ctr", "nn_ndm"
        elif "os" in cn:
            return "ctr", "nn_os"
        elif "fs" in cn:
            return "ctr", "nn_fs"
        return "ctr", "nn_core"
    elif cn.startswith("lfw") or cn.startswith("__lfw"):
        return "engine", "lfw"
    elif cn.startswith("lxp"):
        return "engine", "lxp"
    elif cn.startswith("liz::") or cn.startswith("res"):
        return "engine", "liz"
    elif cn.startswith("gds"):
        return "engine", "gds"
    elif cn.startswith("yw::") or cn.startswith("yw") or cn.startswith("c$"):
        if "loop" in cn:
            return "game", "loops"
        elif "battle" in cn:
            return "game", "battle"
        elif "menu" in cn:
            return "game", "menu"
        elif "rpg" in cn or "world" in cn:
            return "game", "world"
        return "game", "core"
    return "engine", "core"

# 1. Scan TypeInfos
typeinfos = {}
for vma in range(RO_START, DATA_END - 8, 4):
    off = vma - BASE_VMA
    w0, w1 = struct.unpack("<2I", data[off:off+8])
    if w0 and w1 and (RO_START <= w1 <= DATA_END):
        s = read_str(w1)
        if s and (re.match(r"^\d+[a-zA-Z0-9_]+$", s) or re.match(r"^N\d+[a-zA-Z0-9_]+E$", s)):
            base_ptr = read_u32(vma + 8)
            typeinfos[vma] = {
                "mangled": s,
                "name": demangle(s),
                "base_ti": base_ptr
            }

records = {}

# 2. Find Primary Vtables for TypeInfos (in .rodata >= 0x007F2000 with offset_to_top == 0)
vtable_map = {}
for vma in range(0x007F2000, RO_END - 8, 4):
    ti_ptr = read_u32(vma)
    if ti_ptr in typeinfos:
        off_top = struct.unpack("<i", data[vma-BASE_VMA-4:vma-BASE_VMA])[0]
        if off_top == 0 and ti_ptr not in vtable_map:
            vt = vma + 4
            # Count consecutive virtual function pointers (pointing to .text or NULL)
            cur = vt
            vfunc_count = 0
            while cur < RO_END:
                fn = read_u32(cur)
                next_val = read_u32(cur + 4)
                # If the next word is another RTTI pointer, cur is likely off_top of the next vtable
                if next_val in typeinfos and (fn == 0 or fn <= 0):
                    break
                if (TEXT_START <= fn <= TEXT_END) or fn == 0:
                    vfunc_count += 1
                    cur += 4
                else:
                    break
            vtable_map[ti_ptr] = (vt, vfunc_count)

for ti_vma, ti in typeinfos.items():
    name = ti["name"]
    base_name = ""
    if ti["base_ti"] and ti["base_ti"] in typeinfos:
        base_name = typeinfos[ti["base_ti"]]["name"]

    layer, subsys = determine_layer_subsystem(name)
    source_stem = name.split("::")[-1]
    suggested_path = f"src/{layer}/{subsys}/{source_stem}.cpp"

    if ti_vma in vtable_map:
        vt_addr, vfunc_count = vtable_map[ti_vma]
        primary_addr = vt_addr
        addr_type = "vtable"
        vt_str = f"0x{vt_addr:08X}"
        desc = f"Polymorphic C++ class ({vfunc_count} virtual methods)"
    else:
        primary_addr = ti_vma
        addr_type = "rtti_only"
        vt_str = ""
        vfunc_count = 0
        desc = "Abstract / RTTI interface descriptor"

    records[name] = {
        "address": f"0x{primary_addr:08X}",
        "raw_addr": primary_addr,
        "class_name": name,
        "layer": layer,
        "subsystem": subsys,
        "kind": "polymorphic_class",
        "address_type": addr_type,
        "vtable_address": vt_str,
        "rtti_address": f"0x{ti_vma:08X}",
        "base_class": base_name,
        "vfunc_count": vfunc_count,
        "suggested_path": suggested_path,
        "description": desc
    }

# 3. Known CTR-SDK and Engine Value Types & Structures with specific addresses in .text
known_text_items = [
    (0x00107478, "LfwLoopClassInfo", "engine", "lfw", "c_struct", "code_text", "", "", "", 0, "src/engine/lfw/lfwCLoop.cpp", "Level-5 Framework loop state machine descriptor table"),
    (0x00107478, "yw::YwLoopHeader", "game", "loops", "c_struct", "code_text", "", "", "", 0, "src/game/loops/ywCLoop.cpp", "Game loop state machine descriptor header"),
    (0x00112E60, "nn::y2r::Y2rObject", "ctr", "nn_y2r", "c_struct", "code_text", "", "", "", 0, "src/ctr/nn/y2r/func_00112E60.c", "Y2R hardware converter object context"),
    (0x00112E60, "nn::y2r::Y2rSubContext", "ctr", "nn_y2r", "c_struct", "code_text", "", "", "", 0, "src/ctr/nn/y2r/func_00112E60.c", "Y2R conversion channel sub-context descriptor"),
    (0x001274A0, "nn::os::SpinLock", "ctr", "nn_os", "c_struct", "code_text", "", "", "", 0, "src/ctr/nn/os/func_001274A0.c", "Nintendo 3DS OS hardware atomic spinlock"),
    (0x001280A8, "nn::ndm::NdmElement8", "ctr", "nn_ndm", "c_struct", "code_text", "", "", "", 0, "src/ctr/nn/ndm/func_001280A8.c", "NDM daemon 8-byte entry element"),
    (0x001280A8, "nn::ndm::NdmContainer", "ctr", "nn_ndm", "c_struct", "code_text", "", "", "", 0, "src/ctr/nn/ndm/func_001280A8.c", "NDM daemon indexed container header"),
    (0x001300B0, "lxpCMemory", "engine", "lxp", "engine_class", "code_text", "", "", "", 0, "src/engine/lxp/lxpCMemory.cpp", "Level-5 Cross-Platform memory manager"),
    (0x00340C60, "nn::nex::qResult", "ctr", "nn_nex", "value_type", "code_text", "", "", "", 0, "src/ctr/nn/nex/qResult.cpp", "NEX error result code and status wrapper"),
    (0x00340CE8, "nn::nex::NexElement", "ctr", "nn_nex", "value_type", "code_text", "", "", "", 0, "src/ctr/nn/nex/NexElement.cpp", "Network stream element / station identifier (72 B, 5 methods)"),
    (0x00340D30, "nn::nex::StationURL", "ctr", "nn_nex", "value_type", "code_text", "", "", "", 0, "src/ctr/nn/nex/StationURL.cpp", "NEX Rendez-Vous station connection URL descriptor")
]

for addr, name, layer, subsys, kind, atype, vt, rtti, base, vfc, path, desc in known_text_items:
    records[name] = {
        "address": f"0x{addr:08X}",
        "raw_addr": addr,
        "class_name": name,
        "layer": layer,
        "subsystem": subsys,
        "kind": kind,
        "address_type": atype,
        "vtable_address": vt,
        "rtti_address": rtti,
        "base_class": base,
        "vfunc_count": vfc,
        "suggested_path": path,
        "description": desc
    }

# Sort all records strictly in ascending order by hexadecimal address, then by class_name
sorted_records = sorted(records.values(), key=lambda r: (r["raw_addr"], r["class_name"]))

fieldnames = [
    "address", "class_name", "layer", "subsystem", "kind", "address_type",
    "vtable_address", "rtti_address", "base_class", "vfunc_count",
    "suggested_path", "description"
]

OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for row in sorted_records:
        writer.writerow(row)

print(f"✅ Successfully wrote {len(sorted_records)} sorted classes to {OUTPUT_CSV}")
