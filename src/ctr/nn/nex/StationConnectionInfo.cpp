#include <ctr/nex.h>

namespace nn
{
namespace nex
{
    /**
     * @brief StationConnectionInfo::reset
     * @address 0x00340ECC
     * Resets the station connection state by clearing both fields of the internal
     * NexElement structure and zeroing the connection port.
     */
    void StationConnectionInfo::reset()
    {
        m_element.unk_01 = 0;
        m_element.unk_02 = 0;
        m_port = 0;
    }

    /**
     * @brief StationConnectionInfo::setPort
     * @address 0x00340EAC
     * Sets the network port (offset 0x0C) for this station connection.
     * @param port 16-bit network port number.
     * @return Always returns 0 (success).
     */
    u32 StationConnectionInfo::setPort(u16 port)
    {
        m_port = port;
        return 0;
    }

    /**
     * @brief StationConnectionInfo::setElement
     * @address 0x00340EB8
     * Sets the internal network element by delegating to NexElement::operator=.
     * @param element Reference to the source NexElement.
     * @return Always returns 0 (success).
     */
    u32 StationConnectionInfo::setElement(const NexElement &element)
    {
        m_element = element;
        return 0;
    }

    /**
     * @brief StationConnectionInfo::deserialize
     * @address 0x00340E5C
     * Deserializes station connection information from a binary network buffer.
     * Performs a bounds check to verify the pointer lies within the valid application
     * VMA range [0x00100000, 0x20000000). Deserializes the embedded NexElement at offset
     * 0x04 and reads the 16-bit big-endian port at buffer offset 0x06.
     * @param buf Pointer to the serialized network payload.
     * @return 0 on success, 0xE0E14826 if pointer is invalid, or negative qResult on failure.
     */
    u32 StationConnectionInfo::deserialize(const u8 *buf)
    {
        u32 res = 0xE0E14826;
        if ((u32)buf - 0x00100000 < 0x1FF00000)
        {
            u32 elem_res = func_00340C9C(&m_element, buf);
            if ((elem_res & 0x80000000) != 0)
            {
                return elem_res;
            }
            m_port = func_00341368(buf + 6);
            res = 0;
        }
        return res;
    }

    /**
     * @brief StationConnectionInfo::compare
     * @address 0x00340EE8
     * Performs a three-way comparison between this instance and another StationConnectionInfo.
     * Compares the 64-bit identifier obtained from each instance's NexElement via func_0063A6E8.
     * If equal, breaks ties using the 16-bit port number (m_port).
     * @param other The StationConnectionInfo instance to compare against.
     * @return -1 if this < other, 1 if this > other, or 0 if equal.
     */
    s32 StationConnectionInfo::compare(const StationConnectionInfo &other) const
    {
        s64 a = func_0063A6E8(&m_element);
        s64 b = func_0063A6E8(&other.m_element);
        if (a < b)
        {
            return -1;
        }

        s64 c = func_0063A6E8(&other.m_element);
        s64 d = func_0063A6E8(&m_element);
        if (c < d)
        {
            return 1;
        }

        if (other.m_port > m_port)
        {
            return -1;
        }

        if (other.m_port < m_port)
        {
            return 1;
        }

        return 0;
    }
}
}
