from rakpy.protocol.EncapsulatedPacket import EncapsulatedPacket
from rakpy.protocol.Packet import Packet
from rakpy.protocol.PacketIdentifiers import PacketIdentifiers

class DataPacket(Packet):
    id = 0x80
    packets = []
    sequenceNumber = 0
    
    def encodePayload(self):
        self.putLTriad(self.sequenceNumber)
        for packet in self.packets:
            self.put(packet.toBinary().buffer)
        
    def decodePayload(self):
        self.sequenceNumber = self.getLTriad()
        while not self.feof():
            self.packets.append(EncapsulatedPacket.fromBinary(self))
            
    def length(self):
        length = 4
        for packet in self.packets:
            length += packet.getTotalLength()
        return length
