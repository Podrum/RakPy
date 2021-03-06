from rakpy.utils.InternetAddress import InternetAddress
from rakpy.protocol.Packet import Packet
from rakpy.protocol.PacketIdentifiers import PacketIdentifiers

class ConnectionRequestAccepted(Packet):
    id = PacketIdentifiers.ConnectionRequestAccepted
    
    clientAddress = InternetAddress("127.0.0.1", 0, 4)
    systemIndex = 0
    systemAddresses = []
    requestTime = 0
    time = 0
    
    def encodePayload(self):
        self.putAddress(self.clientAddress)
        self.putShort(self.systemIndex)
        i = 0
        while i < 10:
            self.putAddress(self.systemAddresses[i] if len(self.systemAddresses) > i else InternetAddress("127.0.0.1", 0, 4))
            i += 1
        self.putLong(self.requestTime)
        self.putLong(self.time)
        
    def decodePayload(self):
        self.clientAddress = self.getAddress()
        self.systemIndex = self.getShort()
        i = 0
        while i < 10:
            self.systemAddresses.append(self.getAddress())
            i += 1
        self.requestTime = self.getLong()
        self.time = self.getLong()
