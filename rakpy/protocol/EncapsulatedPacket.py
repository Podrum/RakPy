from rakpy.protocol.Reliability import Reliability
from rakpy.utils.BinaryStream import BinaryStream

class EncapsulatedPacket:
    buffer = b""
    reliability = 0
    messageIndex = 0
    sequenceIndex = 0
    orderIndex = 0
    orderChannel = 0
    splitCount = 0
    splitIndex = 0
    splitId = 0
    
    @staticmethod
    def fromBinary(stream):
        packet = EncapsulatedPacket()
        header = stream.getByte()
        packet.reliability = (header & 224) >> 5
        split = (header & 0x10) > 0
        length = stream.getShort() >> 3
        if length == 0:
            raise Exception("Got an empty encapsulated packet")       
        if Reliability.isReliable(packet.reliability):
            packet.messageIndex = stream.getLTriad()
        if Reliability.isSequenced(packet.reliability):
            packet.sequenceIndex = stream.getLTriad()
        if Reliability.isSequencedOrOrdered(packet.reliability):
            packet.orderIndex = stream.getLTriad()
            packet.orderChannel = stream.getByte()
        if split:
            packet.splitCount = stream.getInt()
            packet.splitId = stream.getShort()
            packet.splitIndex = stream.getInt()
        packet.buffer = stream.get(length)
        return packet

    def toBinary(self):
        stream = BinaryStream()
        header = self.reliability << 5
        if self.splitCount > 0:
            header |= 0x10
        stream.putByte(header)
        stream.putShort(len(self.buffer) << 3)
        if Reliability.isReliable(self.reliability):
            stream.putLTriad(self.messageIndex)
        if Reliability.isSequenced(self.reliability):
            stream.putLTriad(self.sequenceIndex)
        if Reliability.isSequencedOrOrdered(self.reliability):
            stream.putLTriad(self.orderIndex)
            stream.putByte(self.orderChannel)
        if self.splitCount > 0:
            stream.putInt(self.splitCount)
            stream.putShort(self.splitId)
            stream.putInt(self.splitIndex)
        stream.put(self.buffer)
        return stream
    
    def getTotalLength(self):
        length = 3
        length += 3 if Reliability.isReliable(self.reliability) else 0
        length += 3 if Reliability.isSequenced(self.reliability) else 0
        length += 4 if Reliability.isSequencedOrOrdered(self.reliability) else 0
        length += 10 if self.splitCount > 0 else 0
        length += len(self.buffer)
        return length
