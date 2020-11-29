import Capture.capture as cap
import threading
import Capture.packets
import time

packets=[]

def print_packet(packet):
    packets.append(packet)

def capture():
    threading._start_new_thread(cap.capture, (), {"apply":print_packet})

    while True:
        print(len(packets))
        time.sleep(0.5)

capture()