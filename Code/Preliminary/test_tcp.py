import socket
import struct

def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = socket.gethostbyname(socket.gethostname())
    conn.bind((HOST, 0))
    conn.setsockopt(socket.IPPROTO_TCP, socket.IP_HDRINCL, 1)
    #conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    while True:
        raw_data, addr = conn.recv(1024)
        #vers = (struct.unpack('! B', raw_data[:1])[0] & 240) >> 4
        packet = Packet(raw_data)
        #if(packet.getSourceIP()!=socket.gethostname() and packet.getDestIP()!=socket.gethostname()):
        #    continue
        print("##### New Packet ######")
        print("Source port: ", packet.getSourcePORT()) 
        print("Destination port: ", packet.getDestPORT()) 
        print("Sequence NUM: ", packet.getSequence())
        print("##### End Packet ######")

class Packet:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.sourcePORT = []
        self.destPORT = []
        self.seq = []

    def getSourcePORT(self):
        self.sourcePORT = int((struct.unpack('! 2B', self.raw_data[:1])[0]) << 4) + int((struct.unpack('! 2B', self.raw_data[1:2])[0]))
        return self.sourcePORT
        #temp = []
        #for i in self.sourcePORT:
        #    temp.append(str(i))
        #return '.'.join(temp)


    def getDestPORT(self):
        self.destPORT = int((struct.unpack('! 2B', self.raw_data[2:3])[0]) << 4) + int((struct.unpack('! 2B', self.raw_data[3:4])[0]))
        return self.destPORT
        #temp = []
        #for i in self.destPORT:
        #    temp.append(str(i))
        #return '.'.join(temp)

    def getSequence(self):
        self.seq = (struct.unpack('! B', self.raw_data[:4])[:4]) 
        return self.seq                                                             

main()
