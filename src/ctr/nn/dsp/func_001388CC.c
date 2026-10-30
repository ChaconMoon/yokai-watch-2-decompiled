#include <ctr/dsp.h>

/**
 * @brief func_001388CC
 * @address 0x001388CC
 * nn::dsp bounded string length (strnlen)
 *
 * Computes the length of a null-terminated string up to a maximum length.
 *
 * @param str Input string.
 * @param max_len Maximum length boundary.
 * @return u32 Length of string (index of null terminator or max_len).
 */
u32 func_001388CC(const char *str, u32 max_len)
{
        u32 i = 0;

        while (1)
        {
                if (str[i] == '\0' || max_len <= i)
                {
                        break;
                }
                i++;
        }

        return i;
}
