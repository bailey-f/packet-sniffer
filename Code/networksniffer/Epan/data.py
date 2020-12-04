class Data():
    def __init__(self, packet):
        self.packet = packet
        self.payload = self._getPayload()

    def _getPayload(self):
        data = str(self.packet.raw_data[self.packet.dOffset:].decode('unicode_escape'))
        return data