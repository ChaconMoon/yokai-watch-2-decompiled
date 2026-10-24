#include <ctr/nex.h>

namespace nn
{
        namespace nex
        {
                // Function 0031F1E8 (Operator asignament for getter of qResult)
                qResult &qResult::operator=(const qResult &other)
                {
                        m_data = other.m_data;

                        return *this;
                }

                // Function 0031F1F4 (default constructor of qResult)
                qResult::qResult() : m_data()
                {
                }
                // Function 0031F204 (Constructor with copy of qResult)
                qResult::qResult(const qResult &other)
                {
                        m_data = other.m_data;
                }

                // Function 0031f210 (Getter / Conversion?)
                u64 qResult::getValue() const
                {
                        return ((u64)m_data.unk_02 << 32) | m_data.unk_01;
                }
        }
}
