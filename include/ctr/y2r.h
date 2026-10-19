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

        /* Returns float value at offset +8 of unk_00815090 */
        float func_00113F70(void);

#ifdef __cplusplus
}
#endif

#endif /* CTR_Y2R_H */
