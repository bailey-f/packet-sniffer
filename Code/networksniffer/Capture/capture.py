import socket
import struct
from Epan import packets
import threading


class Capture():

    def __init__(self, host=socket.gethostbyname(socket.gethostname()), port=0, apply=None):
        print(socket.gethostbyname(socket.gethostname()))
        self.host = host
        self.port = port
        self.apply = apply
        self.running = False

        self.conn = socket.socket(
            socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        self.conn.bind((self.host, self.port))
        self.conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        self.conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self.running = False

    def _loop(self):
        while self.running:
            raw_data, _ = self.conn.recvfrom(65535)
            packet = packets.Packet(raw_data)
            if(packet.protocol == "TCP"):
                packet_spec = packets.TCPPacket(raw_data)
            elif(packet.protocol == "UDP"):
                packet_spec = packets.UDPPacket(raw_data)
            if (self.apply):
                self.apply(packet_spec)
