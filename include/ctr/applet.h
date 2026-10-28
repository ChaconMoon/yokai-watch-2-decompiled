#ifndef CTR_APPLET_H
#define CTR_APPLET_H

#include "types.h"

#ifndef __cplusplus
#ifndef __bool_true_false_are_defined
typedef unsigned char bool;
#define true 1
#define false 0
#define __bool_true_false_are_defined 1
#endif
#endif

#ifdef __cplusplus

namespace nn
{
        namespace applet
        {
                namespace CTR
                {
                        /**
                         * @brief Checks whether the currently running CTR title is a standard application.
                         */
                        bool IsApplication();
                }

                namespace detail
                {
                        typedef void (*CallbackFn)(void *arg);

                        /**
                         * @brief Registers callback slot 3 and its user context argument (0x00128544).
                         */
                        void SetNotificationCallback(void *callback, void *arg);

                        /**
                         * @brief Stores the given 32-bit state value into unk_10 (0x00128558).
                         */
                        void SetState10(u32 val);

                        /**
                         * @brief Reads the 8-bit unsigned state value at offset 0x0C (0x00128568).
                         */
                        u8 GetState0C();

                        /**
                         * @brief Stores an 8-bit unsigned state value at offset 0x0C (0x00128578).
                         */
                        void SetState0C(u8 val);

                        /**
                         * @brief Registers the sleep transition callback and context argument (0x00128588).
                         */
                        void SetSleepCallback(void *callback, void *arg);

                        /**
                         * @brief Sets the signed state byte at offset 0x08 to 1 (0x0012859C).
                         */
                        void SetState08_1();

                        /**
                         * @brief Reads the signed 8-bit state value at offset 0x08 (0x001285B0).
                         */
                        s8 GetState08();

                        /**
                         * @brief Registers the awake transition callback and context argument (0x001285C0).
                         */
                        void SetAwakeCallback(void *callback, void *arg);

                        /**
                         * @brief Resets the signed state byte at offset 0x08 to 0 (0x001285D4).
                         */
                        void SetState08_0();

                        /**
                         * @brief Reads the 8-bit unsigned state value at offset 0x0B (0x001285E8).
                         */
                        u8 GetState0B();

                        /**
                         * @brief Stores an 8-bit unsigned state value at offset 0x0B (0x001285F8).
                         */
                        void SetState0B(u8 val);

                        /**
                         * @brief Reads the signed 8-bit state value at offset 0x0D (0x00128608).
                         */
                        s8 GetState0D();

                        /**
                         * @brief Stores a signed 8-bit state value at offset 0x0D (0x00128618).
                         */
                        void SetState0D(s8 val);

                        /**
                         * @brief Sets the signed state byte at offset 0x07 to 1 (0x00128628).
                         */
                        void SetState07_1();

                        /**
                         * @brief Reads the signed 8-bit state value at offset 0x07 (0x0012863C).
                         */
                        s8 GetState07();

                        /**
                         * @brief Resets the signed state byte at offset 0x07 to 0 (0x0012864C).
                         */
                        void SetState07_0();

                        /**
                         * @brief Applet system callbacks and context registration structure (0x00815CA0).
                         */
                        class AppletContext
                        {
                        public:
                                s8 GetStatusByte() const { return unk_00; }

                        public:
                                s8 unk_00;              /* 0x00: Leído por func_00138A80 (nn::dsp) */
                                u8 pad_01[0x1F];        /* 0x01 - 0x1F */
                                void *callbacks[4];     /* 0x20 - 0x2F: Callbacks (0x20, 0x24, 0x28, 0x2C) */
                                u8 pad_30[0x30];        /* 0x30 - 0x5F */
                                void *callback_args[4]; /* 0x60 - 0x6F: Argumentos de contexto (0x60, 0x64, 0x68, 0x6C) */
                        };

                        /**
                         * @brief Global applet state and attribute structure (0x00814E00).
                         */
                        class AppletState
                        {
                        public:
                                /* Offset 0x18: Atributos */
                                bool IsApplication() const { return (attribute & 0x07) == 0; }

                        public:
                                u8 pad_00[0x07]; /* 0x00 - 0x06 */
                                s8 unk_07;       /* 0x07: Estado con signo */
                                s8 unk_08;       /* 0x08: Estado con signo */
                                u8 pad_09[0x02]; /* 0x09 - 0x0A */
                                u8 unk_0B;       /* 0x0B: Byte de estado */
                                u8 unk_0C;       /* 0x0C: Byte de estado */
                                s8 unk_0D;       /* 0x0D: Byte de estado con signo */
                                u8 pad_0E[0x02]; /* 0x0E - 0x0F */
                                u32 unk_10;      /* 0x10: Leído por nn::dsp */
                                u32 unk_14;      /* 0x14: Usado por LFW */
                                u32 attribute;   /* 0x18: Atributo de tipo de título */
                        };
                }
        }
}

extern "C"
{
        extern nn::applet::detail::AppletContext g_AppletState_00815CA0;
        extern nn::applet::detail::AppletState g_AppletState_00814E00;
}

namespace nn
{
        namespace applet
        {
                namespace detail
                {
                        using ::g_AppletState_00814E00;
                        using ::g_AppletState_00815CA0;
                }
        }
}

using nn::applet::detail::AppletContext;
using nn::applet::detail::AppletState;

#else /* !__cplusplus (Pure C) */

typedef struct AppletState
{
        u8 pad_00[0x07];
        s8 unk_07;
        s8 unk_08;
        u8 pad_09[0x02];
        u8 unk_0B;
        u8 unk_0C;
        s8 unk_0D;
        u8 pad_0E[0x02];
        u32 unk_10;
        u32 unk_14;
        u32 attribute;
} AppletState;

typedef struct AppletContext
{
        s8 unk_00;
        u8 pad_01[0x1F];
        void *callbacks[4];
        u8 pad_30[0x30];
        void *callback_args[4];
} AppletContext;

extern AppletState g_AppletState_00814E00;
extern AppletContext g_AppletState_00815CA0;

#endif /* __cplusplus */

#endif /* CTR_APPLET_H */
