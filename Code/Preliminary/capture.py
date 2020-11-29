import socket
import struct
import packets

def capture(apply=None):
    conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    HOST = socket.gethostbyname(socket.gethostname())
    conn.bind((HOST, 0))
    conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    while True:
        raw_data, _ = conn.recvfrom(65535)
        packet = packets.Packet(raw_data)
        if(packet.protocol == "TCP"):
            packet_spec = packets.TCPPacket(raw_data)
        elif(packet.protocol == "UDP"):
            packet_spec= packets.UDPPacket(raw_data)
        
        if (apply):
            apply(packet_spec)




"""def unpackData(byteAmount, raw_data, offset, bitShift, shiftOp):
    byteAmountF = '! ' + str(byteAmount) + "B"
    print(byteAmount)
    if(byteAmount!=0 and shiftOp=="R"):
        data = int( (struct.unpack(byteAmountF, raw_data[offset+1:offset+1+byteAmount])[:byteAmount])) >> bitShift
    elif(byteAmount!=0 and shiftOp=="L"):
        data = int( (struct.unpack(byteAmountF, raw_data[offset+1:offset+1+byteAmount])[:byteAmount])) << bitShift
    elif(byteAmount==0 and shiftOp=="R"):
        data = int( (struct.unpack(byteAmountF, raw_data[offset+1:offset+1+byteAmount])[0])) >> bitShift
    elif(byteAmount==0 and shiftOp=="L"):
        data = int( (struct.unpack(byteAmountF, raw_data[offset+1:offset+1+byteAmount])[0])) << bitShift
    else:
        data = "Invalid input."
    return data"""

