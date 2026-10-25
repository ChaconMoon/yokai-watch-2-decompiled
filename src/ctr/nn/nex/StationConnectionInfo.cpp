#include <ctr/nex.h>

namespace nn
{
namespace nex
{
    void StationConnectionInfo::reset()
    {
        m_element.unk_01 = 0;
        m_element.unk_02 = 0;
        m_port = 0;
    }

    u32 StationConnectionInfo::setPort(u16 port)
    {
        m_port = port;
        return 0;
    }

    u32 StationConnectionInfo::setElement(const NexElement &element)
    {
        m_element = element;
        return 0;
    }

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
