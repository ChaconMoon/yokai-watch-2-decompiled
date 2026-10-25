#!/usr/bin/env python3
"""
.agents/skills/decomp-me-context/scripts/decomp_me_helper.py

Prepares everything needed to create or work on a scratch in decomp.me:
  1. Target Assembly (clean disassembly with local labels, literal pool and symbol annotations)
  2. Current Decompiled C/C++ Code (extracted from src/ or scratches/)
  3. Context (clean, self-contained header/declaration block ready to paste into decomp.me's Context tab)
  4. Diff Analysis & Matching Strategy (diff between target and current compiled object, proposed adjustments)
  5. List WIP / Staged functions needing review in decomp.me
"""

import argparse
import csv
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

# Resolve project root
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR
for parent in [SCRIPT_DIR] + list(SCRIPT_DIR.parents):
    if (parent / "Makefile").exists() or (parent / "extracted").exists() or (parent / ".git").exists():
        PROJECT_ROOT = parent
        break

CONFIG_DIR = PROJECT_ROOT / "config"
RAW_BIN = PROJECT_ROOT / "extracted" / "code.raw.bin"
BUILD_DIR = PROJECT_ROOT / "build"
FUNCTIONS_CSV = CONFIG_DIR / "functions.csv"
MEMORY_MAP_JSON = CONFIG_DIR / "memory_map.json"
BASE_VMA = 0x00100000

LINE_RE = re.compile(r"^\s*([0-9a-fA-F]+):\s+([0-9a-fA-F]{4,8})\s+(.*)$")
BRANCH_RE = re.compile(
    r"^(blx?|b(?:eq|ne|cs|hs|cc|lo|mi|pl|vs|vc|hi|ls|ge|lt|gt|le)?|cbz|cbnz)\s+(?:r\d+,\s*)?(?:0x)?([0-9a-fA-F]+)"
)


def load_manifest():
    entries = []
    if not FUNCTIONS_CSV.exists():
        return entries
    with open(FUNCTIONS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row["raw_addr"] = int(row["address"], 0)
                row["raw_size"] = int(row["size"])
                entries.append(row)
            except (ValueError, KeyError):
                continue
    return entries


def get_wip_list():
    manifest = load_manifest()
    wips = [
        row for row in manifest
        if row.get("status", "").lower() in ("wip", "staged", "in_progress", "pending")
    ]
    return wips


def find_source_file_for_function(addr: int, symbol: str):
    """Searches src/ and scratches/ for files containing this function definition or implementation."""
    hex_str = f"{addr:08X}"
    hex_short = f"{addr:06X}"

    # Priority 1: Check for filename directly matching func_00XXXXXX
    for folder in ["src", "scratches"]:
        base = PROJECT_ROOT / folder
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix in (".c", ".cpp"):
                stem = p.stem.lower()
                if hex_str.lower() in stem or hex_short.lower() in stem:
                    return p

    # Priority 2: Look for actual function definition with body '{'
    method_name = symbol
    method_match = re.search(r"(\w+::)?(\w+)\s*\(", symbol)
    if method_match:
        method_name = method_match.group(2)

    search_patterns = [
        re.compile(rf"\bfunc_{hex_str}\s*\([^;]*\)\s*(?:const\s*)?\{{", re.IGNORECASE),
        re.compile(rf"\bfunc_{hex_short}\s*\([^;]*\)\s*(?:const\s*)?\{{", re.IGNORECASE),
        re.compile(rf"\b{re.escape(method_name)}\s*\([^;]*\)\s*(?:const\s*)?\{{"),
        re.compile(rf"//\s*Function\s*0*{hex_short}", re.IGNORECASE),
    ]

    candidate_files = []
    for folder in ["src", "scratches"]:
        base = PROJECT_ROOT / folder
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix in (".c", ".cpp"):
                content = p.read_text(encoding="utf-8", errors="ignore")
                for pat in search_patterns:
                    if pat.search(content):
                        return p
                if symbol in content or hex_str.lower() in content.lower():
                    candidate_files.append(p)

    return candidate_files[0] if candidate_files else None


import textwrap


def strip_cpp_blocks_to_pure_c(text: str) -> str:
    """Evaluates preprocessor conditionals assuming __cplusplus is NOT defined, returning 100% pure C."""
    out_lines = []
    # Stack of (is_cplusplus_branch, keep_current_branch)
    cond_stack = []

    def is_keeping():
        return all(keep for _, keep in cond_stack)

    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^#ifdef\s+__cplusplus\b", stripped) or re.match(r"^#if\s+defined\s*\(\s*__cplusplus\s*\)", stripped):
            cond_stack.append(("cpp", False))
            continue
        elif re.match(r"^#ifndef\s+__cplusplus\b", stripped) or re.match(r"^#if\s+!defined\s*\(\s*__cplusplus\s*\)", stripped):
            cond_stack.append(("cpp", True))
            continue
        elif re.match(r"^#if(?:def|ndef)?\b", stripped):
            cond_stack.append(("other", is_keeping()))
            if is_keeping():
                out_lines.append(line)
            continue
        elif re.match(r"^#else\b", stripped):
            if cond_stack:
                kind, keep = cond_stack[-1]
                if kind == "cpp":
                    cond_stack[-1] = ("cpp", not keep)
                    continue
                else:
                    if all(k for _, k in cond_stack[:-1]):
                        out_lines.append(line)
                    continue
        elif re.match(r"^#endif\b", stripped):
            if cond_stack:
                kind, _ = cond_stack.pop()
                if kind == "cpp":
                    continue
                else:
                    if is_keeping():
                        out_lines.append(line)
                    continue

        if is_keeping():
            out_lines.append(line)

    return "\n".join(out_lines)


def adapt_cpp_function_to_pure_c(code: str, symbol: str) -> str:
    """Converts a C++ member method implementation into an equivalent pure C function ready for decomp.me."""
    if not code:
        return code

    code = textwrap.dedent(code).strip()
    if "::" not in code:
        return code

    lines = code.splitlines()
    sig_idx = None
    for i, line in enumerate(lines):
        if "::" in line and "(" in line and not line.strip().startswith("//"):
            sig_idx = i
            break

    if sig_idx is None:
        return code

    sig_line = lines[sig_idx]
    m = re.match(
        r"^\s*(?P<ret>[\w\s\*&]*?)\b(?P<cls>\w+)::(?P<meth>~?\w+|operator=)\s*\((?P<params>[^)]*)\)\s*(?P<const>const)?(?:\s*:\s*[^{]+)?",
        sig_line,
    )
    if not m:
        return code

    ret_raw = m.group("ret").strip()
    cls_name = m.group("cls").strip()
    meth_name = m.group("meth").strip()
    params_raw = m.group("params").strip()
    is_const = bool(m.group("const"))

    if not ret_raw:
        ret_c = "void" if meth_name.startswith("~") else f"{cls_name} *"
    else:
        ret_c = ret_raw.replace("&", "*").strip()

    self_param = f"const {cls_name} *self" if is_const else f"{cls_name} *self"

    ref_params = []
    c_params = [self_param]
    if params_raw and params_raw != "void":
        for p in params_raw.split(","):
            p_clean = p.strip()
            if "&" in p_clean:
                pm = re.search(r"&\s*(\w+)\s*$", p_clean)
                if pm:
                    ref_params.append(pm.group(1))
                p_clean = p_clean.replace("&", "*")
            c_params.append(p_clean)

    new_sig = f"{ret_c} {symbol}({', '.join(c_params)})"
    # If original sig_line had '{' on the same line, preserve it
    if "{" in sig_line:
        new_sig += " {"
    lines[sig_idx] = new_sig

    body = "\n".join(lines[sig_idx + 1 :])
    body = re.sub(r"\*\s*this\b", "self", body)
    body = re.sub(r"\bthis->", "self->", body)
    body = re.sub(r"\bthis\b", "self", body)

    for rp in ref_params:
        body = re.sub(rf"\b{re.escape(rp)}\.", f"{rp}->", body)
        body = re.sub(rf"=\s*{re.escape(rp)}\s*;", f"= *{rp};", body)

    # Prefix known class member fields with self-> when not already accessed via . or ->
    member_fields = ["m_element", "m_port", "m_data", "unk_00", "unk_01", "unk_02"]
    for mf in member_fields:
        body = re.sub(rf"(?<![\.\w>])\b{mf}\b", f"self->{mf}", body)

    header_lines = lines[: sig_idx + 1]
    return "\n".join(header_lines) + "\n" + body


def extract_function_code_from_file(file_path: Path, symbol: str, addr: int):
    """Extracts only the target function definition from the source file and adapts it to pure C."""
    if not file_path or not file_path.exists():
        return None

    content = file_path.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()

    hex_str = f"{addr:08X}"
    hex_short = f"{addr:06X}"
    method_name = symbol
    method_match = re.search(r"(\w+::)?(\w+)\s*\(", symbol)
    if method_match:
        method_name = method_match.group(2)

    # Patterns indicating definition (must not be a simple call or comparison)
    def_patterns = [
        re.compile(rf"\bfunc_{hex_str}\s*\(", re.IGNORECASE),
        re.compile(rf"\bfunc_{hex_short}\s*\(", re.IGNORECASE),
        re.compile(rf"(?:::|\s|^){re.escape(method_name)}\s*\("),
    ]

    start_line = None
    for i, line in enumerate(lines):
        # Ignore comments or call-like lines if they don't look like definitions
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
            continue

        for pat in def_patterns:
            if pat.search(stripped) and not stripped.endswith(";") and not stripped.startswith("if (") and not stripped.startswith("while ("):
                start_line = i
                # Check backwards for preceding comment header if any
                if i > 0 and lines[i-1].strip().startswith("//"):
                    start_line = i - 1
                break
        if start_line is not None:
            break

    if start_line is None:
        # Fallback: search for comment with address
        for i, line in enumerate(lines):
            if re.search(rf"Function\s*0*{hex_short}", line, re.IGNORECASE):
                start_line = i
                break

    if start_line is None:
        return adapt_cpp_function_to_pure_c(content.strip(), symbol)

    # Find matching brace
    brace_count = 0
    found_open = False
    fn_lines = []

    for idx in range(start_line, len(lines)):
        line = lines[idx]
        fn_lines.append(line)
        if "{" in line:
            brace_count += line.count("{")
            found_open = True
        if "}" in line:
            brace_count -= line.count("}")
        if found_open and brace_count == 0:
            break

    raw_fn = "\n".join(fn_lines)
    return adapt_cpp_function_to_pure_c(raw_fn, symbol)


def build_self_contained_context(target_layer: str, target_subsystem: str, src_file: Path = None, target_header: str = None):
    """Builds a 100% clean, self-contained PURE C context block without header guards, includes, or C++ constructs, ready for decomp.me Context tab."""
    context_parts = []
    included_files = set()

    # 1. Base types header (strip guards, assertions, and C++ blocks)
    types_path = PROJECT_ROOT / "include" / "types.h"
    if types_path.exists():
        types_text = types_path.read_text(encoding="utf-8", errors="ignore")
        types_text = re.sub(r"#ifndef\s+TYPES_H\s*\n#define\s+TYPES_H\s*\n?", "", types_text)
        types_text = re.sub(r"#endif\s+/\*\s*TYPES_H\s*\*/\s*$", "", types_text, flags=re.MULTILINE)
        types_text = re.sub(r"#define\s+STATIC_ASSERT.*", "", types_text)
        types_text = strip_cpp_blocks_to_pure_c(types_text)
        context_parts.append(types_text.strip())
        included_files.add(types_path.resolve())

    # 2. Collect relevant headers:
    headers_to_load = []
    if src_file and src_file.exists():
        src_text = src_file.read_text(encoding="utf-8", errors="ignore")
        for inc_match in re.finditer(r'#include\s+[<"]([^>"]+)[>"]', src_text):
            inc_rel = inc_match.group(1).lstrip("/")
            cand = PROJECT_ROOT / "include" / inc_rel
            if not cand.exists():
                cand = PROJECT_ROOT / inc_rel
            if cand.exists() and cand.is_file() and cand.resolve() not in included_files:
                headers_to_load.append(cand)
                included_files.add(cand.resolve())

    # Also infer subsystem header if not already added
    subsys_map = {
        "nex": PROJECT_ROOT / "include" / "ctr" / "nex.h",
        "os": PROJECT_ROOT / "include" / "ctr" / "os.h",
        "svc": PROJECT_ROOT / "include" / "ctr" / "svc.h",
        "y2r": PROJECT_ROOT / "include" / "ctr" / "y2r.h",
        "dsp": PROJECT_ROOT / "include" / "ctr" / "dsp.h",
        "ndm": PROJECT_ROOT / "include" / "ctr" / "ndm.h",
        "lfw": PROJECT_ROOT / "include" / "engine" / "lfw.h",
        "lxp": PROJECT_ROOT / "include" / "engine" / "lxp.h",
        "core": PROJECT_ROOT / "include" / "engine" / "core.h" if target_layer == "engine" else PROJECT_ROOT / "include" / "game" / "core.h",
        "loops": PROJECT_ROOT / "include" / "game" / "loops.h",
    }
    for key, path in subsys_map.items():
        if key in target_subsystem and path.exists() and path.resolve() not in included_files:
            headers_to_load.append(path)
            included_files.add(path.resolve())

    # 3. Read, strip includes/guards, and evaluate in pure C mode
    for h in headers_to_load:
        h_text = h.read_text(encoding="utf-8", errors="ignore")
        h_text = re.sub(r'#include\s+[<"][^>"]+[>"]\s*\n?', '', h_text)
        h_text = re.sub(r'#ifndef\s+[A-Za-z0-9_]+\s*\n#define\s+[A-Za-z0-9_]+\s*\n?', '', h_text)
        h_text = re.sub(r'#endif\s+/\*\s*[A-Za-z0-9_]+\s*\*/\s*$', '', h_text, flags=re.MULTILINE)
        h_text = strip_cpp_blocks_to_pure_c(h_text)
        context_parts.append(h_text.strip())

    raw_context = "\n\n".join(context_parts)
    cleaned_context = re.sub(r'\n{3,}', '\n\n', raw_context)
    return cleaned_context.strip()


def dump_target_assembly(addr: int, size: int, symbol_name: str):
    """Runs objdump on code.raw.bin and formats clean target assembly ready for decomp.me."""
    scan_stop = addr + size + 64
    cmd = [
        "arm-none-eabi-objdump", "-b", "binary", "-m", "arm",
        "-D", f"--adjust-vma={BASE_VMA:#x}",
        f"--start-address={addr:#x}",
        f"--stop-address={scan_stop:#x}",
        str(RAW_BIN)
    ]
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.PIPE)
    except Exception as e:
        return f"; Error reading assembly: {e}"

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

    parsed_lines = [(la, hv, rst) for la, hv, rst in raw_lines if la < effective_end]

    asm_lines = [f"{symbol_name}:"]
    for line_addr, hexval, rest in parsed_lines:
        insn = re.sub(r"\s+@.*$", "", rest).replace("\t", " ").strip()
        if line_addr in pool_targets:
            insn = f".word 0x{hexval.upper()}"
        else:
            bm = BRANCH_RE.match(insn)
            if bm:
                t_branch = int(bm.group(2), 16)
                op = bm.group(1)
                if t_branch in branch_targets:
                    insn = f"{op} .L_{t_branch:08X}"
                elif op in ("bl", "blx"):
                    insn = f"{op} func_{t_branch:08X}"

        if line_addr in branch_targets:
            asm_lines.append(f".L_{line_addr:08X}:")
        asm_lines.append(f"    {insn}")

    return "\n".join(asm_lines)


def get_compiled_assembly_and_diff(obj_path: Path, symbol: str, addr: int, size: int):
    """Disassembles the current compiled object and notes byte diffs against raw binary."""
    if not obj_path or not obj_path.exists():
        return None, "No compiled object found in build/. Run 'make' first."

    cmd = ["arm-none-eabi-objdump", "-d", "-r", str(obj_path)]
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.PIPE)
    except Exception as e:
        return None, str(e)

    # Read expected raw slice
    with open(RAW_BIN, "rb") as f:
        raw_data = f.read()

    raw_offset = addr - BASE_VMA
    expected_slice = raw_data[raw_offset : raw_offset + size]

    # Find function in objdump
    compiled_lines = []
    in_fn = False
    for line in out.splitlines():
        if f"<{symbol}>:" in line or (f": <" in line and f"{addr:08x}" in line.lower()):
            in_fn = True
            compiled_lines.append(line)
            continue
        if in_fn:
            if line.strip() == "" or (re.match(r"^[0-9a-fA-F]+ <", line) and not line.startswith(" ")):
                break
            compiled_lines.append(line)

    return "\n".join(compiled_lines), None


def generate_wip_recommendations(addr: int, symbol: str, size: int, raw_asm: str, compiled_asm: str):
    """Analyzes differences and suggests concrete compiler flags and C/C++ syntactic changes."""
    suggestions = []

    # 1. Regalloc and early exit analysis
    if "popcs" in compiled_asm or "popne" in compiled_asm or "poplt" in compiled_asm:
        if "bcs" in raw_asm or "bmi" in raw_asm:
            suggestions.append(
                "• **Unificación de epílogo / Retorno único:** En lugar de múltiples `return`, usa una sola variable `result` y deja que el flujo salte al final. El binario original salta con `bcs`/`bmi` a un único `pop {..., pc}`."
            )

    if "ands" in raw_asm and "tst" in compiled_asm:
        suggestions.append(
            "• **Instrucción `ands` vs `tst`:** El original usa `ands r1, r0, #-2147483648` (conserva el resultado de la máscara en un registro). Prueba asignar el resultado o evaluar una macro tipo `if ((res & 0x80000000) != 0)` guardándolo en variable."
        )

    if "rev16" in raw_asm and "uxth" in compiled_asm:
        suggestions.append(
            "• **Byte swap de 16 bits sin extensión:** Usa el modismo big-endian directo: `(u16)((b[0] << 8) | b[1])`. ARMCC lo compila directamente a `ldrh` + `rev16` sin la instrucción redundante `uxth`."
        )

    if "orr" in raw_asm and ("subs" in raw_asm or "sbcs" in raw_asm):
        suggestions.append(
            "• **Comparación de 64 bits (`s64`):** El original evalúa `func_0063A6E8(&elem)` empaquetado en 64 bits. Prueba comparar directamente el entero `s64` o usar una `union` con dos campos de 32 bits."
        )

    # Compiler flag recommendations
    suggestions.append(
        "• **Banderas de compilación recomendadas para decomp.me:**\n"
        "  - Compilador: `ARM C/C++ (RVCT 4.0 build 821)` o `ARM11 GCC (fallback)`\n"
        "  - Banderas base: `--cpu=mpcore -O3 --gnu -c` (para C++) o `-c -mcpu=mpcore -O3` (GCC)\n"
        "  - Variantes a probar si hay diferencias de regalloc: `-Otime` vs `-Ospace` (o `-O2`)"
    )

    return "\n".join(suggestions)


def main():
    ap = argparse.ArgumentParser(description="decomp.me Context & Scratch Preparation Helper")
    ap.add_argument("target", nargs="?", default=None, help="Virtual address (e.g. 0x00340E5C) or 'list'")
    ap.add_argument("--json", action="store_true", help="Output result as JSON")
    args = ap.parse_args()

    # Mode 1: List WIP / Staged functions
    if args.target is None or args.target.lower() == "list":
        wips = get_wip_list()
        if args.json:
            print(json.dumps(wips, indent=2))
            return 0

        print("================================================================================")
        print("  Yo-kai Watch 2 (3DS) — Funciones WIP / Staged para decomp.me")
        print("================================================================================")
        print(f"  Total de funciones pendientes de matching exacto: {len(wips)}\n")
        print(f"  {'DIRECCIÓN':<12} {'TAMAÑO':<8} {'CAPA / SUB':<18} {'SÍMBOLO / DESCRIPCIÓN'}")
        print("  " + "-" * 76)
        for w in wips:
            addr = w["address"]
            size = f"{w['size']} B"
            layer_sub = f"{w['layer']}/{w['subsystem']}"
            desc = w.get("description", w["symbol"])
            print(f"  {addr:<12} {size:<8} {layer_sub:<18} {desc}")
        print("================================================================================")
        print("  Uso: python3 .agents/skills/decomp-me-context/scripts/decomp_me_helper.py <0xADDRESS>")
        print("================================================================================")
        return 0

    # Mode 2: Generate full package for target function
    manifest = load_manifest()
    clean_target = args.target.strip()
    target_row = None

    # Find in manifest
    m_hex = re.match(r"^(?:0x)?([0-9a-fA-F]{6,8})$", clean_target)
    if m_hex:
        target_addr = int(m_hex.group(1), 16)
        for row in manifest:
            if row.get("raw_addr") == target_addr:
                target_row = row
                break
    else:
        for row in manifest:
            if clean_target.lower() in row.get("symbol", "").lower():
                target_row = row
                break

    if not target_row:
        if m_hex:
            target_addr = int(m_hex.group(1), 16)
            target_row = {
                "address": f"0x{target_addr:08X}",
                "raw_addr": target_addr,
                "symbol": f"func_{target_addr:08X}",
                "size": 32,
                "layer": "ctr",
                "subsystem": "nn_nex",
                "status": "staged",
                "description": f"Function 0x{target_addr:08X}"
            }
        else:
            print(f"❌ Error: Función '{clean_target}' no encontrada en el catálogo.", file=sys.stderr)
            return 1

    addr = target_row["raw_addr"]
    size = int(target_row["size"])
    symbol = target_row["symbol"]
    layer = target_row.get("layer", "ctr")
    subsys = target_row.get("subsystem", "nn_nex")
    status = target_row.get("status", "staged")

    # 1. Target Assembly
    target_asm = dump_target_assembly(addr, size, symbol)

    # 2. Source file & Current Code
    src_file = find_source_file_for_function(addr, symbol)
    current_code = extract_function_code_from_file(src_file, symbol, addr) if src_file else None

    # 3. Standalone Context (100% clean, no #include, ready to copy-paste into decomp.me)
    context_code = build_self_contained_context(layer, subsys, src_file)

    # 4. Compiled assembly and suggestions
    compiled_asm = ""
    compiled_obj = None
    if src_file:
        # Check expected build object path
        rel_src = src_file.relative_to(PROJECT_ROOT)
        obj_candidate = BUILD_DIR / rel_src.with_suffix(".o")
        if obj_candidate.exists():
            compiled_obj = obj_candidate
            compiled_asm, _ = get_compiled_assembly_and_diff(compiled_obj, symbol, addr, size)

    recommendations = generate_wip_recommendations(addr, symbol, size, target_asm, compiled_asm or "")

    if args.json:
        print(json.dumps({
            "address": f"0x{addr:08X}",
            "symbol": symbol,
            "size": size,
            "status": status,
            "source_file": str(src_file.relative_to(PROJECT_ROOT)) if src_file else None,
            "target_assembly": target_asm,
            "current_code": current_code,
            "context": context_code,
            "recommendations": recommendations
        }, indent=2))
        return 0

    print("================================================================================")
    print(f"  PAQUETE DECOMP.ME — 0x{addr:08X} ({symbol})")
    print("================================================================================")
    print(f"  • Dirección       : 0x{addr:08X} ({size} bytes)")
    print(f"  • Estado actual   : {status.upper()}")
    print(f"  • Archivo fuente  : {src_file.relative_to(PROJECT_ROOT) if src_file else '(no encontrado)'}")
    print("--------------------------------------------------------------------------------")
    print("  [1] TARGET ASSEMBLY (Copiar y pegar en pestaña 'Target Assembly' de decomp.me)")
    print("--------------------------------------------------------------------------------")
    print(target_asm)
    print("\n--------------------------------------------------------------------------------")
    print("  [2] CÓDIGO ACTUAL (Tu implementación actual en el repositorio)")
    print("--------------------------------------------------------------------------------")
    if current_code:
        print(current_code)
    else:
        print("  // No se encontró implementación en src/. Empezar desde stub vacío.")
    print("\n--------------------------------------------------------------------------------")
    print("  [3] ESTRATEGIA Y CAMBIOS RECOMENDADOS PARA LLEGAR AL MATCH")
    print("--------------------------------------------------------------------------------")
    print(recommendations)
    print("\n--------------------------------------------------------------------------------")
    print("  [4] CONTEXTO COMPLETO (Copiar y pegar en pestaña 'Context' de decomp.me)")
    print("--------------------------------------------------------------------------------")
    print(context_code)
    print("================================================================================")
    return 0


if __name__ == "__main__":
    sys.exit(main())
