# Notas Técnicas de Sesión: NexElement, SVCs del Kernel y Pila ARM (19 de octubre de 2026)

## 1. Resumen Ejecutivo de la Sesión

- **Hitos Principales:**
  1. **Consolidación del Bloque `NexElement` (72 B contiguos en `ctr/nn_nex`):**
     - Decompilación de 5 funciones contiguas sin ningún salto en memoria:
       - `0x00340CE8` (`func_00340CE8`, 20 B, Nivel 2): Operador de asignación / copia de `NexElement`.
       - `0x00340CFC` (`func_00340CFC`, 12 B, Nivel 2): Setter multi-campo de `NexElement` (`s32` en `+0`, `s16` en `+4`).
       - `0x00340D08` (`func_00340D08`, 16 B, Nivel 2): Inicializador a cero / Clear de `NexElement`.
       - `0x00340D18` (`func_00340D18`,  4 B, Nivel 1): Stub vacío / Destructor por defecto `~NexElement()`.
       - `0x00340D1C` (`func_00340D1C`, 20 B, Nivel 2): Constructor de copia de `NexElement`.
  2. **Creación de la Cabecera de Red (`include/ctr/nex.h`):**
     - Definición formal de `NexElement` (`s32 unk_01`, `s16 unk_02`) y sus prototipos con guardas C++ (`extern "C"`).
  3. **Descubrimiento de Diferencias de Compilador (GCC vs ARMCC):**
     - Comportamiento de planificación de instrucciones: GCC reordena lecturas/escrituras mientras que ARMCC RVCT 4.0 b821 compila en orden secuencial `ldr -> str -> ldrh -> strh`.
     - Integración de reglas dedicadas de ARMCC en el `Makefile`.
  4. **Estudio Profundo de las Syscalls del Kernel CTR (`ctr/svc`):**
     - Comprensión de las instrucciones `push`, `svc` y el registro de pila `sp`.
     - Tipos de retorno `Result` y patrones de paso de `Handle`.

---

## 2. El Kernel de Nintendo 3DS y la Pila ARM (`sp`)

### A. ¿Por qué `svc` se implementa en Ensamblador?
- En el lenguaje C estándar **no existe ninguna palabra clave para invocar llamadas al sistema**.
- El procesador ARM11 de la Nintendo 3DS requiere ejecutar la instrucción de interrupción por software `svc 0xXX` para saltar de **Modo Usuario** a **Modo Supervisor/Kernel**.
- Para evitar que el compilador altere o mueva registros que el kernel espera por hardware, los *wrappers* del CTR-SDK se escriben como rutinas de ensamblador directo o en C con `__attribute__((naked))` y `__asm__ volatile`.

### B. El Registro `sp` (*Stack Pointer*) y la Instrucción `push`
- **`sp` (Registro `r13`):** Guarda la dirección de memoria de la cima de la pila en RAM. La pila en ARM crece en sentido descendente (hacia direcciones numéricas más bajas).
- **`push {r0}`:**
  1. Resta 4 bytes al puntero de pila: `sp = sp - 4`.
  2. Almacena el contenido del registro `r0` en la memoria RAM apuntada por `[sp]`.
- **`ldr r2, [sp]`:** Recupera el dato guardado en la pila y lo carga en el registro `r2`.
- **`add sp, sp, #4`:** Restaura la posición original de la pila sumando los 4 bytes previamente restados.

---

## 3. Arquitectura de las Syscalls en Nintendo 3DS

### A. ¿Qué es `Result`?
En todo el sistema operativo de Nintendo 3DS, **`Result`** es un entero con signo de 32 bits (`s32`):
- **`Result >= 0` (`0x00000000`):** Éxito (`R_SUCCEEDED`).
- **`Result < 0` (Bit 31 activo):** Error (`R_FAILED`). Codifica en sus bits:
  - *Description* (bits 0–9): Motivo específico del fallo.
  - *Module* (bits 10–17): Subsistema que generó el error (Kernel, FS, OS, etc.).
  - *Summary* (bits 21–26): Categoría general del error.
  - *Level* (bits 27–31): Gravedad (informativo, transitorio, fatal).

---

### B. Las 3 Familias de Llamadas al Sistema (`svc`)

| Familia | Firma en C | Comportamiento en ARM | Ejemplos |
| :--- | :--- | :--- | :--- |
| **1. Creación de Recursos** | `Result svc...(Handle *out, ...)` | **Usa la pila (`push {r0}`):** El puntero destino entra en `r0`, pero el kernel devuelve `Result` en `r0` y el `Handle` en `r1`. Para no perder el puntero, se salva en la pila antes del `svc`. | `svcCreateEvent`, `svcCreateThread`, `svcDuplicateHandle`, `svcCreateMemoryBlock` |
| **2. Operaciones sobre Recursos** | `Result svc...(Handle handle, ...)` | **Sin pila:** Recibe el identificador del recurso por valor (`Handle` en `r0`). El kernel realiza la operación y devuelve `Result` en `r0`. | `svcCloseHandle`, `svcSignalEvent`, `svcClearEvent` |
| **3. Control del Sistema / CPU** | `void svc...(void)` o `u64 svc...` | Funciones globales del sistema sin identificadores. | `svcExitProcess`, `svcSleepThread`, `svcGetSystemTick` |

---

## 4. Anatomía de `svcCreateEvent` (`0x0010AAA8`)

```arm
svcCreateEvent:
    push {r0}          @ 1. Salva el puntero de salida (Handle *event) en la pila
    svc  0x00000021    @ 2. Llama al Kernel (devuelve Result en r0, Handle en r1)
    ldr  r2, [sp]      @ 3. Recupera el puntero event desde la pila
    str  r1, [r2]      @ 4. Escribe el nuevo Handle en *event
    add  sp, sp, #4    @ 5. Limpia el hueco de 4 bytes en la pila
    bx   lr            @ 6. Retorna con el Result intacto en r0
```

---

## 5. Estado Global del Repositorio

- **Total de funciones matched:** **30 funciones** (`19` en `ctr`, `7` en `engine`, `4` en `game`).
- **Bytes verificados:** **444 bytes** de `.text` verificados byte-exact.
- **Syscalls matched en `ctr/svc` (5):**
  - `0x00104778` (`svcExitProcess`, 8 B) — `svc 0x03`
  - `0x0010AAA8` (`svcCreateEvent`, 24 B) — `svc 0x21`
  - `0x0010AAC0` (`svcDuplicateHandle`, 24 B) — `svc 0x38`
  - `0x00151FA0` (`svcCreateAddressArbiter`, 24 B) — `svc 0x17`
  - `0x00151FBC` (`svcSleepThread`, 8 B) — `svc 0x28`
  - `0x00151FC4` (`svcGetThreadId`, 24 B) — `svc 0x37`

