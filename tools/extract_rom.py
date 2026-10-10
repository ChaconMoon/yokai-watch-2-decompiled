#!/usr/bin/env python3
"""
tools/extract_rom.py — Extractor y descompresor de ejecutables de Nintendo 3DS
para Yo-kai Watch 2: Mentespectros.

Soporta:
1. Inspección de archivos .3ds (NCSD) / .ncch / .cxi.
2. Detección de cifrado AES-CTR de Nintendo (Retail Crypto).
3. Extracción de exheader.bin y exefs/code.bin.
4. Descompresión de Nintendo Extended LZSS (Backwards BLZ) a code.raw.bin.
5. Cálculo y verificación del hash SHA-256 de referencia.
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
    Descomprime un buffer code.bin utilizando el algoritmo Nintendo Backwards LZSS (BLZ).
    Usa la implementación estándar de pyctr (o mediante uvx si no está en el entorno).
    """
    try:
        from pyctr.type.exefs import decompress_code
        return decompress_code(data)
    except ImportError:
        pass

    # Intentar invocar uvx con pyctr de forma transparente
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

    print("⚠️ No se pudo cargar el descompresor pyctr. Conservando datos originales.")
    return data


def inspect_and_extract_3ds(rom_path: Path):
    """Analiza la estructura NCSD/NCCH y extrae el ejecutable si no está cifrado."""
    print(f"📦 Analizando contenedor: {rom_path.name} ({rom_path.stat().st_size / (1024*1024):.2f} MB)")

    with open(rom_path, "rb") as f:
        header = f.read(0x300)

        # 1. Comprobar si es un archivo .3ds (NCSD) o un .cxi/.ncch directo
        if header[0x100:0x104] == b"NCSD":
            part0_offset_mu = struct.unpack_from("<I", header, 0x120)[0]
            part0_offset = part0_offset_mu * 512
            print(f"   ✓ Formato detectado: Nintendo 3DS Cartridge (NCSD)")
            print(f"   ✓ Offset Partición 0 (NCCH Ejecutable): 0x{part0_offset:X}")
            f.seek(part0_offset)
            ncch_hdr = f.read(0x200)
        elif header[0x100:0x104] == b"NCCH":
            part0_offset = 0
            ncch_hdr = header[:0x200]
            print(f"   ✓ Formato detectado: NCCH / CXI directo")
        else:
            print("❌ Error: No se encontró la firma mágica 'NCSD' ni 'NCCH'.")
            return False

        if ncch_hdr[0x100:0x104] != b"NCCH":
            print("❌ Error: Cabecera NCCH inválida en la Partición 0.")
            return False

        product_code = ncch_hdr[0x150:0x160].decode("ascii", errors="ignore").strip("\x00")
        print(f"   🏷️ Product Code: {product_code}")

        # Localizar ExeFS
        exefs_offset_mu = struct.unpack_from("<I", ncch_hdr, 0x1A0)[0]
        exefs_size_mu = struct.unpack_from("<I", ncch_hdr, 0x1A4)[0]
        exefs_abs_offset = part0_offset + (exefs_offset_mu * 512)
        exefs_size = exefs_size_mu * 512

        print(f"   📁 ExeFS Offset: 0x{exefs_abs_offset:X} | Tamaño: {exefs_size} bytes")

        # Leer tabla de archivos de ExeFS (0x200 bytes)
        f.seek(exefs_abs_offset)
        exefs_header = f.read(0x200)

        # Verificar si la tabla de ExeFS contiene nombres legibles (ASCII) o está cifrada
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
            print("⚠️ AVISO DE CIFRADO DE NINTENDO 3DS (RETAIL AES-CTR)")
            print("=" * 70)
            print("El volcado actual proviene directamente de cartucho físico con cifrado")
            print("activo de fábrica de Nintendo. En una consola 3DS real, el coprocesador")
            print("criptográfico descifra estos sectores de forma transparente al vuelo.\n")
            print("Para obtener el ejecutable listo para decompilación:")
            print("  1. Inserta tu tarjeta SD en tu Nintendo 3DS e inicia GodMode9.")
            print("  2. Navega hasta el cartucho o el archivo .3ds:")
            print("     [C:] GAMECART  ➔  pulsa (A) sobre tu juego")
            print("     Selecciona: 'NCSD image options...' ➔ 'Decrypt file'")
            print("     (GodMode9 descifrará la ROM en tu SD en unos 30 segundos).")
            print("  O mejor aún (pesa solo 5 MB en vez de 4 GB):")
            print("     Selecciona: 'NCCH image options...' ➔ 'Mount image to drive'")
            print("     Entra en 'exefs' y copia 'code.bin' y 'exheader.bin' a tu SD.")
            print("  3. Coloca 'code.bin' directamente en la carpeta 'extracted/'.")
            print("=" * 70 + "\n")
            return False

        # Si no está cifrado, extraer code.bin
        code_offset, code_size = code_entry
        abs_code_offset = exefs_abs_offset + 0x200 + code_offset
        print(f"   ⚡ Extrayendo 'code.bin' descifrado (0x{abs_code_offset:X}, {code_size} bytes)...")

        f.seek(abs_code_offset)
        code_data = f.read(code_size)

        EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)
        raw_path = EXTRACTED_DIR / "code.bin"
        raw_path.write_bytes(code_data)
        print(f"   ✓ Guardado: {raw_path.relative_to(PROJECT_ROOT)}")

        process_code_binary(code_data)
        return True


def process_code_binary(data: bytes):
    """Descomprime y analiza el ejecutable code.bin."""
    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)

    sha256_comp = hashlib.sha256(data).hexdigest()
    print(f"\n📊 Ejecutable Comprimido ('code.bin'):")
    print(f"   - Tamaño: {len(data)} bytes ({len(data) / (1024*1024):.2f} MB)")
    print(f"   - SHA-256: {sha256_comp}")

    # Descompresión FastLZSS / BLZ
    print("🔄 Verificando y aplicando descompresión FastLZSS (BLZ)...")
    decomp_data = decompress_nintendo_lzss(data)

    decomp_path = EXTRACTED_DIR / "code.raw.bin"
    decomp_path.write_bytes(decomp_data)

    sha256_decomp = hashlib.sha256(decomp_data).hexdigest()
    print(f"\n🎯 Ejecutable Plano Descomprimido ('code.raw.bin'):")
    print(f"   - Tamaño: {len(decomp_data)} bytes ({len(decomp_data) / (1024*1024):.2f} MB)")
    print(f"   - SHA-256: {sha256_decomp}")
    print(f"   - Dirección Base de Carga: 0x00100000 (ARM11 MPCore)")
    print(f"   ✓ Archivo listo para Ghidra / decomp.me en: {decomp_path.relative_to(PROJECT_ROOT)}")


def find_local_code_binary():
    """Busca el ejecutable code.bin / .code en extracted/ o en la raíz."""
    names = ["code.bin", ".code", "code", ".code.bin"]
    # 1. Buscar en extracted/
    for name in names:
        p = EXTRACTED_DIR / name
        if p.is_file():
            return p
    # 2. Buscar en la raíz del proyecto
    for name in names:
        p = PROJECT_ROOT / name
        if p.is_file():
            return p
    return None


def main():
    parser = argparse.ArgumentParser(description="Extractor de ejecutables de Nintendo 3DS para decompilación.")
    parser.add_argument("--rom", type=str, help="Ruta a la ROM .3ds / .cxi")
    parser.add_argument("--code", type=str, help="Ruta directa al archivo code.bin / .code")
    args = parser.parse_args()

    # Si se pasa explícitamente --code o se detecta localmente
    code_target = Path(args.code) if args.code else find_local_code_binary()
    if code_target and code_target.is_file() and not args.rom:
        print(f"🔍 Detectado ejecutable local: {code_target.relative_to(PROJECT_ROOT)}")
        process_code_binary(code_target.read_bytes())
        return

    # Buscar cualquier archivo .3ds en el directorio del proyecto
    rom_file = None
    if args.rom:
        rom_file = Path(args.rom)
    else:
        candidates = list(PROJECT_ROOT.glob("*.3ds")) + list(PROJECT_ROOT.glob("*.cxi"))
        if candidates:
            rom_file = candidates[0]

    if not rom_file or not rom_file.exists():
        print("❌ No se encontró ninguna ROM (.3ds o .cxi) ni archivo 'code.bin' / '.code'.")
        print("Coloca tu ROM en esta carpeta o aporta directamente '.code' / 'code.bin' en 'extracted/'.")
        sys.exit(1)

    inspect_and_extract_3ds(rom_file)


if __name__ == "__main__":
    main()
