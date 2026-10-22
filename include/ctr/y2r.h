#ifndef CTR_Y2R_H
#define CTR_Y2R_H

#include "types.h"

#ifdef __cplusplus
extern "C"
{
#endif

        typedef struct
        {
                u32 unk_00;
                u32 unk_04;
                f32 value;
        } Y2rGlobalState;

        extern Y2rGlobalState unk_00815090;

        typedef struct
        {
                u8 pad[0xDCC];
                u8 flag;
        } Y2rContext;

        typedef struct
        {
                u8 pad[0x21C8];
                u16 flag;
        } Y2rObject;

        extern Y2rContext unk_008661EC;

        /* Method chaining wrapper invoking func_0014A06C */
        void *func_00112D8C(void *self);

        /* Returns u16 at offset +8648 */
        u16 func_00112E60(const Y2rObject *y2rObject);

        /* Invokes func_00136154(&unk_0086A0A4) and returns 1 */
        s32 func_001137C0(void);

        /* Returns bit 3 flag from unk_008661EC */
        u32 func_00113F58(void);

        /* Returns float value at offset +8 of unk_00815090 */
        f32 func_00113F70(void);

#ifdef __cplusplus
}
#endif

#endif /* CTR_Y2R_H */
