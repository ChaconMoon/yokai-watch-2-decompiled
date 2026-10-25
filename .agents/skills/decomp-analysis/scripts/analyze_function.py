#!/usr/bin/env python3
"""
.agents/skills/decomp-analysis/scripts/analyze_function.py

Universal Nintendo 3DS (ARM11 MPCore / ARMv6K) Function Decompilation Analyzer.
Designed for Yo-kai Watch 2: Psychic Specters and extrapolable to any 3DS project.

Given a function address, symbol name, or partial identifier, this script extracts:
  1. Clean ARM/Thumb disassembly (both annotated and decomp.me-ready)
  2. Literal pool values, strings, vtable/RTTI pointers, and subcalls
  3. Cross-references (XREFs: callers via BL/BLX and pointers in .text/.rodata/.data)
  4. Automated structural analysis (registers, stack frame, memory offsets, control flow)
  5. Hierarchical classification: Namespace, Layer/Submodule, and Class
  6. Proposed demangled C++ signature, mangled symbol, and target paths (src/ & include/)
"""

import argparse
import csv
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

# Auto-detect project root (supports running from .agents/skills/decomp-analysis/scripts/ or tools/)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR
for parent in [SCRIPT_DIR] + list(SCRIPT_DIR.parents):
    if (parent / "Makefile").exists() or (parent / "extracted").exists() or (parent / ".git").exists():
        PROJECT_ROOT = parent
        break

DEFAULT_BIN = PROJECT_ROOT / "extracted" / "code.raw.bin"
if not DEFAULT_BIN.exists() and (PROJECT_ROOT / "extracted" / "code.bin").exists():
    DEFAULT_BIN = PROJECT_ROOT / "extracted" / "code.bin"

DEFAULT_CONFIG_DIR = PROJECT_ROOT / "config"
DEFAULT_BASE_VMA = 0x00100000

LINE_RE = re.compile(r"^\s*([0-9a-fA-F]+):\s+([0-9a-fA-F]{4,8})\s+(.*)$")
BRANCH_RE = re.compile(
    r"^(blx?|b(?:eq|ne|cs|hs|cc|lo|mi|pl|vs|vc|hi|ls|ge|lt|gt|le)?|cbz|cbnz)\s+(?:r\d+,\s*)?(?:0x)?([0-9a-fA-F]+)"
)


def is_call_opcode(op: str) -> bool:
    return op in ("bl", "blx")

MEM_ACCESS_RE = re.compile(
    r"^(ldr|ldrh|ldrb|ldrsb|ldrsh|ldrd|str|strh|strb|strd)(?:eq|ne|cs|hs|cc|lo|mi|pl|vs|vc|hi|ls|ge|lt|gt|le)?\s+"
    r"([a-z0-9]+),\s*\[([a-z0-9]+)(?:,\s*#(-?(?:0x)?[0-9a-fA-F]+))?\](\!)?"
)

SVC_NAMES = {
    0x01: "svcControlMemory",
    0x02: "svcQueryMemory",
    0x03: "svcExitProcess",
    0x08: "svcCreateThread",
    0x09: "svcExitThread",
    0x0A: "svcSleepThread",
    0x0B: "svcGetThreadPriority",
    0x0C: "svcSetThreadPriority",
    0x13: "svcCreateMutex",
    0x14: "svcReleaseMutex",
    0x17: "svcCreateEvent",
    0x18: "svcSignalEvent",
    0x19: "svcClearEvent",
    0x1A: "svcCreateTimer",
    0x1F: "svcCreateMemoryBlock",
    0x21: "svcCreateAddressArbiter",
    0x22: "svcArbitrateAddress",
    0x23: "svcCloseHandle",
    0x24: "svcWaitSynchronization1",
    0x25: "svcWaitSynchronizationN",
    0x27: "svcDuplicateHandle",
    0x28: "svcGetSystemTick",
    0x2D: "svcConnectToPort",
    0x32: "svcSendSyncRequest",
    0x35: "svcGetProcessId",
    0x37: "svcGetThreadId",
    0x38: "svcGetResourceLimit",
    0x3C: "svcBreak",
}


def load_memory_map(config_dir: Path, bin_size: int, base_vma: int) -> dict:
    mmap_path = config_dir / "memory_map.json"
    if mmap_path.exists():
        try:
            with open(mmap_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            sections = data.get("sections", {})
            if sections:
                return {
                    "text_start": int(sections.get(".text", {}).get("vma_start", f"0x{base_vma:08X}"), 16),
                    "text_end": int(sections.get(".text", {}).get("vma_end", "0x006F32AC"), 16),
                    "rodata_start": int(sections.get(".rodata", {}).get("vma_start", "0x006F4000"), 16),
                    "rodata_end": int(sections.get(".rodata", {}).get("vma_end", "0x0080C42C"), 16),
                    "data_start": int(sections.get(".data", {}).get("vma_start", "0x0080D000"), 16),
                    "data_end": int(sections.get(".data", {}).get("vma_end", "0x00860934"), 16),
                    "bss_start": int(sections.get(".bss", {}).get("vma_start", "0x00860934"), 16),
                    "bss_end": int(sections.get(".bss", {}).get("vma_end", "0x0091B9BC"), 16),
                }
        except Exception:
            pass
    return {
        "text_start": base_vma,
        "text_end": min(base_vma + bin_size, 0x006F32AC),
        "rodata_start": 0x006F4000,
        "rodata_end": 0x0080C42C,
        "data_start": 0x0080D000,
        "data_end": 0x00860934,
        "bss_start": 0x00860934,
        "bss_end": 0x0091B9BC,
    }


def classify_vma_section(vma: int, mmap: dict) -> str:
    if mmap["text_start"] <= vma < mmap["text_end"]:
        return ".text"
    if mmap["rodata_start"] <= vma < mmap["rodata_end"]:
        return ".rodata"
    if mmap["data_start"] <= vma < mmap["data_end"]:
        return ".data"
    if mmap["bss_start"] <= vma < mmap["bss_end"]:
        return ".bss"
    if 0x1FF80000 <= vma < 0x1FF82000:
        return "CFG_MEM (3DS Shared Config Page)"
    if 0x1EC00000 <= vma < 0x1F600000:
        return "IO_VRAM"
    return "external/constant"


def read_ascii_string(raw_bytes: bytes, base_vma: int, vma: int, max_len: int = 80):
    off = vma - base_vma
    if 0 <= off < len(raw_bytes):
        end = raw_bytes.find(b"\x00", off, off + max_len)
        if end != -1 and end > off:
            chunk = raw_bytes[off:end]
            if all(32 <= b < 127 for b in chunk):
                return chunk.decode("ascii")
    return None


def load_catalogs(config_dir: Path):
    functions_by_addr = {}
    functions_by_sym = {}
    classes_list = []

    # 1. Load functions_classified.csv
    classified_path = config_dir / "functions_classified.csv"
    if classified_path.exists():
        with open(classified_path, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    addr = int(row["address"], 0)
                    entry = {
                        "address": addr,
                        "symbol": row["symbol"],
                        "size": int(row["size"]),
                        "layer": row.get("layer", ""),
                        "subsystem": row.get("subsystem", ""),
                        "difficulty": row.get("difficulty", ""),
                        "description": row.get("description", ""),
                        "status": "unmatched",
                    }
                    functions_by_addr[addr] = entry
                    functions_by_sym[row["symbol"].lower()] = entry
                except (ValueError, KeyError):
                    continue

    # 2. Load ykw_2_identify_fuctions.csv (fallback for any missing entry)
    ident_path = config_dir / "ykw_2_identify_fuctions.csv"
    if ident_path.exists():
        with open(ident_path, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    addr = int(row["Location"], 16)
                    if addr not in functions_by_addr:
                        entry = {
                            "address": addr,
                            "symbol": row.get("Name", f"func_{addr:08X}"),
                            "size": int(row.get("Function Size", "0")),
                            "layer": "",
                            "subsystem": "",
                            "difficulty": "",
                            "description": "",
                            "status": "unmatched",
                        }
                        functions_by_addr[addr] = entry
                        functions_by_sym[entry["symbol"].lower()] = entry
                except (ValueError, KeyError):
                    continue

    # 3. Load canonical functions.csv (highest precedence)
    for manifest_name in ["functions_candidates.csv", "functions.csv"]:
        mpath = config_dir / manifest_name
        if mpath.exists():
            with open(mpath, "r", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    try:
                        addr = int(row["address"], 0)
                        entry = {
                            "address": addr,
                            "symbol": row["symbol"],
                            "size": int(row["size"]),
                            "layer": row.get("layer", ""),
                            "subsystem": row.get("subsystem", ""),
                            "difficulty": row.get("level", ""),
                            "description": row.get("description", ""),
                            "status": row.get("status", "matched"),
                        }
                        functions_by_addr[addr] = entry
                        functions_by_sym[row["symbol"].lower()] = entry
                    except (ValueError, KeyError):
                        continue

    # 4. Load classes_identified.csv
    classes_path = config_dir / "classes_identified.csv"
    if classes_path.exists():
        with open(classes_path, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    row["raw_addr"] = int(row["address"], 0)
                    row["raw_vtable"] = int(row["vtable_address"], 0) if row.get("vtable_address") else None
                    classes_list.append(row)
                except (ValueError, KeyError):
                    continue

    return functions_by_addr, functions_by_sym, classes_list


def scan_headers_for_address(project_root: Path, addr: int):
    """Scans include/ and src/ for comments mentioning the hex address (e.g. 00340E5C)."""
    hex_short = f"{addr:06X}"
    hex_full = f"{addr:08X}"
    pattern = re.compile(rf"(?:0x)?(?:00)?{hex_short}\b", re.IGNORECASE)
    matches = []

    for folder in ["include", "src"]:
        base_dir = project_root / folder
        if not base_dir.exists():
            continue
        for path in sorted(base_dir.rglob("*")):
            if not path.is_file() or path.suffix not in (".h", ".hpp", ".c", ".cpp"):
                continue
            try:
                lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
            except Exception:
                continue
            current_ns = []
            current_class = None
            for idx, line in enumerate(lines, 1):
                ns_m = re.match(r"^\s*namespace\s+([a-zA-Z0-9_]+)", line)
                if ns_m:
                    current_ns.append(ns_m.group(1))
                cls_m = re.match(r"^\s*(?:class|struct)\s+([a-zA-Z0-9_]+)\s*(?::|{|$)", line)
                if cls_m and ";" not in line:
                    current_class = cls_m.group(1)
                if pattern.search(line):
                    matches.append({
                        "file": str(path.relative_to(project_root)),
                        "line": idx,
                        "text": line.strip(),
                        "namespace": "::".join(current_ns),
                        "class_name": current_class,
                    })
    return matches


def resolve_target(target: str, functions_by_addr: dict, functions_by_sym: dict):
    clean = target.strip()
    # Try direct hex or func_XXXXXXXX / FUN_xxxxxxxx
    m_func = re.match(r"^(?:func_|FUN_|sub_)?(?:0x)?([0-9a-fA-F]{6,8})$", clean)
    if m_func:
        addr = int(m_func.group(1), 16)
        if addr in functions_by_addr:
            return functions_by_addr[addr]
        return {
            "address": addr,
            "symbol": f"func_{addr:08X}",
            "size": 0,
            "layer": "",
            "subsystem": "",
            "difficulty": "",
            "description": "",
            "status": "unmatched",
        }

    # Try exact symbol match
    if clean.lower() in functions_by_sym:
        return functions_by_sym[clean.lower()]

    # Try substring match on symbol or description
    for addr, info in sorted(functions_by_addr.items()):
        if clean.lower() in info["symbol"].lower() or clean.lower() in info.get("description", "").lower():
            return info

    return None


def auto_detect_size(raw_bytes: bytes, base_vma: int, addr: int, functions_by_addr: dict) -> int:
    """Heuristically detects function size if not in catalog or if size == 0."""
    # Check next known function in catalog
    sorted_addrs = sorted(functions_by_addr.keys())
    for next_addr in sorted_addrs:
        if next_addr > addr and (next_addr - addr) <= 512:
            # Also scan for bx lr or pop {..., pc} before next_addr
            break

    off = addr - base_vma
    max_scan = min(512, len(raw_bytes) - off)
    for i in range(0, max_scan, 4):
        word = struct.unpack_from("<I", raw_bytes, off + i)[0]
        # bx lr (0xE12FFF1E) or pop {..., pc} (0xE8BD8xxx) or ldr pc, [sp], #4 (0xE49DF004)
        if word == 0xE12FFF1E or (word & 0xFFFF8000) == 0xE8BD8000 or word == 0xE49DF004:
            return i + 4
    return 32


def find_xrefs(raw_bytes: bytes, base_vma: int, text_end: int, target_addr: int, max_xrefs: int = 15):
    """Scans binary for direct BL calls and 32-bit pointer references (vtables, tables)."""
    callers = []
    ptr_refs = []
    text_len = min(text_end - base_vma, len(raw_bytes))

    # 1. Scan .text for BL <target_addr>
    for off in range(0, text_len - 3, 4):
        insn = struct.unpack_from("<I", raw_bytes, off)[0]
        # BL / BLX cond: top nibble 0xE or cond, bits 27..24 == 0xB
        if ((insn >> 24) & 0x0F) == 0x0B:
            imm24 = insn & 0x00FFFFFF
            if imm24 & 0x00800000:
                imm24 -= 0x01000000
            pc = base_vma + off + 8
            dest = pc + (imm24 << 2)
            if dest == target_addr:
                callers.append(base_vma + off)
                if len(callers) >= max_xrefs:
                    break

    # 2. Scan whole binary for 32-bit pointer equal to target_addr
    target_bytes = struct.pack("<I", target_addr)
    pos = 0
    while len(ptr_refs) < max_xrefs:
        idx = raw_bytes.find(target_bytes, pos)
        if idx == -1:
            break
        if idx % 4 == 0:
            ptr_refs.append(base_vma + idx)
        pos = idx + 4

    return callers, ptr_refs


def infer_hierarchy(
    addr: int,
    meta: dict,
    header_matches: list,
    ptr_refs: list,
    literal_pool_info: list,
    functions_by_addr: dict,
    classes_list: list,
):
    """
    Determines:
      - layer ('ctr', 'engine', 'game')
      - submodule (e.g. 'nn/nex', 'svc', 'lfw', 'lxp', 'loops', 'core')
      - namespace (e.g. 'nn::nex', 'nn::os', 'lfw', 'yw', or '')
      - class_name (e.g. 'StationConnectionInfo', 'NexElement', 'qResult', etc.)
    """
    layer = meta.get("layer", "")
    subsys = meta.get("subsystem", "")
    namespace = ""
    class_name = ""

    # 1. Check if already mentioned in a header/source file
    for hm in header_matches:
        if hm.get("namespace"):
            namespace = hm["namespace"]
        if hm.get("class_name"):
            class_name = hm["class_name"]

    # 2. Check if description or symbol already has Class::method
    desc = meta.get("description", "")
    m_desc_cpp = re.match(r"^([a-zA-Z0-9_:]+)::([~a-zA-Z0-9_]+|operator[^\s(]+)\s*\(", desc)
    if m_desc_cpp:
        scope = m_desc_cpp.group(1)
        parts = scope.split("::")
        class_name = parts[-1]
        if len(parts) > 1:
            namespace = "::".join(parts[:-1])

    # 3. Check literal pool references to vtables in classes_identified.csv
    if not class_name:
        for lp in literal_pool_info:
            val = lp["value"]
            for cls in classes_list:
                if cls.get("raw_vtable") and abs(val - cls["raw_vtable"]) <= 8:
                    full_cls = cls["class_name"]
                    parts = full_cls.split("::")
                    class_name = parts[-1]
                    if len(parts) > 1:
                        namespace = "::".join(parts[:-1])
                    layer = cls["layer"]
                    subsys = cls["subsystem"]
                    break

    # 4. Check if pointer references hit a known vtable
    if not class_name:
        for ref_vma in ptr_refs:
            for cls in classes_list:
                vt = cls.get("raw_vtable")
                if vt and vt <= ref_vma < vt + int(cls.get("vfunc_count", 0)) * 4 + 16:
                    full_cls = cls["class_name"]
                    parts = full_cls.split("::")
                    class_name = parts[-1]
                    if len(parts) > 1:
                        namespace = "::".join(parts[:-1])
                    layer = cls["layer"]
                    subsys = cls["subsystem"]
                    break

    # 5. Check neighboring functions within +/- 0x150 bytes for known class context
    if not class_name:
        for delta in range(-0x150, 0x154, 4):
            near_addr = addr + delta
            if near_addr in functions_by_addr:
                near_desc = functions_by_addr[near_addr].get("description", "")
                m_near = re.match(r"^([a-zA-Z0-9_:]+)::([~a-zA-Z0-9_]+|operator[^\s(]+)", near_desc)
                if m_near:
                    scope = m_near.group(1)
                    parts = scope.split("::")
                    class_name = parts[-1]
                    if len(parts) > 1 and not namespace:
                        namespace = "::".join(parts[:-1])
                    if not layer:
                        layer = functions_by_addr[near_addr].get("layer", "")
                    if not subsys:
                        subsys = functions_by_addr[near_addr].get("subsystem", "")
                    break

    # 6. Fallback layer/subsystem from address ranges if not set
    if not layer or not subsys:
        if 0x00100000 <= addr < 0x00104770:
            layer, subsys = "ctr", "crt"
        elif 0x00104770 <= addr < 0x00107400 or 0x00127000 <= addr < 0x00128500:
            layer, subsys = "ctr", "nn_os"
        elif 0x0010B500 <= addr < 0x0010C800 or 0x00124000 <= addr < 0x00126800:
            layer, subsys = "engine", "lfw"
        elif 0x0010C800 <= addr < 0x00112500:
            layer, subsys = "game", "loops"
        elif 0x00112500 <= addr < 0x00114000:
            layer, subsys = "ctr", "nn_y2r"
        elif 0x0012A000 <= addr < 0x00136000 or 0x00200000 <= addr < 0x00260000:
            layer, subsys = "engine", "lxp"
        elif 0x00136000 <= addr < 0x00139000:
            layer, subsys = "ctr", "nn_dsp"
        elif 0x00280000 <= addr < 0x00300000:
            layer, subsys = "ctr", "nn_cecd"
        elif 0x00300000 <= addr < 0x00370000:
            layer, subsys = "ctr", "nn_nex"
        elif 0x00580000 <= addr < 0x006F32AC:
            layer, subsys = "engine", "core"
        else:
            layer, subsys = "game", "core"

    # Map subsystem to directory path and default namespace
    subsys_dir_map = {
        "nn_nex": ("nn/nex", "nn::nex", "include/ctr/nex.h"),
        "nn_os": ("nn/os", "nn::os", "include/ctr/os.h"),
        "nn_ndm": ("nn/ndm", "nn::ndm", "include/ctr/ndm.h"),
        "nn_y2r": ("nn/y2r", "nn::y2r", "include/ctr/y2r.h"),
        "nn_dsp": ("nn/dsp", "nn::dsp", "include/ctr/dsp.h"),
        "nn_cecd": ("nn/cecd", "nn::cecd", "include/ctr/cecd.h"),
        "svc": ("svc", "", "include/ctr/svc.h"),
        "crt": ("crt", "", "include/common.h"),
        "lfw": ("lfw", "lfw", "include/engine/lfw.h"),
        "lxp": ("lxp", "lxp", "include/engine/lxp.h"),
        "gds": ("gds", "gds", "include/engine/gds.h"),
        "loops": ("loops", "yw", "include/game/loops.h"),
    }
    sub_dir, default_ns, header_path = subsys_dir_map.get(
        subsys, (subsys or "core", "", f"include/{layer}/{subsys or 'core'}.h")
    )
    if not namespace:
        namespace = default_ns

    if class_name:
        src_path = f"src/{layer}/{sub_dir}/{class_name}.cpp"
    else:
        sym = meta.get("symbol", f"func_{addr:08X}")
        if sym.startswith("FUN_"):
            sym = f"func_{addr:08X}"
        ext = ".cpp" if namespace and "::" in namespace else ".c"
        src_path = f"src/{layer}/{sub_dir}/{sym}{ext}"

    return {
        "layer": layer,
        "subsystem": subsys,
        "submodule_dir": f"{layer}/{sub_dir}",
        "namespace": namespace or "(global / extern \"C\")",
        "class_name": class_name or "(Standalone / C struct function)",
        "src_path": src_path,
        "header_path": header_path,
    }


def mangle_itanium_method(namespace: str, class_name: str, method_name: str, is_const: bool = False, args_code: str = "v") -> str:
    """Generates the ARMCC / Itanium C++ ABI mangled symbol for a class method."""
    if not class_name or class_name.startswith("("):
        return method_name
    parts = []
    if namespace and not namespace.startswith("("):
        parts.extend([p for p in namespace.split("::") if p])
    parts.append(class_name)

    prefix = "_ZNK" if is_const else "_ZN"
    encoded_scope = ""
    for idx, p in enumerate(parts):
        encoded_scope += f"{len(p)}{p}"

    if method_name == class_name:
        m_part = "C1"
    elif method_name == f"~{class_name}":
        m_part = "D1"
    elif method_name == "operator=":
        m_part = "aS"
    elif method_name == "operator==":
        m_part = "eq"
    elif method_name == "operator!=":
        m_part = "ne"
    elif method_name == "operator<":
        m_part = "lt"
    else:
        m_part = f"{len(method_name)}{method_name}"

    return f"{prefix}{encoded_scope}{m_part}E{args_code}"


def analyze_instructions(
    addr: int,
    size: int,
    parsed_lines: list,
    pool_targets: set,
    branch_targets: set,
    raw_bytes: bytes,
    base_vma: int,
    mmap: dict,
    functions_by_addr: dict,
    hierarchy: dict,
):
    """Performs semantic analysis of instructions, registers, memory offsets, and calls."""
    mem_accesses = []
    subcalls = []
    syscalls = []
    literal_loads = []
    has_stack_frame = False
    pushed_regs = ""
    writes_to_r0_fields = []
    reads_from_r0_fields = []
    reads_from_r1_fields = []
    has_self_comparison = False
    r0_modified = False
    stores_vtable = None

    # Map literal pool address -> 32-bit value
    pool_values = {}
    for pt in sorted(pool_targets):
        off = pt - base_vma
        if 0 <= off <= len(raw_bytes) - 4:
            val = struct.unpack_from("<I", raw_bytes, off)[0]
            pool_values[pt] = val

    for line_addr, hexval, rest in parsed_lines:
        if line_addr in pool_targets:
            continue
        insn = re.sub(r"\s+@.*$", "", rest).replace("\t", " ").strip()

        # Check push prologue
        if insn.startswith("push "):
            has_stack_frame = True
            pushed_regs = insn[5:].strip()

        # Check SVC
        m_svc = re.match(r"^svc\s+(?:0x)?([0-9a-fA-F]+)", insn)
        if m_svc:
            svc_id = int(m_svc.group(1), 16)
            syscalls.append((svc_id, SVC_NAMES.get(svc_id, f"svc_{svc_id:02X}")))

        # Check self-comparison (cmp r0, r1 / cmp r0, r4) before r0 is overwritten
        if not r0_modified and re.match(r"^cmp\s+r0,\s*r[14]$", insn):
            has_self_comparison = True
        if re.match(r"^(?:mov|sub|add|ldr|mvn)\s+r0,", insn):
            r0_modified = True

        # Check PC-relative literal pool load
        if re.search(r"ldr[a-z0-9]*\s+([a-z0-9]+),\s*\[pc", rest, re.IGNORECASE):
            reg = insn.split(",")[0].split()[1]
            cm = re.search(r"@\s*(?:0x)?([0-9a-fA-F]+)", rest)
            if cm:
                t_addr = int(cm.group(1), 16)
                val = pool_values.get(t_addr)
                if val is not None:
                    sec = classify_vma_section(val, mmap)
                    s_lit = read_ascii_string(raw_bytes, base_vma, val)
                    literal_loads.append({
                        "insn_addr": line_addr,
                        "reg": reg,
                        "pool_addr": t_addr,
                        "value": val,
                        "section": sec,
                        "string": s_lit,
                    })
                    if sec == ".rodata" and 0x007F2000 <= val < 0x0080C42C:
                        stores_vtable = val

        # Check struct field memory access
        mm = MEM_ACCESS_RE.match(insn)
        if mm:
            op, rd, rn, imm_str, writeback = mm.groups()
            if rn != "pc" and rn != "sp":
                imm_val = int(imm_str, 0) if imm_str else 0
                type_map = {
                    "ldr": ("read", "u32 / s32 / ptr", 4),
                    "ldrh": ("read", "u16", 2),
                    "ldrsh": ("read", "s16", 2),
                    "ldrb": ("read", "u8", 1),
                    "ldrsb": ("read", "s8", 1),
                    "ldrd": ("read", "u64", 8),
                    "str": ("write", "u32 / s32 / ptr", 4),
                    "strh": ("write", "u16", 2),
                    "strb": ("write", "u8", 1),
                    "strd": ("write", "u64", 8),
                }
                rw, ctype, width = type_map.get(op, ("access", "u32", 4))
                mem_accesses.append({
                    "addr": line_addr,
                    "op": op,
                    "rw": rw,
                    "reg": rd,
                    "base": rn,
                    "offset": imm_val,
                    "type": ctype,
                    "width": width,
                })
                if rn in ("r0", "r5", "r6"):
                    if rw == "write":
                        writes_to_r0_fields.append((imm_val, ctype, op))
                    else:
                        reads_from_r0_fields.append((imm_val, ctype, op))
                elif rn in ("r1", "r4", "r7") and rw == "read":
                    reads_from_r1_fields.append((imm_val, ctype, op))

        # Check subcalls (BL / BLX or tail-calls outside function bounds)
        bm = BRANCH_RE.match(insn)
        if bm:
            op = bm.group(1)
            target_b = int(bm.group(2), 16)
            if is_call_opcode(op) or not (addr <= target_b < addr + size):
                callee_info = functions_by_addr.get(target_b, {})
                callee_sym = callee_info.get("symbol", f"func_{target_b:08X}")
                callee_desc = callee_info.get("description", "")
                subcalls.append({
                    "insn_addr": line_addr,
                    "op": op,
                    "target": target_b,
                    "symbol": callee_sym,
                    "description": callee_desc,
                })

    # Propose function name and signature based on pattern heuristics
    cls = hierarchy["class_name"]
    ns = hierarchy["namespace"]
    has_cls = cls and not cls.startswith("(")
    full_scope = f"{ns}::{cls}" if (has_cls and ns and not ns.startswith("(")) else (cls if has_cls else "")

    existing_sym = functions_by_addr.get(addr, {}).get("symbol", f"func_{addr:08X}")
    existing_desc = functions_by_addr.get(addr, {}).get("description", "")

    proposed_cpp_name = existing_sym
    proposed_signature = f"void {existing_sym}(void)"
    mangled_name = existing_sym

    if syscalls and size <= 36:
        svc_id, svc_name = syscalls[0]
        proposed_cpp_name = svc_name
        proposed_signature = f"Result {svc_name}(...)"
        mangled_name = svc_name
    elif existing_desc and "::" in existing_desc:
        proposed_cpp_name = existing_desc.split("(")[0].strip()
        proposed_signature = existing_desc
        mangled_name = existing_sym
    elif has_cls:
        # Heuristic method identification for C++ classes
        if stores_vtable is not None:
            if any("C1" in c["symbol"] or "D08" in f"{c['target']:X}" for c in subcalls):
                proposed_cpp_name = f"{full_scope}::{cls}"
                proposed_signature = f"{full_scope}::{cls}()"
                mangled_name = mangle_itanium_method(ns, cls, cls, False, "v")
            elif any("aS" in c["symbol"] or "CE8" in f"{c['target']:X}" for c in subcalls):
                proposed_cpp_name = f"{full_scope}::{cls}"
                proposed_signature = f"{full_scope}::{cls}(const {cls} &other)"
                mangled_name = mangle_itanium_method(ns, cls, cls, False, f"RKS1_")
            else:
                proposed_cpp_name = f"{full_scope}::~{cls}"
                proposed_signature = f"{full_scope}::~{cls}()"
                mangled_name = mangle_itanium_method(ns, cls, f"~{cls}", False, "v")
        elif has_self_comparison and subcalls:
            proposed_cpp_name = f"{full_scope}::operator="
            proposed_signature = f"{cls} &{full_scope}::operator=(const {cls} &other)"
            mangled_name = mangle_itanium_method(ns, cls, "operator=", False, "RKS1_")
        elif any(lp["value"] == 0xE0E14826 for lp in literal_loads):
            proposed_cpp_name = f"{full_scope}::readFromBuffer"
            proposed_signature = f"u32 {full_scope}::readFromBuffer(const u8 *buffer)"
            mangled_name = mangle_itanium_method(ns, cls, "readFromBuffer", False, "PKh")
        elif len(subcalls) >= 2 and any(c["target"] == 0x0063A6E8 for c in subcalls):
            proposed_cpp_name = f"{full_scope}::compare"
            proposed_signature = f"s32 {full_scope}::compare(const {cls} &other) const"
            mangled_name = mangle_itanium_method(ns, cls, "compare", True, "RKS1_")
        elif not subcalls and writes_to_r0_fields and not reads_from_r0_fields:
            if all(off != 0 for off, _, _ in writes_to_r0_fields) and len(writes_to_r0_fields) == 1:
                off, ctype, _ = writes_to_r0_fields[0]
                proposed_cpp_name = f"{full_scope}::setField_{off:02X}"
                proposed_signature = f"u32 {full_scope}::setField_{off:02X}({ctype.split()[0]} val)"
            else:
                proposed_cpp_name = f"{full_scope}::reset"
                proposed_signature = f"void {full_scope}::reset()"
        elif not subcalls and reads_from_r0_fields and not writes_to_r0_fields:
            off, ctype, _ = reads_from_r0_fields[0]
            proposed_cpp_name = f"{full_scope}::getField_{off:02X}"
            proposed_signature = f"{ctype.split()[0]} {full_scope}::getField_{off:02X}() const"
        else:
            m_name = f"func_{addr:08X}"
            proposed_cpp_name = f"{full_scope}::{m_name}"
            proposed_signature = f"u32 {full_scope}::{m_name}(...)"
    else:
        if size == 4 and not mem_accesses and not subcalls:
            proposed_cpp_name = f"func_{addr:08X}"
            proposed_signature = f"void func_{addr:08X}(void)"
        elif literal_loads and len(mem_accesses) == 1 and not subcalls:
            rw = mem_accesses[0]["rw"]
            ctype = mem_accesses[0]["type"].split()[0]
            if rw == "read":
                proposed_cpp_name = f"func_{addr:08X}"
                proposed_signature = f"{ctype} func_{addr:08X}(void)"
            else:
                proposed_cpp_name = f"func_{addr:08X}"
                proposed_signature = f"void func_{addr:08X}({ctype} value)"

    return {
        "has_stack_frame": has_stack_frame,
        "pushed_regs": pushed_regs,
        "mem_accesses": mem_accesses,
        "subcalls": subcalls,
        "syscalls": syscalls,
        "literal_loads": literal_loads,
        "pool_values": pool_values,
        "proposed_cpp_name": proposed_cpp_name,
        "proposed_signature": proposed_signature,
        "mangled_name": mangled_name,
    }


def main():
    ap = argparse.ArgumentParser(
        description="Analyze a 3DS function for matching decompilation (decomp-analysis skill)"
    )
    ap.add_argument("target", help="Function address (e.g. 0x00340E5C), symbol, or identifier")
    ap.add_argument("--size", type=lambda x: int(x, 0), default=None, help="Explicit function size in bytes")
    ap.add_argument("--binary", type=Path, default=DEFAULT_BIN, help="Path to uncompressed 3DS code binary")
    ap.add_argument("--base-vma", type=lambda x: int(x, 0), default=DEFAULT_BASE_VMA, help="Base VMA (default 0x00100000)")
    ap.add_argument("--config-dir", type=Path, default=DEFAULT_CONFIG_DIR, help="Path to config directory")
    ap.add_argument("--thumb", action="store_true", help="Force Thumb mode disassembly")
    ap.add_argument("--json", action="store_true", help="Emit JSON output")
    args = ap.parse_args()

    if not args.binary.exists():
        print(f"❌ Error: Reference binary not found at '{args.binary}'.", file=sys.stderr)
        return 1

    raw_bytes = args.binary.read_bytes()
    mmap = load_memory_map(args.config_dir, len(raw_bytes), args.base_vma)
    functions_by_addr, functions_by_sym, classes_list = load_catalogs(args.config_dir)

    meta = resolve_target(args.target, functions_by_addr, functions_by_sym)
    if not meta:
        print(f"❌ Error: Could not resolve target '{args.target}'.", file=sys.stderr)
        return 1

    addr = meta["address"]
    size = args.size or meta.get("size") or auto_detect_size(raw_bytes, args.base_vma, addr, functions_by_addr)
    meta["size"] = size

    # Disassemble with arm-none-eabi-objdump
    scan_stop = addr + size + 64
    cmd = ["arm-none-eabi-objdump", "-b", "binary", "-m", "arm"]
    if args.thumb or (addr & 1):
        cmd += ["-M", "force-thumb"]
        addr &= ~1
    cmd += [
        "-D",
        f"--adjust-vma={args.base_vma:#x}",
        f"--start-address={addr:#x}",
        f"--stop-address={scan_stop:#x}",
        str(args.binary),
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout

    pool_targets = set()
    branch_targets = set()
    raw_lines = []

    for line in out.splitlines():
        m = LINE_RE.match(line)
        if not m:
            continue
        line_addr = int(m.group(1), 16)
        hexval = m.group(2)
        rest = m.group(3)

        if line_addr < addr + size:
            if re.search(r"ldr[a-z0-9]*\s+[^,]+,\s*\[pc", rest, re.IGNORECASE):
                cm = re.search(r"@\s*(?:0x)?([0-9a-fA-F]+)", rest)
                if cm:
                    t_ref = int(cm.group(1), 16)
                    if addr <= t_ref < addr + size + 512:
                        pool_targets.add(t_ref)

            insn_clean = re.sub(r"\s+@.*$", "", rest).strip()
            bm = BRANCH_RE.match(insn_clean)
            if bm:
                t_branch = int(bm.group(2), 16)
                if addr <= t_branch < addr + size and t_branch != line_addr:
                    branch_targets.add(t_branch)

        raw_lines.append((line_addr, hexval, rest))

    effective_end = addr + size
    if pool_targets:
        effective_end = max(effective_end, max(pool_targets) + 4)
    pool_bytes = effective_end - (addr + size)

    parsed_lines = [(la, hv, rst) for la, hv, rst in raw_lines if la < effective_end]

    # Scan headers and XREFs
    header_matches = scan_headers_for_address(PROJECT_ROOT, addr)
    callers, ptr_refs = find_xrefs(raw_bytes, args.base_vma, mmap["text_end"], addr)

    # Pre-collect literal pool values for hierarchy inference
    prelim_lp = []
    for pt in sorted(pool_targets):
        off = pt - args.base_vma
        if 0 <= off <= len(raw_bytes) - 4:
            val = struct.unpack_from("<I", raw_bytes, off)[0]
            prelim_lp.append({"pool_addr": pt, "value": val})

    hierarchy = infer_hierarchy(
        addr, meta, header_matches, ptr_refs, prelim_lp, functions_by_addr, classes_list
    )
    analysis = analyze_instructions(
        addr,
        size,
        parsed_lines,
        pool_targets,
        branch_targets,
        raw_bytes,
        args.base_vma,
        mmap,
        functions_by_addr,
        hierarchy,
    )

    # Build decomp.me assembly and annotated assembly
    decomp_me_lines = [f"func_{addr:08X}:"]
    annotated_lines = []

    for line_addr, hexval, rest in parsed_lines:
        insn = re.sub(r"\s+@.*$", "", rest).replace("\t", " ").strip()
        note = ""
        if line_addr in pool_targets:
            val = int(hexval, 16)
            sec = classify_vma_section(val, mmap)
            s_lit = read_ascii_string(raw_bytes, args.base_vma, val)
            insn = f".word 0x{hexval.upper()}"
            note = f"  @ {sec}" + (f' ("{s_lit}")' if s_lit else "")
        else:
            bm = BRANCH_RE.match(insn)
            if bm:
                t_branch = int(bm.group(2), 16)
                op = bm.group(1)
                if t_branch in branch_targets:
                    if "cbz" in op or "cbnz" in op:
                        reg_part = insn.split(",")[0].split()[1]
                        insn = f"{op} {reg_part}, .L_{t_branch:08X}"
                    else:
                        insn = f"{op} .L_{t_branch:08X}"
                elif is_call_opcode(op):
                    callee_sym = functions_by_addr.get(t_branch, {}).get("symbol", f"func_{t_branch:08X}")
                    insn = f"{op} func_{t_branch:08X}"
                    if callee_sym != f"func_{t_branch:08X}":
                        note = f"  @ {callee_sym}"
            insn = re.sub(r"nop\s*\{0\}", "nop", insn)

        if line_addr in branch_targets:
            decomp_me_lines.append(f".L_{line_addr:08X}:")
            annotated_lines.append(f"                .L_{line_addr:08X}:")

        decomp_me_lines.append(f"    {insn}")
        annotated_lines.append(f"  +{line_addr - addr:02X} ({line_addr:08X}): {hexval}  {insn}{note}")

    if args.json:
        print(
            json.dumps(
                {
                    "address": f"0x{addr:08X}",
                    "size": size,
                    "pool_bytes": pool_bytes,
                    "status": meta.get("status", "unmatched"),
                    "hierarchy": hierarchy,
                    "analysis": analysis,
                    "header_matches": header_matches,
                    "callers": [f"0x{c:08X}" for c in callers],
                    "pointer_refs": [f"0x{p:08X}" for p in ptr_refs],
                    "decomp_me_asm": "\n".join(decomp_me_lines),
                },
                indent=2,
            )
        )
        return 0

    print("========================================================================")
    print(f"  3DS DECOMP-ANALYSIS REPORT — 0x{addr:08X} ({analysis['proposed_cpp_name']})")
    print("========================================================================")
    print(f"  • Address          : 0x{addr:08X}")
    print(f"  • Size             : {size} bytes code" + (f" (+ {pool_bytes} bytes literal pool)" if pool_bytes > 0 else ""))
    print(f"  • Catalog Symbol   : {meta.get('symbol', f'func_{addr:08X}')} (status: {meta.get('status', 'unmatched')})")
    print(f"  • Namespace        : {hierarchy['namespace']}")
    print(f"  • Layer / Submodule: {hierarchy['submodule_dir']} (layer='{hierarchy['layer']}', subsystem='{hierarchy['subsystem']}')")
    print(f"  • Class / Struct   : {hierarchy['class_name']}")
    print(f"  • Proposed Name    : {analysis['proposed_cpp_name']}")
    print(f"  • Proposed Sig     : {analysis['proposed_signature']}")
    print(f"  • Mangled Symbol   : {analysis['mangled_name']}")
    print(f"  • Target Source    : {hierarchy['src_path']}")
    print(f"  • Target Header    : {hierarchy['header_path']}")
    print("------------------------------------------------------------------------")
    print("  [1] ANNOTATED ASSEMBLY (Offsets & Raw Words)")
    print("------------------------------------------------------------------------")
    for al in annotated_lines:
        print(al)

    print("------------------------------------------------------------------------")
    print("  [2] TARGET ASSEMBLY (Ready for decomp.me)")
    print("------------------------------------------------------------------------")
    for dl in decomp_me_lines:
        print(dl)

    print("------------------------------------------------------------------------")
    print("  [3] SEMANTIC & STRUCTURAL ANALYSIS")
    print("------------------------------------------------------------------------")
    print(f"  • Frame / Leaf     : {'Non-leaf / Stack frame (' + analysis['pushed_regs'] + ')' if analysis['has_stack_frame'] else 'Leaf function (no stack push)'}")
    if analysis["syscalls"]:
        for sid, sname in analysis["syscalls"]:
            print(f"  • Kernel Syscall   : svc 0x{sid:02X} ({sname})")
    if analysis["literal_loads"]:
        print("  • Literal Pool Refs:")
        for lp in analysis["literal_loads"]:
            s_part = f' -> "{lp["string"]}"' if lp["string"] else ""
            print(
                f"      - +0x{lp['insn_addr'] - addr:02X}: loads 0x{lp['value']:08X} into {lp['reg']} (pool @ 0x{lp['pool_addr']:08X}, {lp['section']}){s_part}"
            )
    if analysis["mem_accesses"]:
        print("  • Struct / Memory Offsets:")
        for ma in analysis["mem_accesses"]:
            print(
                f"      - +0x{ma['addr'] - addr:02X}: {ma['op']} ({ma['rw']} {ma['type']}) at [{ma['base']} + 0x{ma['offset']:02X}] (reg {ma['reg']})"
            )
    if analysis["subcalls"]:
        print("  • Subcalls (BL/BLX):")
        for sc in analysis["subcalls"]:
            desc_part = f" — {sc['description']}" if sc["description"] else ""
            print(f"      - +0x{sc['insn_addr'] - addr:02X}: {sc['op']} 0x{sc['target']:08X} ({sc['symbol']}){desc_part}")
    if callers or ptr_refs:
        print("  • Cross-References (XREFs):")
        if callers:
            print(f"      - Direct BL callers ({len(callers)}): {', '.join(f'0x{c:08X}' for c in callers[:8])}")
        if ptr_refs:
            print(
                f"      - Pointer / Vtable refs ({len(ptr_refs)}): "
                + ", ".join(f"0x{p:08X} ({classify_vma_section(p, mmap)})" for p in ptr_refs[:8])
            )
    if header_matches:
        print("  • Existing Repo Mentions:")
        for hm in header_matches:
            print(f"      - {hm['file']}:{hm['line']} -> {hm['text']}")
    print("========================================================================")
    return 0


if __name__ == "__main__":
    sys.exit(main())
