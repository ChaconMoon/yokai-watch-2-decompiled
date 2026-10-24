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
        }
}
