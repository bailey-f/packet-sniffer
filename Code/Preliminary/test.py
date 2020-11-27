import socket
import struct

def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    HOST = socket.gethostbyname(socket.gethostname())
    conn.bind((HOST, 0))
    conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    while True:
        raw_data, addr = conn.recvfrom(65535)
        packet = PacketIP(raw_data)
        if(packet.getProtocol()=="TCP"):
            packet_tcp = PacketTCP(raw_data, packet.getHeaderLen())
        if(packet.getSourceIP()==socket.gethostname() and packet.getDestIP()==socket.gethostname()):
            print('##### Redundant Packet ######')
        else:
            print("##### New Packet ######")
            print("Source: ", packet.getSourceIP()) 
            print("Destination: ", packet.getDestIP()) 
            print("Version: ", packet.getVers())
            print("Total Length: ", packet.getLen())
            print("Header Length: ", packet.getHeaderLen())
            print("Time To Live: ", packet.getTTL())
            print("Protocol: ", packet.getProtocol())
            print("Offset: ", packet_tcp.formatTCPHeader())
            print("Source Port: ", packet_tcp.getSrcPort())
            print("Destination Port: ", packet_tcp.getDestPort())
            print("##### End Packet ######")

class PacketIP:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.sourceIP = []
        self.destIP = []
        self.vers = []
        self.len = 0

    def getSourceIP(self):
        self.sourceIP = (struct.unpack('! 4B', self.raw_data[12:16])[:4])
        return formatIP(self.sourceIP)

    def getDestIP(self):
        self.destIP = (struct.unpack('! 4B', self.raw_data[16:20])[:4])
        return formatIP(self.destIP)

    def getVers(self):
        self.vers = (struct.unpack('! B', self.raw_data[:1])[0] & 240) >> 4 # bitwise AND operation to 111000 to eliminate final 4 bits, then bitwise SHIFT 4 as we want those 4 bits. 
        return self.vers                                                                # (struct denies explicit bit manipulation so we work in bytes THEN manipulate with bits.)

    def getLen(self):
        self.len = int((struct.unpack('! B', self.raw_data[2:3])[0]) << 8) + int((struct.unpack('! B', self.raw_data[3:4])[0]) ) #bitwise SHIFT left 8 as the length takes up two bytes, we want to be adding the 4 bits in the right places (xxx0000)
        #len2 = (struct.unpack('! B', self.raw_data[3:4])[0]) deprecated
        #self.len = int(len1)+int(len2) #adding the integer value of (aaaabbbb) deprecated
        return self.len
    
    def getHeaderLen(self):
        self.headerLen = int((struct.unpack('! B', self.raw_data[:1])[0]) & 15) 
        return self.headerLen
    
    def getTTL(self):
        self.ttl = int((struct.unpack('! B', self.raw_data[8:9])[0]))
        return self.ttl
    
    def getProtocol(self):
        proto = ""
        self.protocol = str((struct.unpack('! B', self.raw_data[9:10])[0]))
        if(self.protocol=="1"):
            proto = "ICMP"
        elif(self.protocol=="6"):
            proto = "TCP"
        elif(self.protocol=="17"):
            proto = "UDP"
        return proto

class PacketTCP(PacketIP):
    def __init__(self, raw_data, ip_header_len):
        self.raw_data = raw_data
        self.ip_header_len = ip_header_len
        self.srcPort = []
        self.destPort = []
        self.seqNum = []
        self.tcp_offset = 0
    
    def formatTCPHeader(self):
        self.tcp_offset = int(self.ip_header_len) * 4 #ipheaderlen is the amount of 32 bit words in the ipheader, this will be the offset in bytes.
        return self.tcp_offset

    def getSrcPort(self):
        self.srcPort = int((struct.unpack('! B', self.raw_data[self.tcp_offset:self.tcp_offset+1])[0]) << 8) + int((struct.unpack('! B', self.raw_data[self.tcp_offset+1:self.tcp_offset+2])[0]))
        return self.srcPort

    def getDestPort(self):
        self.destPort = int((struct.unpack('! B', self.raw_data[self.tcp_offset+2:self.tcp_offset+3])[0]) << 8) + int((struct.unpack('! B', self.raw_data[self.tcp_offset+3:self.tcp_offset+4])[0]))
        return self.destPort



def formatIP(ip):
    temp = []
    for i in ip:
        temp.append(str(i))
    return '.'.join(temp)

main()
