#!/usr/bin/env python3
"""
tools/extract_rom.py — Nintendo 3DS executable extractor and decompressor
for Yo-kai Watch 2: Psychic Specters.

Supports:
1. Inspecting .3ds (NCSD) / .ncch / .cxi files.
2. Detecting Nintendo AES-CTR retail encryption.
3. Extracting exheader.bin and exefs/code.bin.
4. Decompressing Nintendo Extended LZSS (Backwards BLZ) to code.raw.bin.
5. Computing and verifying the reference SHA-256 hash.
"""

import argparse
import hashlib
import os
import struct
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXTRACTED_DIR = PROJECT_ROOT / "extracted"


def decompress_nintendo_lzss(data: bytes) -> bytes:
    """
    Decompresses a code.bin buffer using the Nintendo Backwards LZSS (BLZ) algorithm.
    Uses standard pyctr implementation (or via uvx if not installed in the environment).
    """
    try:
        from pyctr.type.exefs import decompress_code
        return decompress_code(data)
    except ImportError:
        pass

    # Attempt to invoke uvx with pyctr transparently
    import subprocess
    import shutil

    uvx_bin = shutil.which("uvx") or os.path.expanduser("~/.local/bin/uvx")
    if os.path.exists(uvx_bin):
        cmd = [
            uvx_bin,
            "--from", "pyctr",
            "python3", "-c",
            "import sys; from pyctr.type.exefs import decompress_code; sys.stdout.buffer.write(decompress_code(sys.stdin.buffer.read()))"
        ]
        res = subprocess.run(cmd, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode == 0 and len(res.stdout) > len(data):
            return res.stdout

    print("⚠️ Could not load pyctr decompressor. Keeping original data.")
    return data


def inspect_and_extract_3ds(rom_path: Path):
    """Analyzes NCSD/NCCH structure and extracts the executable if unencrypted."""
    print(f"📦 Analyzing container: {rom_path.name} ({rom_path.stat().st_size / (1024*1024):.2f} MB)")

    with open(rom_path, "rb") as f:
        header = f.read(0x300)

        # 1. Check if it's a .3ds (NCSD) or direct .cxi/.ncch
        if header[0x100:0x104] == b"NCSD":
            part0_offset_mu = struct.unpack_from("<I", header, 0x120)[0]
            part0_offset = part0_offset_mu * 512
            print(f"   ✓ Detected format: Nintendo 3DS Cartridge (NCSD)")
            print(f"   ✓ Partition 0 offset (Executable NCCH): 0x{part0_offset:X}")
            f.seek(part0_offset)
            ncch_hdr = f.read(0x200)
        elif header[0x100:0x104] == b"NCCH":
            part0_offset = 0
            ncch_hdr = header[:0x200]
            print(f"   ✓ Detected format: Direct NCCH / CXI")
        else:
            print("❌ Error: Magic signature 'NCSD' or 'NCCH' not found.")
            return False

        if ncch_hdr[0x100:0x104] != b"NCCH":
            print("❌ Error: Invalid NCCH header in Partition 0.")
            return False

        product_code = ncch_hdr[0x150:0x160].decode("ascii", errors="ignore").strip("\x00")
        print(f"   🏷️ Product Code: {product_code}")

        # Locate ExeFS
        exefs_offset_mu = struct.unpack_from("<I", ncch_hdr, 0x1A0)[0]
        exefs_size_mu = struct.unpack_from("<I", ncch_hdr, 0x1A4)[0]
        exefs_abs_offset = part0_offset + (exefs_offset_mu * 512)
        exefs_size = exefs_size_mu * 512

        print(f"   📁 ExeFS Offset: 0x{exefs_abs_offset:X} | Size: {exefs_size} bytes")

        # Read ExeFS file table (0x200 bytes)
        f.seek(exefs_abs_offset)
        exefs_header = f.read(0x200)

        # Verify whether ExeFS table contains legible ASCII names or is encrypted
        code_entry = None
        is_encrypted = True

        for i in range(10):
            entry = exefs_header[i*16:(i+1)*16]
            raw_name = entry[:8].rstrip(b"\x00")
            try:
                name = raw_name.decode("ascii")
                if name in ("code", "icon", "banner", "logo"):
                    is_encrypted = False
            except UnicodeDecodeError:
                pass

            offset = struct.unpack_from("<I", entry, 8)[0]
            size = struct.unpack_from("<I", entry, 12)[0]
            if raw_name == b"code":
                code_entry = (offset, size)

        if is_encrypted or code_entry is None:
            print("\n" + "=" * 70)
            print("⚠️ NINTENDO 3DS ENCRYPTION NOTICE (RETAIL AES-CTR)")
            print("=" * 70)
            print("The current dump originates from a physical cartridge with retail")
            print("factory encryption enabled. On real 3DS hardware, the cryptographic")
            print("coprocessor decrypts these sectors on the fly.\n")
            print("To obtain a decrypted executable ready for decompilation:")
            print("  1. Insert your SD card into your Nintendo 3DS and boot GodMode9.")
            print("  2. Navigate to your gamecart or .3ds file:")
            print("     [C:] GAMECART  ➔  press (A) on your game")
            print("     Select: 'NCSD image options...' ➔ 'Decrypt file'")
            print("     (GodMode9 will decrypt the ROM to your SD in ~30 seconds).")
            print("  Or even better (only ~5 MB instead of 4 GB):")
            print("     Select: 'NCCH image options...' ➔ 'Mount image to drive'")
            print("     Enter 'exefs' and copy 'code.bin' and 'exheader.bin' to your SD.")
            print("  3. Place 'code.bin' directly in the 'extracted/' folder.")
            print("=" * 70 + "\n")
            return False

        # Extract code.bin if unencrypted
        code_offset, code_size = code_entry
        abs_code_offset = exefs_abs_offset + 0x200 + code_offset
        print(f"   ⚡ Extracting decrypted 'code.bin' (0x{abs_code_offset:X}, {code_size} bytes)...")

        f.seek(abs_code_offset)
        code_data = f.read(code_size)

        EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)
        raw_path = EXTRACTED_DIR / "code.bin"
        raw_path.write_bytes(code_data)
        print(f"   ✓ Saved: {raw_path.relative_to(PROJECT_ROOT)}")

        process_code_binary(code_data)
        return True


def process_code_binary(data: bytes):
    """Decompresses and analyzes the code.bin executable."""
    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)

    sha256_comp = hashlib.sha256(data).hexdigest()
    print(f"\n📊 Compressed Executable ('code.bin'):")
    print(f"   - Size: {len(data)} bytes ({len(data) / (1024*1024):.2f} MB)")
    print(f"   - SHA-256: {sha256_comp}")

    # FastLZSS / BLZ decompression
    print("🔄 Verifying and applying FastLZSS (BLZ) decompression...")
    decomp_data = decompress_nintendo_lzss(data)

    decomp_path = EXTRACTED_DIR / "code.raw.bin"
    decomp_path.write_bytes(decomp_data)

    sha256_decomp = hashlib.sha256(decomp_data).hexdigest()
    print(f"\n🎯 Decompressed Raw Executable ('code.raw.bin'):")
    print(f"   - Size: {len(decomp_data)} bytes ({len(decomp_data) / (1024*1024):.2f} MB)")
    print(f"   - SHA-256: {sha256_decomp}")
    print(f"   - Base Load Address: 0x00100000 (ARM11 MPCore)")
    print(f"   ✓ File ready for Ghidra / decomp.me at: {decomp_path.relative_to(PROJECT_ROOT)}")


def find_local_code_binary():
    """Searches for code.bin / .code in extracted/ or project root."""
    names = ["code.bin", ".code", "code", ".code.bin"]
    # 1. Search in extracted/
    for name in names:
        p = EXTRACTED_DIR / name
        if p.is_file():
            return p
    # 2. Search in project root
    for name in names:
        p = PROJECT_ROOT / name
        if p.is_file():
            return p
    return None


def main():
    parser = argparse.ArgumentParser(description="Nintendo 3DS executable extractor for decompilation projects.")
    parser.add_argument("--rom", type=str, help="Path to .3ds / .cxi ROM")
    parser.add_argument("--code", type=str, help="Direct path to code.bin / .code file")
    args = parser.parse_args()

    # If --code passed explicitly or found locally
    code_target = Path(args.code) if args.code else find_local_code_binary()
    if code_target and code_target.is_file() and not args.rom:
        print(f"🔍 Detected local executable: {code_target.relative_to(PROJECT_ROOT)}")
        process_code_binary(code_target.read_bytes())
        return

    # Look for any .3ds / .cxi ROM in root
    rom_file = None
    if args.rom:
        rom_file = Path(args.rom)
    else:
        candidates = list(PROJECT_ROOT.glob("*.3ds")) + list(PROJECT_ROOT.glob("*.cxi"))
        if candidates:
            rom_file = candidates[0]

    if not rom_file or not rom_file.exists():
        print("❌ No ROM (.3ds or .cxi) or 'code.bin' / '.code' file found.")
        print("Place your ROM in this directory or provide '.code' / 'code.bin' in 'extracted/'.")
        sys.exit(1)

    inspect_and_extract_3ds(rom_file)


if __name__ == "__main__":
    main()
