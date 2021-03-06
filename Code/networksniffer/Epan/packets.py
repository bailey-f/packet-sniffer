import struct
import json


class PacketEncoder(json.JSONEncoder):
    def default(self, o):
        return {}


class Packet():
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.decdata = self._getDecData()
        self.sourceIP = self._getSourceIP()
        self.destIP = self._getDestIP()
        self.vers = self._getVers()
        self.len = self._getLen()
        self.headerLen = self._getHeaderLen()
        self.protocol = self._getProtocol()
        self.offset = int(self.headerLen) * 4
        self.ttl = self._getTTL()
        self.payload = None

    def get_json(self):
        return json.dumps(self.decdata)

    def _formatIP(self, ip):
        temp = []
        for i in ip:
            temp.append(str(i))
        return '.'.join(temp)

    def _getDecData(self):
        data = []
        n = 2
        try:
            for i in range(0, len(str(self.raw_data)), n):
                byte = self.raw_data[i:i + n]
                data.append(byte)
            for i in range(0, len(data)):
                try:
                    if(data[i] == ""):
                        data[i] = ".."
                    else:
                        data[i] = data[i].hex()
                except:
                    pass
                    data[i] = ".."
        except:
            pass
            data = ".."
        return "".join(data)

    def _getSourceIP(self):
        sourceIP = (struct.unpack('! 4B', self.raw_data[12:16])[:4])
        return self._formatIP(sourceIP)

    def _getDestIP(self):
        destIP = (struct.unpack('! 4B', self.raw_data[16:20])[:4])
        return self._formatIP(destIP)

    def _getVers(self):
        # bitwise AND operation to 111000 to eliminate final 4 bits, then bitwise SHIFT 4 as we want those 4 bits.
        return int((struct.unpack('! B', self.raw_data[:1])[0] & 240) >> 4)

    def _getLen(self):
        # bitwise SHIFT left 8 as the length takes up two bytes, we want to be adding the 4 bits in the right places (xxx0000)
        return int((struct.unpack('! B', self.raw_data[2:3])[0]) << 8) + int((struct.unpack('! B', self.raw_data[3:4])[0]))

    def _getHeaderLen(self):
        return int((struct.unpack('! B', self.raw_data[:1])[0]) & 15)

    def _getTTL(self):
        return int((struct.unpack('! B', self.raw_data[8:9])[0]))

    def _getProtocol(self):
        proto = ""
        self.protocol = str((struct.unpack('! B', self.raw_data[9:10])[0]))
        if(self.protocol == "1"):
            proto = "ICMP"
        elif(self.protocol == "6"):
            proto = "TCP"
        elif(self.protocol == "17"):
            proto = "UDP"
        return proto


class TCPPacket(Packet):
    def __init__(self, raw_data):
        super().__init__(raw_data)
        self.srcPort = self._getSrcPort()
        self.destPort = self._getDestPort()
        self.seqNum = self._getSequenceNum()
        self.dOffset = self._getTCPHLen()
        self.flags = self._getFlags()
        self.payload = Payload(self)

    def _getSrcPort(self):
        return int((struct.unpack('! B', self.raw_data[self.offset:self.offset+1])[0]) << 8) + int((struct.unpack('! B', self.raw_data[self.offset+1:self.offset+2])[0]))

    def _getDestPort(self):
        return int((struct.unpack('! B', self.raw_data[self.offset+2:self.offset+3])[0]) << 8) + int((struct.unpack('! B', self.raw_data[self.offset+3:self.offset+4])[0]))

    def _getSequenceNum(self):
        return int((struct.unpack('! B', self.raw_data[self.offset+4:self.offset+5])[0]) << 24) + int((struct.unpack('! B', self.raw_data[self.offset+5:self.offset+6])[0]) << 16) + int((struct.unpack('! B', self.raw_data[self.offset+6:self.offset+7])[0]) << 8) + int((struct.unpack('! B', self.raw_data[self.offset+7:self.offset+8])[0]))

    def _getTCPHLen(self):
        return int((struct.unpack('! B', self.raw_data[self.offset+12:self.offset+13])[0] & 240) >> 4)

    def _getFlags(self):
        offset_reserved_flags = int(
            (struct.unpack('! B', self.raw_data[self.offset+13:self.offset+14])[0]))
        flag_urg = offset_reserved_flags & 32 >> 5
        flag_ack = offset_reserved_flags & 16 >> 4
        flag_psh = offset_reserved_flags & 8 >> 3
        flag_rst = offset_reserved_flags & 4 >> 2
        flag_syn = offset_reserved_flags & 2 >> 1
        flag_fin = offset_reserved_flags & 1
        return " ".join(("URG:", str(flag_urg))), " ".join(("ACK:", str(flag_ack))), " ".join(("PSH:", str(flag_psh))), " ".join(("RST:", str(flag_rst))), " ".join(("SYN:", str(flag_syn))), " ".join(("FIN:", str(flag_fin)))


class UDPPacket(Packet):
    def __init__(self, raw_data):
        super().__init__(raw_data)
        self.srcPort = self._getSrcPort()
        self.destPort = self._getDestPort()
        self.seqNum = self._getSequenceNum()
        self.dOffset = self._getUDPHLen()
        self.payload = Payload(self)

    def _getSrcPort(self):
        return int((struct.unpack('! B', self.raw_data[self.offset:self.offset+1])[0]) << 8) + int((struct.unpack('! B', self.raw_data[self.offset+1:self.offset+2])[0]))

    def _getDestPort(self):
        return int((struct.unpack('! B', self.raw_data[self.offset+2:self.offset+3])[0]) << 8) + int((struct.unpack('! B', self.raw_data[self.offset+3:self.offset+4])[0]))

    def _getSequenceNum(self):
        return int((struct.unpack('! B', self.raw_data[self.offset+4:self.offset+5])[0]) << 24) + int((struct.unpack('! B', self.raw_data[self.offset+5:self.offset+6])[0]) << 16) + int((struct.unpack('! B', self.raw_data[self.offset+6:self.offset+7])[0]) << 8) + int((struct.unpack('! B', self.raw_data[self.offset+7:self.offset+8])[0]))

    def _getUDPHLen(self):
        return int((struct.unpack('! B', self.raw_data[self.offset+12:self.offset+13])[0] & 240) >> 4)


class Payload():
    def __init__(self, packet):
        self.payloaddata = packet.raw_data[packet.dOffset:]
        self.decdata = self._getDecData()
        self.data = self._getData()

    def _getDecData(self):
        data = []
        n = 2
        try:
            for i in range(0, len(str(self.payloaddata)), n):
                byte = self.payloaddata[i:i + n]
                data.append(byte)
            for i in range(0, len(data)):
                try:
                    data[i] = data[i].decode('unicode_escape')
                except:
                    pass
                    data[i] = ".."
        except:
            pass
            data = ".."

        return data

    def _getData(self):
        data = []
        n = 2
        try:
            for i in range(0, len(str(self.payloaddata)), n):
                byte = self.payloaddata[i:i + n]
                data.append(byte)
            for i in range(0, len(data)):
                try:
                    if(data[i] == ""):
                        data[i] = ".."
                    else:
                        data[i] = data[i].hex()
                except:
                    pass
                    data[i] = ".."
        except:
            pass
            data = ".."
        return "".join(data)

