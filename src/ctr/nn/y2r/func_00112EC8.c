#include <ctr/y2r.h>

extern void *unk_00867CF8;
extern void func_0012F804(void *mutex);
extern void func_00155E8C(void *mutex);

/**
 * @brief func_00112EC8
 * @address 0x00112EC8
 * Y2R mutex lock/unlock sequence on unk_00867CF8
 */
void func_00112EC8(void)
{
        func_0012F804(&unk_00867CF8);
        func_00155E8C(&unk_00867CF8);
}
