#ifndef GAME_LOOPS_H
#define GAME_LOOPS_H

#include "types.h"
#include "engine/lfw.h"

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================
 * Yo-kai Watch 2 (yw2) — Game Loop Subclasses (ywCLoop*)
 * Registered in the loop descriptor table starting at 0x00107478:
 *   - ywCLoopRPG         (0x0086048C)
 *   - ywCLoopMain        (0x00860497)
 *   - ywCLoopMenu        (0x008604A3)
 *   - ywCLoopRace        (0x008604AF)
 *   - ywCLoopEvent       (0x008604BB)
 *   - ywCLoopBattle      (0x008604C8)
 *   - ywCLoopCapsule     (0x008604D9)
 *   - ywCLoopOrgeTime    (0x00860546)
 *   - ywCLoopWatchmap    (0x00860556)
 *   - ywCLoopQR          (0x00860794)
 * ======================================================================== */

void *func_0010C894(void);                  /* 0x0010C894 */
void  func_0011054C(void *hdr);             /* 0x0011054C */

#ifdef __cplusplus
}
#endif

#endif /* GAME_LOOPS_H */

