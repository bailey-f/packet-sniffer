import Capture.capture as capture
import time
import threading
from GUI import userinterface as ui


class Application():

    def __init__(self):
        # Create UI
        self.ui = ui.UserInterface()
        self.capture = capture.Capture(apply=self.register_packet)
        self.ui.add_toolbar_command("Start capture", self.capture.start)
        self.ui.packetid=0
        self.ui.add_toolbar_command("Stop capture", self.capture.stop)
        self.ui.render()
        
    
    def register_packet(self, packet):
        time.sleep(0.125)
        self.ui.register_packet(packet)
        # do other shnizzle


# Exec main if this python file is run directly
if __name__ == "__main__":
    app = Application()
