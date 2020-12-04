import Capture.capture as cap
from Epan.data import Data
import threading
import Capture.packets
import time

packets=[]

def print_packet(packet):

    data = Data(packet)

    print('\n#### New Packet ####')
    print(packet.sourceIP)
    print(packet.destIP)
    print(packet.vers)
    print(packet.protocol)
    print(packet.len)
    print(packet.headerLen)
    if(packet.protocol=="UDP"):
        print("\nUDP INFO: \n")
    elif(packet.protocol=="TCP"):
        print("\nTCP INFO: ")
        print(packet.flags)

    print(packet.offset)
    print(packet.srcPort)
    print(packet.destPort)
    print(packet.seqNum)
    print(data.payload)


def capture():
    threading._start_new_thread(cap.capture, (), {"apply":print_packet})
    while True:
        continue
capture()
