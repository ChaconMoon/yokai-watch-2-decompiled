---
name: decomp-me-context
description: >-
  Prepares all essential assets in 100% pure C to create and work on a scratch in decomp.me.
  Given a function address, symbol, or 'list', it delivers: (1) Target Assembly with clean labels
  and literal pool, (2) Current decompiled function adapted to pure C (with explicit 'self' pointer
  if it is a C++ method), (3) Self-contained pure C Context header ready to copy-paste into
  decomp.me (no #include, no C++ constructs), and (4) Compiler flags and matching recommendations.
---

# `decomp-me-context` — Asistente de Scratch y Contexto en C Puro para decomp.me

Esta skill automatiza y genera todo lo necesario en **C puro (estándar C)** para trabajar y crear scratches en [decomp.me](https://decomp.me) a partir del estado real del repositorio (*Yo-kai Watch 2* / Nintendo 3DS).

---

## 1. Modos de Uso

### Modo 1: Listar funciones pendientes (`list`)
Cuando el usuario envía el comando con la palabra `list`:
```bash
python3 .agents/skills/decomp-me-context/scripts/decomp_me_helper.py list
```
Muestra la tabla de todas las funciones que están en estado `wip`, `staged`, `in_progress` o `pending` en `config/functions.csv`, detallando dirección, tamaño, capa/submódulo y descripción.

### Modo 2: Preparar paquete de scratch para una función (`<0xADDRESS | symbol>`)
Cuando el usuario indica una dirección o identificador (o cuando se invoca la skill):
```bash
python3 .agents/skills/decomp-me-context/scripts/decomp_me_helper.py <0xADDRESS>
```

---

## 2. Reglas Estrictas de Entrega al Usuario (Todo en C Puro, Listo para Copiar y Pegar)

Dado que `decomp.me` compila los scratches en **C**, TANTO el **Source Code** como el **Context** DEBEN entregarse siempre en **C puro** (nunca C++), siguiendo rigurosamente esta estructura en 4 secciones:

### 1. Pestaña `Target Assembly` (decomp.me)
- Ensamblador limpio generado con etiquetas locales relativas `.L_<ADDRESS>` y literales con formato `.word 0x...`.
- Listo para ser copiado y pegado directamente en la pestaña **Target Assembly** del scratch en `decomp.me`.

### 2. Pestaña `Source Code` (Tu función actual adaptada a C puro)
- Si la función en el repositorio está en un archivo `.cpp` (método de clase C++ como `ClassName::method(...)`), se entrega **adaptada a C puro**:
  - Sin `ClassName::`, usando el nombre del símbolo del ensamblador.
  - Con el puntero `self` explícito como primer parámetro (`ClassName *self` o `const ClassName *self`).
  - Referencias `&other` convertidas a punteros `*other` y accesos a miembros prefijados con `self->`.

### 3. Pestaña `Context` (decomp.me) — **100% C Puro y Autocontenido para Copiar y Pegar**
- **REGLA CRÍTICA:** El bloque de Contexto debe ser **100% C válido**:
  - **SIN** directivas `#include` ni guardas `#ifndef ... #define ...` de cabecera.
  - **SIN** `#ifdef __cplusplus`, `extern "C"`, `namespace`, `class`, `public:`, `private:` ni `friend`.
  - Todas las clases/estructuras se declaran como `typedef struct ... { ... } ...;` con sus campos exactos y todos los tipos base de `include/types.h` (`u8`, `u16`, `u32`, `u64`, `s8`, `s16`, `s32`, `s64`, `bool32`, `NULL`).
- **El usuario debe poder copiar este bloque entero con un solo clic y pegarlo directamente en la pestaña Context de decomp.me sin tocar nada.**

### 4. Configuración y Cambios Sugeridos para el MATCH (WIP)
- **Compiler:** `ARM C/C++ (RVCT 4.0 build 821)` (en modo C) o `ARM11 GCC`.
- **Compiler Flags:** `--cpu=mpcore -O3 --gnu -c` (opciones alternativas: `-Otime`, `-Ospace`, `-O2`).
- **Análisis de Discrepancias:** Diferencias de regalloc, modismos de big-endian, unificación de epílogo (`return` único vs `pop` condicionales), etc.

---

## 3. Ejemplo de Estructura de Respuesta

```markdown
### 📋 Paquete decomp.me (C Puro): `<symbol_name>` (`<0xADDRESS>`)

#### 1. Pestaña `Target Assembly` (decomp.me)
```arm
<ensamblador listo para pegar>
```

#### 2. Pestaña `Source Code` (Implementación actual en C puro)
```c
<código actual de la función en C puro>
```

#### 3. Pestaña `Context` (decomp.me — C puro listo para copiar y pegar)
```c
<contexto 100% autocontenido en C puro, sin #include ni C++, con todos los typedefs y structs>
```

#### 4. Estrategia y Cambios Recomendados para Match
- Diagnóstico de diferencias de registro / flujo de control.
- Banderas de compilación recomendadas.
```

