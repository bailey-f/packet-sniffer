import socket
import struct
import textwrap

def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    conn.bind(('localhost', 0))
    conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    while True:
        raw_data, addr = conn.recvfrom(65535)
        vers = (struct.unpack('! B', raw_data[:1])[0] & 240) >> 4
        print(vers) 
        
        if(True):
            continue
main()
