#include <ctr/dsp.h>

/**
 * @brief func_001386D4
 * @address 0x001386D4
 * nn::dsp non-empty string / buffer validation
 *
 * Validates that a string pointer is non-NULL and points to a non-zero character.
 *
 * @param str Input string or byte buffer pointer.
 * @return bool32 TRUE (1) if pointer is non-NULL and *str != 0, FALSE (0) otherwise.
 */
bool32 func_001386D4(const char *str)
{
        bool32 ret = TRUE;

        if (str == NULL || *str == '\0')
        {
                ret = FALSE;
        }

        return ret;
}
