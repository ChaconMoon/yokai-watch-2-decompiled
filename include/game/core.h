#ifndef GAME_CORE_H
#define GAME_CORE_H

#include "types.h"

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================
 * Yo-kai Watch 2 (yw2) — Game Core Subsystem
 * General game utilities, entity management, and internal callbacks.
 * ======================================================================== */

extern s32 unk_0091B7B8;

void *func_00171C78(void);
void  func_0017656C(void);

/* Universal cleanup / validator callback (0x0014A06C) */
void func_0014A06C(void *arg);

#ifdef __cplusplus
}
#endif

#endif /* GAME_CORE_H */

