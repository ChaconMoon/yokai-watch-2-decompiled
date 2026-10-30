# Sesión Técnica: Consolidación de nn::applet y Arquitectura de Game Loops (28 de octubre de 2026)

> **Proyecto:** *Yo-kai Watch 2: Psychic Specters* (Nintendo 3DS - EUR `00040000001B2900` / `CTR-P-BYPP`)  
> **Autor y Análisis:** Carlos  
> **Reto:** `#DecompilandoEn358Dias`  
> **Estado:** 119 funciones verificadas al 100% byte-exact (26 en Capa 3 - Game Logic)

---

## 1. Resumen Ejecutivo de la Sesión

En esta sesión se lograron dos grandes hitos estructurales en la jerarquía de 3 capas del proyecto:

1. **Unificación 100% C++ de `nn::applet` (`src/ctr/nn/applet/applet.cpp`):**
   - Sustitución de 17 stubs fragmentados por una única unidad de traducción canónica.
   - Reconstrucción de las clases `AppletState` (`0x00814E00`) y `AppletContext` (`0x00815CA0`), modelando la tabla de despacho de callbacks (`Sleep`, `Awake`, `Notification`) y los flags de estado interno.
   - Demostración práctica de estabilidad del sistema operativo de 3DS: el retorno correcto al menú HOME (botón HOME) y el modo reposo al cerrar la tapa dependen directamente de esta máquina de estados.

2. **Despliegue de los Bucles de Juego de Level-5 (`src/game/loops/`):**
   - Identificación de la tabla de descriptores de bucles (`0x00107478`) y su interfaz en el Level-5 Framework (`LfwLoopClassInfo`).
   - Implementación limpia en C++ de las **11 clases de bucle (`ywCLoop*`)**, con sus métodos estáticos descriptores `getClassType()` y `getClassName()`.
   - Incorporación de 22 funciones en la Capa 3 (Game Logic), elevando el progreso total a **119 funciones (0.65%)** con cero regresiones.

---

## 2. Guía de Documentación Personal del Desarrollador (Carlos)

> [!NOTE]
> Esta sección está diseñada como bitácora y registro técnico curado personalmente por el desarrollador. Documenta el razonamiento inverso, la semántica en el juego, y demuestra la comprensión profunda de la arquitectura frente a cualquier generación automática ciega (*anti-vibecoding*).

A continuación se disponen las fichas técnicas de los módulos implementados para documentar:
- **Semántica en el juego:** Qué subsistema orquesta este bucle y en qué momento de la partida se ejecuta.
- **Análisis de registros y AAPCS:** Cómo viajan los parámetros y el valor de retorno.
- **Detalles del compilador (ARMCC / RVCT 4.0):** Por qué el literal pool se sitúa inmediatamente tras la función o al final de la unidad de traducción.

---

## 3. Fichas Técnicas: Módulo `nn::applet` (Capa 1: CTR-SDK)

### `nn::applet::CTR::IsApplication` (`0x001284E4` — 28 B)
* **Prototipo:** `bool nn::applet::CTR::IsApplication()`
* **Estructura involucrada:** `g_AppletState_00814E00.attribute` (+0x18)
* **Desensamblado clave:**
  ```arm
  ldr  r3, [pc, #12]   @ 0x00814E00
  ldr  r0, [r3, #24]   @ offset +0x18 (attribute)
  ands r0, r0, #7      @ Máscara de los 3 bits inferiores
  moveq r0, #1         @ Si es 0 -> true (es aplicación estándar)
  movne r0, #0         @ Si no -> false (es applet o módulo residente)
  bx   lr
  ```
* **Notas de Carlos (Análisis personal y deducción):**
  > *Escribe aquí tus observaciones sobre cómo la 3DS diferencia entre el ejecutable del juego y un applet del sistema (como el teclado o el navegador de internet)...*

---

### `nn::applet::detail::SetNotificationCallback` / `SetSleepCallback` / `SetAwakeCallback`
* **Direcciones:** `0x00128544` (Notification), `0x00128588` (Sleep), `0x001285C0` (Awake)
* **Estructura involucrada:** `g_AppletState_00815CA0.callbacks[]` (+0x20) y `callback_args[]` (+0x60)
* **Notas de Carlos (Análisis personal y deducción):**
  > *Escribe aquí tus observaciones sobre la tabla de callbacks, cómo se asocian las funciones con sus contextos de usuario (puntero `arg`), y qué ocurre en el hardware cuando se cierra la consola...*

---

## 4. Fichas Técnicas: Clases `ywCLoop*` (Capa 3: Game Logic)

### Arquitectura de Descriptores de Nivel-5
En el motor de Level-5, cada máquina de estados de juego hereda de `lfwCLoop` y registra un descriptor de 12 bytes en `0x00107478`:
```cpp
struct LfwLoopClassInfo {
    void *(*createInstance)(void);    /* Constructor / Factory de la clase */
    s32   (*getClassType)(void);       /* Retorna el tipo de clase (0 para bucles estándar) */
    const char *(*getClassName)(void); /* Retorna el puntero a la cadena RTTI en .data */
};
```

---

### 1. `ywCLoopRPG` (Mundo Exterior / Modo Aventura)
* **Direcciones:** `getClassType` (`0x0010CEE8`, 8 B) · `getClassName` (`0x0010CEF0`, 12 B)
* **String literal:** `"ywCLoopRPG"` en `0x0086048C`
* **Archivo:** [`src/game/loops/ywCLoopRPG.cpp`](../../src/game/loops/ywCLoopRPG.cpp)
* **Notas de Carlos:**
  > *Escribe aquí tus notas: ¿Qué papel tiene este bucle durante el movimiento de Nathan/Katie por Floridablanca, interacción con NPCs y transiciones de cámara?...*

---

### 2. `ywCLoopMain` (Máquina de Estados Principal)
* **Direcciones:** `getClassType` (`0x0010CFF4`, 8 B) · `getClassName` (`0x0010CFFC`, 12 B)
* **String literal:** `"ywCLoopMain"` en `0x00860497`
* **Archivo:** [`src/game/loops/ywCLoopMain.cpp`](../../src/game/loops/ywCLoopMain.cpp)
* **Notas de Carlos:**
  > *Escribe aquí tus notas: Cómo este bucle raíz coordina el paso entre el título, la partida guardada y los bucles hijos...*

---

### 3. `ywCLoopBattle` (Sistema de Combate de la Ruleta)
* **Direcciones:** `getClassType` (`0x0010D500`, 8 B) · `getClassName` (`0x0010D508`, 12 B)
* **String literal:** `"ywCLoopBattle"` en `0x008604C8`
* **Archivo:** [`src/game/loops/ywCLoopBattle.cpp`](../../src/game/loops/ywCLoopBattle.cpp)
* **Notas de Carlos:**
  > *Escribe aquí tus notas: La sincronización de la pantalla táctil para la ruleta de 6 Yo-kai, animaciones de animáximum y turnos en tiempo real...*

---

### 4. `ywCLoopMenu` (Interfaz de Usuario, Medalla y Mochila)
* **Direcciones:** `getClassType` (`0x0010D134`, 8 B) · `getClassName` (`0x0010D13C`, 12 B)
* **String literal:** `"ywCLoopMenu"` en `0x008604A3`
* **Archivo:** [`src/game/loops/ywCLoopMenu.cpp`](../../src/game/loops/ywCLoopMenu.cpp)
* **Notas de Carlos:**
  > *Escribe aquí tus notas sobre el menú del Yo-kai Pad, gestión de objetos y medallas...*

---

### 5. `ywCLoopOrgeTime` (Pesadilla / Hora Terror)
* **Direcciones:** `getClassType` (`0x0010DC40`, 8 B) · `getClassName` (`0x0010DC48`, 12 B)
* **String literal:** `"ywCLoopOrgeTime"` en `0x00860546`
* **Archivo:** [`src/game/loops/ywCLoopOrgeTime.cpp`](../../src/game/loops/ywCLoopOrgeTime.cpp)
* **Notas de Carlos:**
  > *Escribe aquí tus notas: Mecánica de sigilo y persecución contra Gargaros/Ogrón, aparición de esbirros y niebla...*

---

### 6. `ywCLoopCapsule` (Expendekai / Crank-a-kai)
* **Direcciones:** `getClassType` (`0x0010D63C`, 8 B) · `getClassName` (`0x0010D644`, 12 B)
* **String literal:** `"ywCLoopCapsule"` en `0x008604D9`
* **Archivo:** [`src/game/loops/ywCLoopCapsule.cpp`](../../src/game/loops/ywCLoopCapsule.cpp)
* **Notas de Carlos:**
  > *Escribe aquí tus notas sobre la tirada diaria de monedas, cálculo de recompensas y animación 3D de la máquina...*

---

### 7. `ywCLoopWatchmap` (Radar Yo-kai y Lente)
* **Direcciones:** `getClassType` (`0x0010DD40`, 8 B) · `getClassName` (`0x0010DD48`, 12 B)
* **String literal:** `"ywCLoopWatchmap"` en `0x00860556`
* **Archivo:** [`src/game/loops/ywCLoopWatchmap.cpp`](../../src/game/loops/ywCLoopWatchmap.cpp)
* **Notas de Carlos:**
  > *Escribe aquí tus notas sobre el radar de rango C/B/A/S, aguja detectora y minijuego de enfocar con la lente...*

---

### 8. `ywCLoopYokaispot` (Puntos Yo-kai)
* **Direcciones:** `getClassType` (`0x0010E35C`, 8 B) · `getClassName` (`0x0010E364`, 12 B)
* **String literal:** `"ywCLoopYokaispot"` en `0x008605AA`
* **Archivo:** [`src/game/loops/ywCLoopYokaispot.cpp`](../../src/game/loops/ywCLoopYokaispot.cpp)
* **Notas de Carlos:**
  > *Escribe aquí tus notas sobre los misterios urbanos y apariciones ocultas...*

---

### 9. `ywCLoopRace` (Carrera de Bicicletas)
* **Direcciones:** `getClassType` (`0x0010D234`, 8 B) · `getClassName` (`0x0010D23C`, 12 B)
* **String literal:** `"ywCLoopRace"` en `0x008604AF`
* **Archivo:** [`src/game/loops/ywCLoopRace.cpp`](../../src/game/loops/ywCLoopRace.cpp)
* **Notas de Carlos:**
  > *Escribe aquí tus notas sobre la física de la bici, checkpoints y circuito urbano...*

---

### 10. `ywCLoopEvent` (Cinemáticas y Diálogos)
* **Direcciones:** `getClassType` (`0x0010D3A8`, 8 B) · `getClassName` (`0x0010D3B0`, 12 B)
* **String literal:** `"ywCLoopEvent"` en `0x008604BB`
* **Archivo:** [`src/game/loops/ywCLoopEvent.cpp`](../../src/game/loops/ywCLoopEvent.cpp)
* **Notas de Carlos:**
  > *Escribe aquí tus notas sobre el intérprete de scripts de historia y bloqueo de controles del jugador...*

---

### 11. `ywCLoopQR` (Lector de Códigos QR y Contenido Descargable)
* **Direcciones:** `getClassType` (`0x0010FEBC`, 8 B) · `getClassName` (`0x0010FEC4`, 12 B)
* **String literal:** `"ywCLoopQR"` en `0x00860794`
* **Archivo:** [`src/game/loops/ywCLoopQR.cpp`](../../src/game/loops/ywCLoopQR.cpp)
* **Notas de Carlos:**
  > *Escribe aquí tus notas sobre la integración con las cámaras de la 3DS para escanear medallas físicas...*

---

## 5. Glosario Técnico y Convenciones de Compilador

- **AAPCS en Leaf Methods:** Funciones hoja que retornan enteros o punteros depositan el valor en `r0` y retornan inmediatamente con `bx lr`, prescindiendo de marco de pila.
- **Partición de Translation Units:** En GCC/ARMCC, compilar cada clase en su propio `.cpp` asegura que los literales de cadena del descriptor (`s_ywCLoop*`) queden en un literal pool contiguo a su clase en `.rodata` y referenciados con `ldr r0, [pc]` exacto.

