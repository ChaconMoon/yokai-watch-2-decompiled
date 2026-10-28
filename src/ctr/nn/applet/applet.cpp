#include <ctr/applet.h>

namespace nn
{
namespace applet
{
        namespace CTR
        {
                /**
                 * @brief Checks whether the currently running CTR title is a standard application.
                 * @address 0x001284E4
                 *
                 * Reads the title type attribute from g_AppletState_00814E00.attribute (offset 0x18).
                 * In the CTR-SDK, a title attribute masked with 7 equal to 0 indicates a standard
                 * retail application (as opposed to an applet, system module, or daemon).
                 *
                 * @return true if the current title is an application, false otherwise.
                 */
                bool IsApplication()
                {
                        if ((detail::g_AppletState_00814E00.attribute & 7) != 0) {
                                return false;
                        }
                        return true;
                }
        }

        namespace detail
        {
                /**
                 * @brief Registers callback slot 3 and its user context argument.
                 * @address 0x00128544
                 *
                 * @param callback Pointer to the notification callback function (stored at offset 0x2C).
                 * @param arg User context pointer passed to callback (stored at offset 0x6C).
                 */
                void SetNotificationCallback(void *callback, void *arg)
                {
                        g_AppletState_00815CA0.callbacks[3] = callback;
                        g_AppletState_00815CA0.callback_args[3] = arg;
                }

                /**
                 * @brief Stores the given 32-bit state value into unk_10 (offset 0x10).
                 * @address 0x00128558
                 *
                 * @param[in] val The new 32-bit state value.
                 */
                void SetState10(u32 val)
                {
                        g_AppletState_00814E00.unk_10 = val;
                }

                /**
                 * @brief Reads and returns the 8-bit unsigned value at offset 0x0C from g_AppletState_00814E00.
                 * @address 0x00128568
                 *
                 * @return u8 The state byte at offset 0x0C.
                 */
                u8 GetState0C()
                {
                        return g_AppletState_00814E00.unk_0C;
                }

                /**
                 * @brief Stores the given 8-bit unsigned value into g_AppletState_00814E00.unk_0C (offset 0x0C).
                 * @address 0x00128578
                 *
                 * @param[in] val The new state byte to store.
                 */
                void SetState0C(u8 val)
                {
                        g_AppletState_00814E00.unk_0C = val;
                }

                /**
                 * @brief Registers callback slot 0 and its user context argument.
                 * @address 0x00128588
                 *
                 * @param callback Pointer to the sleep callback function (stored at offset 0x20).
                 * @param arg User context pointer passed to callback (stored at offset 0x60).
                 */
                void SetSleepCallback(void *callback, void *arg)
                {
                        g_AppletState_00815CA0.callbacks[0] = callback;
                        g_AppletState_00815CA0.callback_args[0] = arg;
                }

                /**
                 * @brief Sets the signed state byte at offset 0x08 of g_AppletState_00814E00 to 1.
                 * @address 0x0012859C
                 */
                void SetState08_1()
                {
                        g_AppletState_00814E00.unk_08 = 1;
                }

                /**
                 * @brief Returns the signed 8-bit state value from g_AppletState_00814E00.unk_08 (offset 0x08).
                 * @address 0x001285B0
                 *
                 * @return s8 The signed state byte at offset 0x08.
                 */
                s8 GetState08()
                {
                        return g_AppletState_00814E00.unk_08;
                }

                /**
                 * @brief Registers callback slot 1 and its user context argument.
                 * @address 0x001285C0
                 *
                 * @param callback Pointer to the awake callback function (stored at offset 0x24).
                 * @param arg User context pointer passed to callback (stored at offset 0x64).
                 */
                void SetAwakeCallback(void *callback, void *arg)
                {
                        g_AppletState_00815CA0.callbacks[1] = callback;
                        g_AppletState_00815CA0.callback_args[1] = arg;
                }

                /**
                 * @brief Resets the signed state byte at offset 0x08 of g_AppletState_00814E00 to 0.
                 * @address 0x001285D4
                 */
                void SetState08_0()
                {
                        g_AppletState_00814E00.unk_08 = 0;
                }

                /**
                 * @brief Reads and returns the 8-bit unsigned value at offset 0x0B from g_AppletState_00814E00.
                 * @address 0x001285E8
                 *
                 * @return u8 The state byte at offset 0x0B.
                 */
                u8 GetState0B()
                {
                        return g_AppletState_00814E00.unk_0B;
                }

                /**
                 * @brief Stores the given 8-bit unsigned value into g_AppletState_00814E00.unk_0B (offset 0x0B).
                 * @address 0x001285F8
                 *
                 * @param[in] val The new state byte to store.
                 */
                void SetState0B(u8 val)
                {
                        g_AppletState_00814E00.unk_0B = val;
                }

                /**
                 * @brief Returns the signed 8-bit state value from g_AppletState_00814E00.unk_0D (offset 0x0D).
                 * @address 0x00128608
                 *
                 * @return s8 The signed state byte at offset 0x0D.
                 */
                s8 GetState0D()
                {
                        return g_AppletState_00814E00.unk_0D;
                }

                /**
                 * @brief Stores the given signed 8-bit value into g_AppletState_00814E00.unk_0D (offset 0x0D).
                 * @address 0x00128618
                 *
                 * @param[in] val The new state byte to store.
                 */
                void SetState0D(s8 val)
                {
                        g_AppletState_00814E00.unk_0D = val;
                }

                /**
                 * @brief Sets the signed state byte at offset 0x07 of g_AppletState_00814E00 to 1.
                 * @address 0x00128628
                 */
                void SetState07_1()
                {
                        g_AppletState_00814E00.unk_07 = 1;
                }

                /**
                 * @brief Returns the signed 8-bit state value from g_AppletState_00814E00.unk_07 (offset 0x07).
                 * @address 0x0012863C
                 *
                 * @return s8 The signed state byte at offset 0x07.
                 */
                s8 GetState07()
                {
                        return g_AppletState_00814E00.unk_07;
                }

                /**
                 * @brief Resets the signed state byte at offset 0x07 of g_AppletState_00814E00 to 0.
                 * @address 0x0012864C
                 */
                void SetState07_0()
                {
                        g_AppletState_00814E00.unk_07 = 0;
                }
        }
}
}
