# Sesión Técnica: Arquitectura en 3 Capas, Structs en C y Emulación (18 de octubre de 2026)

> **Proyecto:** *Yo-kai Watch 2: Psychic Specters* (Nintendo 3DS - EUR `00040000001B2900`)  
> **Reto:** `#DecompilandoEn358Dias`  
> **Estado:** 21 funciones verificadas byte-exact (100% matched)

---

## 1. Resumen Ejecutivo

Durante esta sesión se lograron tres grandes hitos en el proyecto:

1. **Pipeline de Inyección y Emulación con Azahar (`make inject`):**
   - Automatización de la compilación e inyección en `build/code.bin`.
   - Copia directa del ejecutable a la carpeta de mods del emulador:
     `~/.local/share/azahar-emu/load/mods/00040000001B2900/exefs/code.bin`.
   - Verificación de que el hash SHA-256 (`b536dfce...`) se mantiene íntegro.

2. **Estudio Comparativo Cross-Binary (YW1, YW2 BS/FS, YW3):**
   - Análisis de los binarios comerciales preservados fuera del repositorio (`other_code_binaries/` en `.gitignore`).
   - Identificación del selector de versión en `0x001047B0` (`0` = Fantasqueletos, `1` = Carnánimas, `2` = Mentespectros).
   - Descubrimiento de que *Fantasqueletos* y *Carnánimas* son idénticos al 99.999987% (solo 1 byte de diferencia).
   - Cobertura estimada de ~91.5% de código común con YW2 BS/FS y ~60% con YW1 y YW3.

3. **Nueva Función Decompilada al 100%:**
   - **`func_001280A8`** (`src/ctr/nn/ndm/func_001280A8.c`): 24 bytes, Nivel 3.
   - Indexador de array en estructura con comprobación de límites y predicación condicional ARM.

---

## 2. Conceptos Clave de Ensamblador ARMv6K y C

### A. La Instrucción `ldrh` y el Acceso a Memoria
- **`ldrh r2, [r0, #4]`**:
  - Lee 2 bytes (16 bits) sin signo desde la dirección `r0 + 4`.
  - Lo almacena en el registro `r2` con relleno de ceros (*zero-extend*).
  - En C, esto corresponde a acceder a un campo de tipo `u16` situado en el offset `+4` de un `struct` apuntado por `r0`: `ctx->count`.

### B. ¿Por qué `ldrh` va acompañado de `cmp`?
- En procesadores ARM (arquitectura RISC *Load/Store*), la instrucción `cmp` **no puede leer directamente de la memoria RAM**.
- El procesador debe primero "cargar" el dato de la memoria RAM a un registro de propósito general (`ldrh r2, [r0, #4]`) y luego compararlo con el valor de entrada (`cmp r2, r1`).

### C. Predicación ARM: `addhi` y `movls`
- **`cmp r2, r1`** compara el límite del contenedor (`r2`) con el índice solicitado (`r1`).
- Los sufijos evalúan condiciones **sin signo (`unsigned`)**:
  - **`hi` (*Higher* / Mayor estricto):** Se ejecuta solo si `r2 > r1` (el índice está dentro de rango).
  - **`ls` (*Lower or Same* / Menor o igual):** Se ejecuta solo si `r2 <= r1` (fuera de rango).
- **`addhi r0, r0, r1, lsl #3`**:
  - `lsl #3` multiplica `r1` por $2^3 = 8$ (el tamaño de cada elemento del array).
  - Suma el resultado al puntero base `r0`.
- **`addhi r0, r0, #12`**:
  - Suma 12 bytes (`0x0C`) para saltar los campos de la cabecera del struct.
- **`movls r0, #0`**:
  - Si el índice estaba fuera de rango, pone `r0 = NULL` (0).

---

## 3. Correspondencia entre `struct` en C y Offsets en Memoria

En C no se escriben los números de posición a mano en la función; se define una plantilla apilando tipos de datos según su tamaño:
- `u8`: 1 byte
- `u16`: 2 bytes
- `u32`: 4 bytes

```text
Offset en RAM:
+0 bytes          +4 bytes       +6 bytes       +8 bytes          +12 bytes
┌─────────────────┬──────────────┬──────────────┬─────────────────┬───────────────────────┐
│ unk_00 (u32)    │ count (u16)  │ unk_06 (u16) │ unk_08 (u32)    │ items[0] (Element8)   │
│ (ocupa 4 bytes) │ (ocupa 2 B)  │ (ocupa 2 B)  │ (ocupa 4 bytes) │ (ocupa 8 bytes)       │
└─────────────────┴──────────────┴──────────────┴─────────────────┴───────────────────────┘
```

Al escribir en C:
```c
if (ctx->count <= index) {
    return NULL;
}
return &ctx->items[index];
```
El compilador:
1. Sabe que `count` está en el offset `+4` y mide 2 bytes $\rightarrow$ genera `ldrh r2, [r0, #4]`.
2. Sabe que `items` empieza en el offset `+12` y cada elemento mide 8 bytes $\rightarrow$ genera `addhi r0, r0, r1, lsl #3` y `addhi r0, r0, #12`.
3. Sabe que `NULL` es 0 $\rightarrow$ genera `movls r0, #0`.

---

## 4. Pipeline de Emulación (`make inject`)

Se ha integrado el target `make inject` en el `Makefile`:
1. Recompila todos los objetos en `build/src/<capa>/...`.
2. Ejecuta `tools/inject_code.py` para sobreescribir las funciones verificadas en el binario base.
3. Copia automáticamente el resultado a:
   ```text
   ~/.local/share/azahar-emu/load/mods/00040000001B2900/exefs/code.bin
   ```
Permitiendo probar cambios en el emulador Azahar de forma instantánea.

---

## 5. Próximo Candidato para la Siguiente Sesión

- **Función:** `func_00340CFC` (`0x00340CFC`)
- **Capa / Módulo:** `ctr/nn_nex`
- **Tamaño:** 12 bytes (3 instrucciones)
- **Tipo:** Setter elemental de 2 campos de un `struct` (`str` a `+0`, `strh` a `+4`).
- **Código ensamblador:**
  ```arm
  func_00340CFC:
      str  r1, [r0]
      strh r2, [r0, #4]
      bx   lr
  ```
