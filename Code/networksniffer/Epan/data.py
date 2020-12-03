
class Data():
    def __init__(self, packet):
        self.packet = packet
        self.payload = self._getPayload()

    def _getPayload(self):
        data = bytes.fromhex(str(self.packet.raw_data[self.packet.dOffset:].decode('utf-16-le')))
        return data