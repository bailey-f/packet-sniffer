import socket
import struct
import threading
import json
import datetime
import os


class Data():
    def __init__(self, packets):
        self.date = datetime.datetime.now().strftime('%d %b')
    
    def createFile(self, packets):
        # make a path for the new folder
        self.date = datetime.datetime.now().strftime('%d %b')
        self.directory = str(self.date)
        self.parent_dir = "C:/Packet Captures/"
        self.path = os.path.join(self.parent_dir, self.directory)
        self.n = len([name for name in os.listdir(self.path)])
        self.file_path = self.path + "/" + "Capture" + str(self.n) + ".json"

        try:
            os.mkdir(self.path)
        except:
            pass

        # count number of files already in directory and therefore new file name
        print(str(self.n+1) + " files already in directory")

        # make a path for the new file
        print("file " + str(self.file_path) + " made")

        # json dump the contents
        with open(self.file_path, 'a') as f:
            for i in range(len(packets)):
                f.write(packets[i].get_json())
            f.close()

        return str(self.file_path)

    #def loadFile(self):
    #    pass
