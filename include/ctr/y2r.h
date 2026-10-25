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
                u8 pad[0x48];
                u16 flag;
        } Y2rSubContext;

        typedef struct
        {
                u8 pad[0x2180];
                Y2rSubContext sub;
        } Y2rObject;

        typedef struct
        {
                u32 field_524;
                u32 field_528;
                u32 unk_52C;
                u32 field_530;
                u32 field_534;
                u32 field_538;
                u32 field_53C;
                u32 field_540;
                u32 field_544;
                u32 field_548;
                u32 field_54C;
                u32 field_550;
                u32 field_554;
                u32 field_558;
                u32 field_55C;
                u32 field_560;
                u32 field_564;
                u32 field_568;
                u32 field_56C;
                u8 flag_570;
                u8 flag_571;
                u8 flag_572;
                u8 flag_573;
        } Y2rChannelState;

        typedef struct
        {
                u8 pad[0x524];
                Y2rChannelState state;
        } Y2rDevice;

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
