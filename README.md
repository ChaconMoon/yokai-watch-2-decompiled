# Yo-kai Watch 2: Mentespectros (Nintendo 3DS) — Matching Decompilation

<p align="center">
  <img src="https://raw.githubusercontent.com/ChaconMoon/Decompilation-in-358-2/master/docs/diario/diario-images/day-12.png" alt="Yo-kai Watch 2 Decompilation" width="85%">
</p>

<p align="center">
  <strong>Decompilación matching byte-exact en C/C++ del motor de videojuego de Level-5 para Nintendo 3DS (CTR).</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Plataforma-Nintendo%203DS%20(CTR)-e11d48?style=for-the-badge" alt="Nintendo 3DS">
  <img src="https://img.shields.io/badge/CPU-ARM11%20MPCore%20%40%20268%20MHz%20(ARMv6K)-0284c7?style=for-the-badge" alt="ARM11">
  <img src="https://img.shields.io/badge/Compilador%20Original-RVCT%20%2F%20armcc-f59e0b?style=for-the-badge" alt="RVCT">
  <a href="https://github.com/ChaconMoon/Decompilation-in-358-2"><img src="https://img.shields.io/badge/Reto-%23DecompilandoEn358Dias-7c3aed?style=for-the-badge" alt="Reto"></a>
  <img src="https://img.shields.io/badge/Licencia-MIT-10b981?style=for-the-badge" alt="Licencia">
</p>

---

## 🎮 Información del Título

* **Juego**: *Yo-kai Watch 2: Mentespectros* (*Shin'uchi* / *Psychic Specters*)
* **Desarrollador**: Level-5
* **Publisher**: Nintendo / Level-5
* **Plataforma**: Nintendo 3DS (CTR)
* **Title ID**: `00040000001B2900` (Edición Europea / Multi-idioma)
* **Arquitectura de CPU Principal**: **ARM11 MPCore (ARMv6K)** de doble núcleo @ 268 MHz (32-bit Little Endian)
* **Coprocesador**: ARM946E-S (Seguridad y acceso a I/O del sistema operativo Horizon)
* **Convención de Llamadas**: **AAPCS (ARM Architecture Procedure Call Standard)** (`r0`-`r3` para argumentos, `r0` para retorno, `r4`-`r11` callee-saved, `sp`, `lr`, `pc`).
* **Compilador Original**: ARM Compiler (RVCT / `armcc`), verificado mediante las firmas de biblioteca Rogue Wave Standard Library (`RWSTDERR`).

---

## 🔬 Objetivos del Proyecto

Este repositorio persigue la ingeniería inversa y decompilación **100% matching byte-exact** del código ejecutable del juego:
1. Reconstruir el código fuente legible en C/C++ idéntico en bytes al código compilado por Level-5.
2. Mapear y tipar las estructuras internas del motor de combate, tablas de parámetros de Yo-kai, animaciones e inventario.
3. Servir como submódulo activo de la **Fase 2** del reto formativo de 358,5 días [[#DecompilandoEn358Dias](https://github.com/ChaconMoon/Decompilation-in-358-2)].
4. Publicar scratches verificados en [decomp.me](https://decomp.me/) y [decomp.dev](https://decomp.dev/).

---

## 📂 Estructura del Repositorio

```text
yokai-watch-2-decompiled/
├── Makefile              # Orquestador de compilación, extracción y verificación
├── .gitignore            # Protección estricta contra subida de ROMs con copyright
├── README.md             # Documentación técnica del proyecto
├── config/               # Configuración de memoria, linker scripts y símbolos
│   └── symbols.txt       # Tabla de símbolos conocidos y direcciones de funciones
├── tools/                # Scripts de soporte y herramientas de ingeniería inversa
│   └── extract_rom.py    # Extractor de NCSD/NCCH, ExeFS y descompresor FastLZSS
├── asm/                  # Ensamblador de funciones pendientes de decompilar (.s)
├── src/                  # Código fuente en C/C++ decompilado 100% matching
├── include/              # Tipos base de CTR-SDK y estructuras del motor de Level-5
├── scratches/            # Registro de scratches creados en decomp.me
└── extracted/            # [Ignorado en Git] Binarios extraídos de la ROM legal
    ├── exheader.bin      # Extended Header de la aplicación CTR
    ├── code.bin          # Ejecutable comprimido de ExeFS (4.42 MB)
    └── code.raw.bin      # Ejecutable plano descomprimido ARM11 @ 0x00100000 (7.38 MB)
```

---

## 🚀 Pipeline de Extracción y Preparación

### 1. Requisitos
* Python 3.10+
* Herramientas estándar de Unix (`make`, `sha256sum`)
* Una copia legítima del juego dumpeada en formato `.3ds` o `.cia` desde una consola Nintendo 3DS personal con **GodMode9**.

### 2. Extracción de Binarios
Coloca tu archivo dumpeado en la raíz de este repositorio con el nombre del Title ID:
```bash
# Nombre esperado: 00040000001B2900_v00.3ds
make extract
```

El script [`tools/extract_rom.py`](tools/extract_rom.py) realiza automáticamente:
1. Lectura de cabeceras NCSD y partición 0 (NCCH de la aplicación).
2. Extracción de la partición **ExeFS** (`.code` y `exheader.bin`).
3. Descompresión del algoritmo **Nintendo Extended FastLZSS / BLZ invertido**, expandiendo el ejecutable de 4.42 MB a **7.38 MB (7.737.344 bytes)**.
4. Ubicación del binario en `extracted/code.raw.bin`, listo para cargarse en la dirección virtual base **`0x00100000`**.
5. Verificación de integridad con hash SHA-256 de referencia.

---

## 🔍 Análisis Estático y Scratches (Ghidra / decomp.me)

1. **Configuración en Ghidra**:
   * Arquitectura: `ARM:LE:32:v6` o `ARM:LE:32:Cortex` (ARMv6K).
   * Formato: Raw Binary.
   * Dirección base de carga: `0x00100000`.
2. **Desarrollo en decomp.me**:
   * Plataforma: Nintendo 3DS / ARM.
   * Compilador: ARM Compiler (armcc / RVCT).
   * Opciones típicas: `--arm -O3 --apcs /interwork`.
3. **Validación**:
   * Una vez alcanzado el **100% Match** en decomp.me, el código se traslada a `src/` y se registra en `scratches/`.

---

## ⚖️ Política Legal y Ética

Este repositorio **NUNCA distribuye ni distribuirá código fuente comercial con copyright, claves criptográficas (bootrom / AES keys) ni activos audiovisuales del juego**. 

* Todo el proceso requiere que el usuario aporte una copia legal del juego original obtenida legítimamente.
* El proyecto se acoge al derecho de ingeniería inversa con fines educativos, de investigación y de interoperabilidad técnica.

---

<p align="center">
  Submódulo de decompilación para el reto <strong><a href="https://github.com/ChaconMoon/Decompilation-in-358-2">#DecompilandoEn358Dias</a></strong>.<br>
  Mantenido por <a href="https://github.com/ChaconMoon">Carlos Chacón (@ChaconMoon)</a>.
</p>
