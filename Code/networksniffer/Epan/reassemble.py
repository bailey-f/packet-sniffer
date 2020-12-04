import Capture.packets as packets

class Reassemble():
    def __init__(self, packet):
        self.packet = packet
        self.payload = self._ISN()

    def _ISN(self):
        return 0