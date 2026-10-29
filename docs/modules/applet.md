# Official Documentation: Lifecycle Subsystem (nn::applet)

> **Subsystem:** CTR-SDK Applet Management (`src/ctr/nn/applet/applet.cpp`, `include/ctr/applet.h`)  
> **Layer:** Layer 1 — Nintendo CTR-SDK  
> **Author & Documentation:** Carlos  
> **Status:** 100% C++ byte-exact matching (17 unified routines)

---

## 1. Nintendo 3DS Lifecycle Management Overview

The `nn::applet` module is the official CTR-SDK component that interfaces the game title with the Nintendo 3DS `APT` (*Applet Manager*) operating system service.

It is responsible for handling critical hardware interrupts and user-driven events:
1. **HOME Menu Transitions:** When the user presses the HOME button, the game suspends its rendering and audio processing loops, yielding display framebuffers to the *Home Menu Applet*.
2. **Sleep Mode (Low Power):** Closing the console shell triggers power-saving callbacks, powering down the screens and pausing the digital signal processor (DSP) audio pipeline.
3. **System Notifications:** Low-battery warnings, StreetPass events, and sleep state transitions.

---

## 2. Primary Data Structures

### `nn::applet::detail::AppletState` (VMA: `0x00814E00`)
Global state structure holding internal lifecycle flags and title attributes:

```cpp
class AppletState {
public:
    bool IsApplication() const { return (attribute & 0x07) == 0; }

public:
    u8  pad_00[0x07]; /* 0x00 - 0x06 */
    s8  unk_07;       /* 0x07: Signed state flag */
    s8  unk_08;       /* 0x08: Signed state flag */
    u8  pad_09[0x02]; /* 0x09 - 0x0A */
    u8  unk_0B;       /* 0x0B: State byte */
    u8  unk_0C;       /* 0x0C: State byte */
    s8  unk_0D;       /* 0x0D: Signed state byte */
    u8  pad_0E[0x02]; /* 0x0E - 0x0F */
    u32 unk_10;      /* 0x10: Consumed by nn::dsp */
    u32 unk_14;      /* 0x14: Used by Level-5 Framework (LFW) */
    u32 attribute;   /* 0x18: Title type attribute (0 = Standard application) */
};
```

### `nn::applet::detail::AppletContext` (VMA: `0x00815CA0`)
Dispatch table for event callbacks and user context pointers:

```cpp
class AppletContext {
public:
    s8    unk_00;             /* 0x00: Status byte read by nn::dsp */
    u8    pad_01[0x1F];       /* 0x01 - 0x1F */
    void *callbacks[4];       /* 0x20 - 0x2F: Transition event callbacks */
    u8    pad_30[0x30];       /* 0x30 - 0x5F */
    void *callback_args[4];   /* 0x60 - 0x6F: User context arguments passed to callbacks */
};
```

---

## 3. Technical Specifications & Author's Notes

### `nn::applet::CTR::IsApplication` (`0x001284E4` — 28 B)
* **Prototype:** `bool nn::applet::CTR::IsApplication()`
* **Source:** [`src/ctr/nn/applet/applet.cpp`](../../src/ctr/nn/applet/applet.cpp#L19-L25)
* **Author's Notes (Carlos):**
  This function verifies whether the currently running process is the main game (*Yo-kai Watch 2*). To do so, it applies a bitwise AND mask with `7` (`0b111` in binary) against the title attributes (`attribute & 7`). A value of `0` (`0b000`) indicates the standard application identifier.

---

### Sleep and System Callbacks
* `void SetNotificationCallback(void *callback, void *arg)` (`0x00128544` — 20 B)
* `void SetSleepCallback(void *callback, void *arg)` (`0x00128588` — 20 B)
* `void SetAwakeCallback(void *callback, void *arg)` (`0x001285C0` — 20 B)
* **Author's Notes (Carlos):**
  * `SetSleepCallback`: Registers the sleep transition callback; when the user closes the 3DS shell, the system invokes this callback to suspend game execution and shut down the audio engine.
  * `SetAwakeCallback`: Registers the awake transition callback, which restores normal execution when the console is reopened.
  * `SetNotificationCallback`: Registers the notification callback for handling system events (such as low battery warnings).

---

### Internal State Accessors
* `SetState10`, `GetState0C`, `SetState0C`, `SetState08_1`, `GetState08`, `SetState08_0`, `GetState0B`, `SetState0B`, `GetState0D`, `SetState0D`, `SetState07_1`, `GetState07`, `SetState07_0`.
* **Author's Notes (Carlos):**
  * `SetState<HexOffset>`: Sets a specific state value at that offset in the global structure (e.g., `SetState10` stores a 32-bit word, while `SetState0C` stores a byte).
  * `SetState<HexOffset>_0` / `_1`: Clears (`0`) or asserts (`1`) the boolean state flag at that specific byte offset.
  * `GetState<HexOffset>`: Reads and returns the state value stored at that offset.
