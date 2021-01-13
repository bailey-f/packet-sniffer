import Capture.capture as capture
import Epan.data as data
import time
import threading
import Capture.packets as packets
from GUI import userinterface as ui
import json

class Application():

    def __init__(self):
        # create UI and any widgets that interact with capturing
        self.ui = ui.UserInterface()
        self.data = data
        self.allpackets = []
        self.capture = capture.Capture(apply=self.register_packet)
        self.ui.add_toolbar_command("Start Capture", self._startCap)
        self.ui.add_toolbar_command("Stop Capture", self._stopCap)
        self.ui.add_button_command("Start Capture", self._startCap)
        self.ui.add_button_command("Stop Capture", self._stopCap)
        self.ui.add_toolbar_command("Save Captures", self._saveCap)
        self.ui.add_toolbar_command("Load Captures", self._loadCap)
        self.ui.add_button_command("Save Captures", self._saveCap)
        self.ui.add_button_command("Load Captures", self._loadCap)
        self.ui.render()

    def _startCap(self):
        self.capture.start()
        self.ui.statusbar.changeStatus("Capturing packets...")

    def _stopCap(self):
        self.capture.stop()
        self.ui.statusbar.changeStatus("Doing nothing...")

    def register_packet(self, packet):
        self.currentpacket = packet
        self.ui.register_packet(packet)
        self.allpackets = self.ui.packetframe.packets
        # do other shnizzle

    def _saveCap(self):
        self.ui.pop_message("File Saved", "File " + str(self.data.Data(
            self.allpackets).createFile(self.allpackets)) + " successfully created.")

    def _loadCap(self):
        print(bytes(self.currentpacket.raw_data))
        fn = self.ui.controlframe.loadPackets()
        data = self.data.Data(None).loadFile(fn)
        for i in range(len(data)):
            self.register_packet(data[i])


# Exec main if this python file is run directly
if __name__ == "__main__":
    app = Application()
