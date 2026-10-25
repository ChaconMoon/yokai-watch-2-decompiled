#include <ctr/nex.h>

namespace nn
{
namespace nex
{
    /**
     * @brief qResult::operator=
     * @address 0x0031F1E8
     * Assigns the underlying NexElement status data from another qResult.
     * @param other Source qResult.
     * @return Reference to this instance.
     */
    qResult &qResult::operator=(const qResult &other)
    {
        m_data = other.m_data;
        return *this;
    }

    /**
     * @brief qResult::qResult (default constructor)
     * @address 0x0031F1F4
     * Initializes a qResult instance with default-constructed status data.
     */
    qResult::qResult() : m_data()
    {
    }

    /**
     * @brief qResult::qResult (copy constructor)
     * @address 0x0031F204
     * Copies status data from an existing qResult instance.
     * @param other Source qResult to copy.
     */
    qResult::qResult(const qResult &other)
    {
        m_data = other.m_data;
    }

    /**
     * @brief qResult::getValue
     * @address 0x0031F210
     * Reconstructs the full 64-bit status value by combining the high 32-bit word
     * and the low 32-bit word.
     * @return 64-bit integer combining high and low result fields.
     */
    u64 qResult::getValue() const
    {
        return ((u64)m_data.unk_02 << 32) | m_data.unk_01;
    }
}
}
