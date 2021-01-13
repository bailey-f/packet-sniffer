import socket
import struct
import threading
import json
import datetime
import Capture.packets as packets
import os
from binascii import unhexlify


class Data():
    def __init__(self, packets):
        self.date = datetime.datetime.now().strftime('%d %b')
    
    def createFile(self, packets):
        # make a path for the new folder
        self.date = datetime.datetime.now().strftime('%d %b')
        self.directory = str(self.date)
        self.parent_dir = "C:/Packet Captures/"
        self.path = os.path.join(self.parent_dir, self.directory)

        try:
            os.mkdir(self.path)
        except:
            pass

        self.n = len([name for name in os.listdir(self.path)])
        self.file_path = self.path + "/" + "Capture" + str(self.n) + ".json"
        # count number of files already in directory and therefore new file name
        print(str(self.n+1) + " files already in directory")

        # make a path for the new file
        print("file " + str(self.file_path) + " made")

        # json dump the contents
        with open(self.file_path, 'a') as f:
            for i in range(len(packets)):
                f.write(packets[i].get_json() + "\n")
            f.close()

        return str(self.file_path)

    def loadFile(self, file):
        data_list = []
        for line in file:
            normalline = (self.get_normal(line))
            newPacket = packets.Packet(normalline)
            if(newPacket.protocol=="TCP"):
                data_list.append(packets.TCPPacket(normalline))
            elif(newPacket.protocol=="UDP"):
                data_list.append(packets.UDPPacket(normalline))
            else:
                print("Packet not initialised. ERROR")
        file.close()
        return data_list

    #def loadFile(self):
    #    pass
    def get_normal(self, rdata):
        rdata = rdata[1:(len(rdata)-2)]
        rdata = rdata.strip()
        bytesr = bytes.fromhex(rdata)
        return bytesr

        '''
        data2 = []
        n = 2
        try:
            for i in range(0, len(str(rdata)), n):
                byte = rdata[i:i + n]
                data.append(byte)
            for i in range(0, len(data)):
                try:
                    if(data[i] == ""):
                        data[i] = ".."
                    else:
                        data[i] = bytes.fromhex(data[i])
                        print(data[i])
                        data2.append(data[i])
                except:
                    pass
                    data[i] = ".."
        except:
            pass
            data = ".."
        return b''.join(data2)'''