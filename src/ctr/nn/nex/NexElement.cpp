#include <ctr/nex.h>

// NexElement getter
namespace nn
{
        namespace nex
        {
                // Function 00340CE8 (Operator asignament for getter of NexElement)
                NexElement &NexElement::operator=(const NexElement &other)
                {
                        unk_01 = other.unk_01;
                        unk_02 = other.unk_02;
                        return *this;
                }

                // Function 00340CFC (Constructor with params of NexElement)
                NexElement::NexElement(s32 arg1, s16 arg2)
                {
                        unk_01 = arg1;
                        unk_02 = arg2;
                }

                // Function 00340D08 (Constructor of NexElement)
                NexElement::NexElement()
                {
                        unk_01 = 0;
                        unk_02 = 0;
                }

                // Function 00340D18 (Destructor of NexElement)
                NexElement::~NexElement()
                {
                }

                // Function 00340D1C (Constructor with copy of NexElement)
                NexElement::NexElement(const NexElement &other)
                {
                        unk_01 = other.unk_01;
                        unk_02 = other.unk_02;
                }
        }
}