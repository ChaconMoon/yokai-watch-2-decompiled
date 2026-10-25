#include <ctr/nex.h>

namespace nn
{
namespace nex
{
    /**
     * @brief NexElement::operator=
     * @address 0x00340CE8
     * Copies the 32-bit and 16-bit payload fields from another NexElement instance.
     * @param other Source NexElement.
     * @return Reference to this instance.
     */
    NexElement &NexElement::operator=(const NexElement &other)
    {
        unk_01 = other.unk_01;
        unk_02 = other.unk_02;
        return *this;
    }

    /**
     * @brief NexElement::NexElement (parameterized constructor)
     * @address 0x00340CFC
     * Initializes NexElement with an explicit 32-bit ID/type and a 16-bit flag/index.
     * @param arg1 32-bit identifier or property value.
     * @param arg2 16-bit descriptor or status flag.
     */
    NexElement::NexElement(s32 arg1, s16 arg2)
    {
        unk_01 = arg1;
        unk_02 = arg2;
    }

    /**
     * @brief NexElement::NexElement (default constructor)
     * @address 0x00340D08
     * Zero-initializes all payload fields of the NexElement.
     */
    NexElement::NexElement()
    {
        unk_01 = 0;
        unk_02 = 0;
    }

    /**
     * @brief NexElement::~NexElement (destructor)
     * @address 0x00340D18
     * Trivial leaf destructor for NexElement.
     */
    NexElement::~NexElement()
    {
    }

    /**
     * @brief NexElement::NexElement (copy constructor)
     * @address 0x00340D1C
     * Copies all payload fields from another NexElement instance.
     * @param other Source NexElement to copy.
     */
    NexElement::NexElement(const NexElement &other)
    {
        unk_01 = other.unk_01;
        unk_02 = other.unk_02;
    }
}
}
