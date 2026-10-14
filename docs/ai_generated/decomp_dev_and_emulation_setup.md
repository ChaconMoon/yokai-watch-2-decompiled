# Sesión: Verificación de Emulación en Azahar e Integración con decomp.dev

> **Fecha:** 14 de octubre de 2026  
> **Proyecto:** *Yo-kai Watch 2: Psychic Specters* (Nintendo 3DS - EUR `00040000001B2900`)  
> **Autor / Asistencia:** Documentación generada con asistencia de IA (Antigravity) para el reto `#DecompilandoEn358Dias`.

---

## 1. Verificación de Ejecución Real en Azahar (AppImage)

Se implementó un pipeline para probar que el emulador Azahar (fork de Citra) ejecuta realmente el binario recompilado y parcheado (`build/code.bin`):

1. **Inyección en ExeFS:**
   - La herramienta [`tools/inject_code.py`](../../tools/inject_code.py) toma el ejecutable original de referencia (`extracted/code.raw.bin`), sobreescribe los bytes de las funciones decompiladas y genera un `code.bin` de 7,737,344 bytes.
   - Ubicación en el sistema:
     ```text
     ~/.local/share/azahar-emu/load/mods/00040000001B2900/exefs/code.bin
     ```
2. **Prueba Empírica del Cuelgue (Smoke Test):**
   - Se generó un binario de prueba (`build/code_test_freeze.bin`) con un bucle infinito ARM (`b .`, `0xEAFFFFFE`) en `0x00100024` (inicio de `clear_bss`).
   - Al iniciar en Azahar, la pantalla quedó completamente en negro a 0 FPS en el primer microsegundo, **confirmando al 100% que Azahar ejecuta el código inyectado**.
   - Tras comprobarlo, se restauró el binario limpio con las 20 funciones recompiladas, arrancando el juego con normalidad.

---

## 2. Integración con `decomp.dev` y `objdiff`

El repositorio quedó completamente integrado con el rastreador público de progreso de la comunidad ([`decomp.dev`](https://decomp.dev)):

### A. Herramientas y Objetos Objetivo (`expected/`)
- Se descargó el binario de línea de comandos [`tools/objdiff-cli`](../../tools/objdiff-cli) (v3.8.2).
- Se implementó [`tools/generate_expected.py`](../../tools/generate_expected.py) para extraer y ensamblar los slices individuales de cada función desde `code.raw.bin` hacia `expected/<symbol>.o`.
- Se actualizó [`.gitignore`](../../.gitignore) con `!expected/*.o` para rastrear estos objetos sin violar derechos de autor (solo contienen los símbolos aislados).

### B. Flujo de GitHub Actions ([`.github/workflows/report.yml`](../../.github/workflows/report.yml))
- Se configuró el workflow para ejecutarse tras cada `push` o `Pull Request`.
- Instala la toolchain GNU ARM (`gcc-arm-none-eabi`), `wibo-i686` y `objdiff-cli`.
- Compila los objetos en `build/` (usando fallback automático a GCC si ARMCC no estuviese configurado con secrets en CI).
- Sube el reporte como artefacto con la convención reglamentaria: **`00040000001B2900_report`**.

### C. Métricas Reales y Escala del Treemap
- **El problema detectado:** Al principio `decomp.dev` mostraba ~80-90% decompilado porque `objdiff` sólo comparaba las 20 funciones entre sí (~240 bytes).
- **La solución implementada:** Se creó [`tools/generate_undecompiled.py`](../../tools/generate_undecompiled.py), que genera al vuelo un objeto `expected/undecompiled.o` con los **4,802,885 bytes restantes** (~18,272 funciones del catálogo).
- **Resultado actual en `decomp.dev`:**
  - **Total Code:** `4.80 MB` (`4,803,125 bytes`)
  - **Matched Code:** `216 bytes` (20 funciones verificadas byte-exact)
  - **Progreso:** **0.01%**

---

## 3. Estado de Visibilidad en `decomp.dev`

En el panel de control aparece el siguiente aviso:
> *"This project is hidden until it has reached a minimum of 0.5% matched code."*

* **Significado:** El proyecto ya está registrado y activo, pero la portada principal de `decomp.dev/projects` exige un mínimo del **0.5%** (~24,015 bytes / ~24 KB) para evitar spam de repositorios recién creados.
* **Acceso:** Tu página personal de proyecto y el reporte de commits ya están operativos y accesibles directamente.

---

## 4. Estado del Proyecto y Próximos Pasos

* **Funciones verificadas byte-exact:** **20 / ~18,292 (0.11%)**
* **Bytes completados:** **252 B**
* **Siguiente función candidata:**
  - **[`src/system/func_001274A0.c`](../../src/system/func_001274A0.c)** (`0x001274A0`, 24 B)
  - *Tipo:* Bucle atómico spinlock (`ldrex` / `strex`)
  - *Compilador:* ARMCC 4.0 [Build 821] (`--cpu=mpcore -O3`)
