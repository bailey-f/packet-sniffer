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
        vers = (struct.unpack('! B', raw_data[:1])[0] & 240) >> 4
        packet = Packet(raw_data)
        if(packet.getSourceIP()==socket.gethostname() and packet.getDestIP()==socket.gethostname()):
            continue
        print("##### New Packet ######")
        print("Source: ", packet.getSourceIP()) 
        print("Destination: ", packet.getDestIP()) 
        print("Version: ", packet.getVers())
        print("Total Length: ", packet.getLen())
        print("##### End Packet ######")

class Packet:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.sourceIP = []
        self.destIP = []
        self.vers = []
        self.len = 0

    def getSourceIP(self):
        self.sourceIP = (struct.unpack('! 4B', self.raw_data[12:16])[:4])
        temp = []
        for i in self.sourceIP:
            temp.append(str(i))
        return '.'.join(temp)

    def getDestIP(self):
        self.destIP = (struct.unpack('! 4B', self.raw_data[16:20])[:4])
        temp = []
        for i in self.destIP:
            temp.append(str(i))
        return '.'.join(temp)

    def getVers(self):
        self.vers = (struct.unpack('! B', self.raw_data[:1])[0] & 240) >> 4 # bitwise AND operation to 111000 to eliminate final 4 bits, then bitwise SHIFT 4 as we want those 4 bits. 
        return self.vers                                                                # (struct denies explicit bit manipulation so we work in bytes THEN manipulate with bits.)

    def getLen(self):
        self.len = int((struct.unpack('! B', self.raw_data[2:3])[0]) << 4) +    #bitwise SHIFT left 4 as the length takes up two bytes, we want to be adding the 4 bits in the right places (xxx0000)
                 int((struct.unpack('! B', self.raw_data[3:4])[0]) ) 
        #len2 = (struct.unpack('! B', self.raw_data[3:4])[0]) deprecated
        #self.len = int(len1)+int(len2) #adding the integer value of (aaaabbbb) deprecated
        return self.len

main()
