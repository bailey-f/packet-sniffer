import Capture.capture as capture
import time
import threading
from GUI import userinterface as ui


class Application():

    def __init__(self):
        # create UI
        self.ui = ui.UserInterface()
        self.capture = capture.Capture(apply=self.register_packet)
        self.ui.add_toolbar_command("Start capture", self._startCap)
        self.ui.add_toolbar_command("Stop capture", self._stopCap)
        self.ui.render()
        
    def _startCap(self):
        self.capture.start()
        self.ui.statusbar.change_status("Capturing packets...")
    def _stopCap(self):
        self.capture.stop()
        self.ui.statusbar.change_status("Doing nothing...")
    def register_packet(self, packet):
        self.ui.register_packet(packet)
        # do other shnizzle


# Exec main if this python file is run directly
if __name__ == "__main__":
    app = Application()
