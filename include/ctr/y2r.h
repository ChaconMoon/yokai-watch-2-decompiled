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
                float value;
        } Y2rGlobalState;

        extern Y2rGlobalState unk_00815090;

        typedef struct
        {
                u8 pad[3532];
                u8 flag;
        } Y2rContext;

        extern Y2rContext unk_008661EC;

        /* Method chaining wrapper invoking func_0014A06C */
        void *func_00112D8C(void *self);

        /* Returns u16 at offset +8648 */
        u16 func_00112E60(const void *ptr);

        /* Invokes func_00136154(&unk_0086A0A4) and returns 1 */
        s32 func_001137C0(void);

        /* Returns bit 3 flag from unk_008661EC */
        u32 func_00113F58(void);

        /* Returns float value at offset +8 of unk_00815090 */
        float func_00113F70(void);

#ifdef __cplusplus
}
#endif

#endif /* CTR_Y2R_H */
