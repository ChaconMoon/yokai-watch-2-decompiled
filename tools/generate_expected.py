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
    raw_bin_path = PROJECT_ROOT / "extracted" / "code.raw.bin"
    raw_bytes = raw_bin_path.read_bytes() if raw_bin_path.exists() else b""

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
            status = row.get("status", "").strip().lower()
            if not sym or not addr or status == "asm_stub":
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
                    # Fallback to byte-exact raw emission
                    raw_off = int(addr, 16) - 0x00100000
                    raw_slice = raw_bytes[raw_off : raw_off + int(row["size"])]
                    byte_lines = ", ".join(f"0x{b:02x}" for b in raw_slice)
                    fallback_s = f""".arm
.section .text, "ax", %progbits
.global {sym}
.type {sym}, %function
{sym}:
    .byte {byte_lines}
.size {sym}, . - {sym}
"""
                    with tempfile.NamedTemporaryFile("w", suffix=".s", delete=False) as tf2:
                        tf2.write(fallback_s)
                        temp_s2 = tf2.name
                    as_res2 = subprocess.run(["arm-none-eabi-as", "-mcpu=mpcore", temp_s2, "-o", str(out_o)], capture_output=True, text=True)
                    Path(temp_s2).unlink(missing_ok=True)
                    if as_res2.returncode == 0:
                        generated += 1
                        print(f"  ✓ Generated (raw bytes): expected/{sym}.o")
                    else:
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
        ],
        "StationConnectionInfo": [
            ("0x00340ECC", "_ZN2nn3nex21StationConnectionInfo5resetEv"),
            ("0x00340EAC", "_ZN2nn3nex21StationConnectionInfo7setPortEt"),
            ("0x00340EB8", "_ZN2nn3nex21StationConnectionInfo10setElementERKNS0_10NexElementE"),
        ],
        "qResult": [
            ("0x0031F1E8", "_ZN2nn3nex7qResultaSERKS1_"),
            ("0x0031F1F4", "_ZN2nn3nex7qResultC1Ev"),
            ("0x0031F204", "_ZN2nn3nex7qResultC1ERKS1_"),
            ("0x0031F210", "_ZNK2nn3nex7qResult8getValueEv"),
        ],
        "applet": [
            ("0x001284E4", "_ZN2nn6applet3CTR13IsApplicationEv"),
            ("0x00128544", "_ZN2nn6applet6detail23SetNotificationCallbackEPvS2_"),
            ("0x00128558", "_ZN2nn6applet6detail10SetState10Ej"),
            ("0x00128568", "_ZN2nn6applet6detail10GetState0CEv"),
            ("0x00128578", "_ZN2nn6applet6detail10SetState0CEh"),
            ("0x00128588", "_ZN2nn6applet6detail16SetSleepCallbackEPvS2_"),
            ("0x0012859C", "_ZN2nn6applet6detail12SetState08_1Ev"),
            ("0x001285B0", "_ZN2nn6applet6detail10GetState08Ev"),
            ("0x001285C0", "_ZN2nn6applet6detail16SetAwakeCallbackEPvS2_"),
            ("0x001285D4", "_ZN2nn6applet6detail12SetState08_0Ev"),
            ("0x001285E8", "_ZN2nn6applet6detail10GetState0BEv"),
            ("0x001285F8", "_ZN2nn6applet6detail10SetState0BEh"),
            ("0x00128608", "_ZN2nn6applet6detail10GetState0DEv"),
            ("0x00128618", "_ZN2nn6applet6detail10SetState0DEa"),
            ("0x00128628", "_ZN2nn6applet6detail12SetState07_1Ev"),
            ("0x0012863C", "_ZN2nn6applet6detail10GetState07Ev"),
            ("0x0012864C", "_ZN2nn6applet6detail12SetState07_0Ev"),
        ],
        "ywCLoopMain": [
            ("0x0010CFF4", "_ZN11ywCLoopMain12getClassTypeEv"),
            ("0x0010CFFC", "_ZN11ywCLoopMain12getClassNameEv"),
        ],
        "ywCLoopRPG": [
            ("0x0010CEE8", "_ZN10ywCLoopRPG12getClassTypeEv"),
            ("0x0010CEF0", "_ZN10ywCLoopRPG12getClassNameEv"),
        ],
        "ywCLoopMenu": [
            ("0x0010D134", "_ZN11ywCLoopMenu12getClassTypeEv"),
            ("0x0010D13C", "_ZN11ywCLoopMenu12getClassNameEv"),
        ],
        "ywCLoopRace": [
            ("0x0010D234", "_ZN11ywCLoopRace12getClassTypeEv"),
            ("0x0010D23C", "_ZN11ywCLoopRace12getClassNameEv"),
        ],
        "ywCLoopEvent": [
            ("0x0010D3A8", "_ZN12ywCLoopEvent12getClassTypeEv"),
            ("0x0010D3B0", "_ZN12ywCLoopEvent12getClassNameEv"),
        ],
        "ywCLoopBattle": [
            ("0x0010D500", "_ZN13ywCLoopBattle12getClassTypeEv"),
            ("0x0010D508", "_ZN13ywCLoopBattle12getClassNameEv"),
        ],
        "ywCLoopCapsule": [
            ("0x0010D63C", "_ZN14ywCLoopCapsule12getClassTypeEv"),
            ("0x0010D644", "_ZN14ywCLoopCapsule12getClassNameEv"),
        ],
        "ywCLoopOrgeTime": [
            ("0x0010DC40", "_ZN15ywCLoopOrgeTime12getClassTypeEv"),
            ("0x0010DC48", "_ZN15ywCLoopOrgeTime12getClassNameEv"),
        ],
        "ywCLoopWatchmap": [
            ("0x0010DD40", "_ZN15ywCLoopWatchmap12getClassTypeEv"),
            ("0x0010DD48", "_ZN15ywCLoopWatchmap12getClassNameEv"),
        ],
        "ywCLoopYokaispot": [
            ("0x0010E35C", "_ZN16ywCLoopYokaispot12getClassTypeEv"),
            ("0x0010E364", "_ZN16ywCLoopYokaispot12getClassNameEv"),
        ],
        "ywCLoopQR": [
            ("0x0010FEBC", "_ZN9ywCLoopQR12getClassTypeEv"),
            ("0x0010FEC4", "_ZN9ywCLoopQR12getClassNameEv"),
        ],
    }

    # Auto-discover any other multi-function TU from compiled objects in build/
    manifest_by_sym = {}
    with open(MANIFEST, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            manifest_by_sym[row["symbol"].strip()] = row["address"].strip()

    build_dir = PROJECT_ROOT / "build" / "src"
    if build_dir.exists():
        for obj_file in build_dir.rglob("*.o"):
            stem = obj_file.stem
            if stem in manifest_by_sym or stem in consolidated_tus:
                continue
            try:
                out = subprocess.check_output(
                    ["arm-none-eabi-readelf", "-s", "-W", str(obj_file)],
                    text=True, stderr=subprocess.PIPE
                )
                discovered = []
                for line in out.splitlines():
                    p = line.split()
                    if len(p) >= 8 and p[3] == "FUNC" and p[6] != "UND":
                        sym = p[7]
                        if sym in manifest_by_sym:
                            discovered.append((manifest_by_sym[sym], sym))
                if discovered:
                    discovered.sort(key=lambda x: int(x[0], 16))
                    consolidated_tus[stem] = discovered
            except Exception:
                pass

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

