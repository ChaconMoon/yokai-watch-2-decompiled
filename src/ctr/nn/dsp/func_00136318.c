#include <ctr/dsp.h>

/**
 * @brief func_00136318
 * @address 0x00136318
 * nn::dsp struct header initializer.
 * Sets the magic identifier (0xE7E3FFFF) and clears the status field to 0.
 *
 * @param[out] header Pointer to the DSP header structure to initialize
 */
void func_00136318(DspHeader_00136318 *header)
{
        header->magic = 0xE7E3FFFF;
        header->status = 0;
}
