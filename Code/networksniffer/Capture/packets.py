import struct

class Packet():
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.sourceIP = self._getSourceIP()
        self.destIP = self._getDestIP()
        self.vers = self._getVers()
        self.len = self._getLen()
        self.headerLen = self._getHeaderLen()
        self.protocol = self._getProtocol()

    def _formatIP(self, ip):
        temp = []
        for i in ip:
            temp.append(str(i))
        return '.'.join(temp)

    def _getSourceIP(self):
        sourceIP = (struct.unpack('! 4B', self.raw_data[12:16])[:4])
        return self._formatIP(sourceIP)

    def _getDestIP(self):
        destIP = (struct.unpack('! 4B', self.raw_data[16:20])[:4])
        return self._formatIP(destIP)

    def _getVers(self):
        return int((struct.unpack('! B', self.raw_data[:1])[0] & 240) >> 4) # bitwise AND operation to 111000 to eliminate final 4 bits, then bitwise SHIFT 4 as we want those 4 bits. 

    def _getLen(self):
        return int((struct.unpack('! B', self.raw_data[2:3])[0]) << 8) + int((struct.unpack('! B', self.raw_data[3:4])[0]) ) #bitwise SHIFT left 8 as the length takes up two bytes, we want to be adding the 4 bits in the right places (xxx0000)
    
    def _getHeaderLen(self):
        return int((struct.unpack('! B', self.raw_data[:1])[0]) & 15) 
    
    def _getTTL(self):
        return int((struct.unpack('! B', self.raw_data[8:9])[0]))
    
    def _getProtocol(self):
        proto = ""
        self.protocol = str((struct.unpack('! B', self.raw_data[9:10])[0]))
        if(self.protocol=="1"):
            proto = "ICMP"
        elif(self.protocol=="6"):
            proto = "TCP"
        elif(self.protocol=="17"):
            proto = "UDP"
        return proto

class TCPPacket(Packet):
    def __init__(self, raw_data):
        super().__init__(raw_data)
        self.offset = int(self.headerLen) * 4
        self.srcPort = self._getSrcPort()
        self.destPort = self._getDestPort()
        self.seqNum = self._getSequenceNum()

    def _getSrcPort(self):
        return int((struct.unpack('! B', self.raw_data[self.offset:self.offset+1])[0]) << 8) + int((struct.unpack('! B', self.raw_data[self.offset+1:self.offset+2])[0]))
        
    def _getDestPort(self):
        return int((struct.unpack('! B', self.raw_data[self.offset+2:self.offset+3])[0]) << 8) + int((struct.unpack('! B', self.raw_data[self.offset+3:self.offset+4])[0]))

    def _getSequenceNum(self):
        return int( ( struct.unpack('! B', self.raw_data[self.offset+4:self.offset+5])[0] ) << 24 ) + int( (struct.unpack('! B', self.raw_data[self.offset+5:self.offset+6])[0] ) << 16 ) + int( (struct.unpack('! B', self.raw_data[self.offset+6:self.offset+7])[0] ) << 8) + int( (struct.unpack('! B', self.raw_data[self.offset+7:self.offset+8])[0] ) )

class UDPPacket(Packet):
    def __init__(self, raw_data):
        super().__init__(raw_data)
        self.offset = int(self.headerLen) * 4
        self.srcPort = self._getSrcPort()
        self.destPort = self._getDestPort()
        self.seqNum = self._getSequenceNum()

    def _getSrcPort(self):
        return int((struct.unpack('! B', self.raw_data[self.offset:self.offset+1])[0]) << 8) + int((struct.unpack('! B', self.raw_data[self.offset+1:self.offset+2])[0]))
        
    def _getDestPort(self):
        return int((struct.unpack('! B', self.raw_data[self.offset+2:self.offset+3])[0]) << 8) + int((struct.unpack('! B', self.raw_data[self.offset+3:self.offset+4])[0]))
    
    def _getSequenceNum(self):
        return int( ( struct.unpack('! B', self.raw_data[self.offset+4:self.offset+5])[0] ) << 24 ) + int( (struct.unpack('! B', self.raw_data[self.offset+5:self.offset+6])[0] ) << 16 ) + int( (struct.unpack('! B', self.raw_data[self.offset+6:self.offset+7])[0] ) << 8) + int( (struct.unpack('! B', self.raw_data[self.offset+7:self.offset+8])[0] ) )
