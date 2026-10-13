typedef signed char s8;
typedef unsigned char u8;
typedef int s32;
typedef unsigned int u32;

s32 func_0011EE70(void *, void *, s32 *, s32, s32);
s32 func_00120ABC(void *, s32 *, s32, s32, s32, s32);
void func_0014D528(void *);
void func_0014D534(void *);

typedef void (*VFunc)(void *);
#define CALL_VFUNC(obj) ((*(VFunc **)(obj))[2](obj))

s32 func_0010B6E4(void *arg0, void *arg1, s32 *arg2, s32 arg3, s32 arg4)
{
    s32 temp_sl;
    s32 var_r0;
    void *temp_r9;

    if (*((u8 *)arg0 + 0x27) == 0)
    {
        CALL_VFUNC(arg0);
        func_0014D528(arg0);

        temp_r9 = (char *)arg1 + 0x5D0;
        if (*((s8 *)temp_r9 + 0xDE) & ~arg4)
        {
            temp_sl = func_0011EE70(temp_r9, (char *)arg0 + 0x34, arg2, 2, 1);
            var_r0 = func_0011EE70(temp_r9, (char *)arg0 + 0x80, arg2, 3, 1) & temp_sl;
        }
        else
        {
            var_r0 = func_0011EE70(temp_r9, (char *)arg0 + 0x34, arg2, 2, 1);
        }

        if (var_r0 != 0 && func_00120ABC(arg0, arg2, 0x1000, arg3, 0, -2) != 0)
        {
            *(void **)((char *)arg0 + 0x28) = arg1;
            *(s32 *)((char *)arg0 + 0x2C) = *arg2;
            func_0014D534(arg0);
            return 1;
        }

        func_0014D534(arg0);
        CALL_VFUNC(arg0);
    }
    return 0;
}