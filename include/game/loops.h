#ifndef GAME_LOOPS_H
#define GAME_LOOPS_H

#include "types.h"
#include "engine/lfw.h"

/* ========================================================================
 * Yo-kai Watch 2 (yw2) — Game Loop Subclasses (ywCLoop*)
 *
 * Registered in the Level-5 loop descriptor table (0x00107478):
 *   - ywCLoopMenu        (0x008604A3)
 *   - lfwCLoopEmpty      (0x008602F8)
 *   - ywCLoopMain        (0x00860497)
 *   - ywCLoopRPG         (0x0086048C)
 *   - ywCLoopEvent       (0x008604BB)
 *   - ywCLoopBattle      (0x008604C8)
 *   - ywCLoopWatchmap    (0x00860556)
 *   - ywCLoopYokaispot   (0x008605AA)
 * Standalone loop classes:
 *   - ywCLoopRace        (0x008604AF)
 *   - ywCLoopCapsule     (0x008604D9)
 *   - ywCLoopOrgeTime    (0x00860546)
 *   - ywCLoopQR          (0x00860794)
 * ======================================================================== */

#ifdef __cplusplus

class ywCLoopRPG
{
public:
        static s32 getClassType();
        static const char *getClassName();
};

class ywCLoopMain
{
public:
        static s32 getClassType();
        static const char *getClassName();
};

class ywCLoopMenu
{
public:
        static s32 getClassType();
        static const char *getClassName();
};

class ywCLoopRace
{
public:
        static s32 getClassType();
        static const char *getClassName();
};

class ywCLoopEvent
{
public:
        static s32 getClassType();
        static const char *getClassName();
};

class ywCLoopBattle
{
public:
        static s32 getClassType();
        static const char *getClassName();
};

class ywCLoopCapsule
{
public:
        static s32 getClassType();
        static const char *getClassName();
};

class ywCLoopOrgeTime
{
public:
        static s32 getClassType();
        static const char *getClassName();
};

class ywCLoopWatchmap
{
public:
        static s32 getClassType();
        static const char *getClassName();
};

class ywCLoopYokaispot
{
public:
        static s32 getClassType();
        static const char *getClassName();
};

class ywCLoopQR
{
public:
        static s32 getClassType();
        static const char *getClassName();
};

#endif /* __cplusplus */

#ifdef __cplusplus
extern "C" {
#endif

/* Loop Controller Globals */
extern s32 unk_0086C8CC;

typedef struct YwLoopControllerState
{
        u8    enabled;       /* +0x00: Flag booleano (1 = activo) */
        u8    mode;          /* +0x01: Flag / modo de control */
        u8    pad_02[0x02];  /* +0x02 - +0x03: Alineación a 4 bytes */
        void *target;        /* +0x04: Puntero de destino / contexto */
        void *callback;      /* +0x08: Puntero callback guardado por func_0010C870 */
        u32   pad_0C;        /* +0x0C - +0x0F: Alineación final */
} YwLoopControllerState;

extern YwLoopControllerState g_LoopState_00815C90;

void *func_0010C894(void);
void  func_0010C870(void *callback);
void  func_0010C880(void);
void  func_0010C8A0(u8 mode);
void  func_0010CA68(void *target);

typedef struct YwLoopHeader
{
        union
        {
                struct
                {
                        u8 status;
                        u8 pad[3];
                };
                u32 unk_00;
        };
        u32 value;
} YwLoopHeader;

void func_0011054C(YwLoopHeader *ywLoopHeader);

#ifdef __cplusplus
}
#endif

#endif /* GAME_LOOPS_H */
