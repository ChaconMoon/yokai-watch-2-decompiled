#include <ctr/nex.h>

namespace nn
{
        namespace nex
        {
                // Function 00340ECC (Resest connection and sets all values at zero)
                void StationConnectionInfo::reset()
                {
                        m_element.unk_01 = 0;
                        m_element.unk_02 = 0;
                        m_port = 0;
                }
                // Function 00340EAC (set Port)
                u32 StationConnectionInfo::setPort(u16 port)
                {
                        m_port = port;
                        return 0;
                }
                // Function 00340EB8 (set Element of the connection)
                u32 StationConnectionInfo::setElement(const NexElement &element)
                {
                        m_element = element;
                        return 0;
                }
                // Function 00340E5C (deserialize object)
                u32 StationConnectionInfo::deserialize(const u8 *buf)
                {
                        s32 result_code = 0xE0E14826;
                        if ((u32)(buf - 0x00100000) < 0x1FF00000u)
                        {

                                result_code = func_00340C9C(&m_element, buf);
                                if ((result_code & 0x80000000) == 0)
                                {
                                        m_port = func_00341368(buf + 6);
                                        result_code = 0;
                                }
                        }
                        return result_code;
                }

                // Function 00340EE8 (Three-way comparison returning -1, 0, or 1)
                s32 StationConnectionInfo::compare(const StationConnectionInfo &other) const
                {
                        if (func_0063A6E8(&m_element) < func_0063A6E8(&other.m_element))
                        {
                                return -1;
                        }

                        if (func_0063A6E8(&other.m_element) < func_0063A6E8(&m_element))
                        {
                                return 1;
                        }

                        if (m_port < other.m_port)
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
