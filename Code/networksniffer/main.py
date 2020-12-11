import Capture.capture as cap
import threading
import time
from GUI import userinterface as ui


class Application():

    def __init__(self):
        # Create UI
        self.ui = ui.UserInterface()
        self.ui.add_toolbar_command("Start capture", self.start_capture)
        
    
    def start(self):
        while True:
            self.ui.render()
    
    def start_capture(self):
        threading._start_new_thread(cap.capture, (), {"apply":self.register_packet})
    
    def register_packet(self, packet):
        self.ui.register_packet(packet)
        # do other shnizzle

    
# Exec main if this python file is run directly
if __name__ == "__main__":
    app = Application()
    app.start()
