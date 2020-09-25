from binutilspy.Binary import Binary
from binutilspy.BinaryStream import BinaryStream
from rakpy.protocol.Ack import Ack
from rakpy.protocol.BitFlags import BitFlags
from rakpy.protocol.ConnectedPing import ConnectedPing
from rakpy,protocol.ConnectedPong import ConnectedPong
from rakpy.protocol.ConnectionRequest import ConnectionRequest
from rakpy.protocol.ConnectionRequestAccepted import ConnectionRequestAccepted
from rakpy,protocol.DataPacket import DataPacket
from rakpy.protocol.EncapsulatedPacket import EncapsulatedPacket
from rakpy.protocol.Nack import Nack
from rakpy.protocol.NewIncomingConnection import NewIncomingConnection
from rakpy.utils.InternetAddress import InternetAddress
from time import time as timeNow

class Connection:
    priority = {
        "Normal": 0,
        "Immediate": 1
    }

    status = {
        "Connecting": 0,
        "Connected": 1,
        "Disconnecting": 2,
        "Disconnected": 3
    }
    
    listener = None
    mtuSize = None
    address = None
    state = status["Connecting"]
    nackQueue = []
    ackQueue = []
    recoveryQueue = {}
    packetToSend = []
    sendQueue = DataPacket()
    splitPackets = []
    windowStart = -1
    windowEnd = 2048
    reliableWindowStart = 0
    reliableWindowEnd = 2048
    reliableWindow = {}
    lastReliableIndex = -1
    receivedWindow = []
    lastSequenceNumber = -1
    sendSequenceNumber = 0
    messageIndex = 0
    channelIndex = []
    needACK = []
    splitID = 0
    lastUpdate = None
    isActive = False
    
    def __init__(self, listener, mtuSize, address):
        self.listener = listener
        self.mtuSize = mtuSize
        self.address = address
        self.lastUpdate = int(timeNow())
        for i in range(0, 32):
            self.channelIndex.insert(i, 0)
            
    def update(self, timestamp):
        if not self.isActive and (self.lastUpdate + 10000) < timestamp:
            self.disconnect("timeout")
            return
        self.isActive = False
        if len(self.ackQueue) > 0:
            pk = Ack()
            pk.packets = self.ackQueue
            self.sendPacket(pk)
            self.ackQueue = []
        if len(self.nackQueue) > 0:
            pk = Nack()
            pk.packets = self.nackQueue
            self.sendPacket(pk)
            self.nackQueue = []
        if len(self.packetToSend) > 0
            limit = 16
            for key, pk in enumerate(self.packetToSend):
                pk.sendTime = timestamp
                pk.encode()
                self.recoveryQueue[pk.sequenceNumber] = pk
                del self.packetToSend[key]
                self.sendPacket(pk)
                limit -= 1
                if limit <= 0:
                    break
            if len(self.packetToSend) > 2048:
                self.packetToSend = []
        if len(self.needAck) > 0:
            for identifierACK, indexes in enumerate(self.needACK):
                if len(indexes) == 0:
                    del self.needACK[identifierACK]
                    # Todo add Notify ACK
        for seq, pk in self.recoveryQueue.items():
            if pk.sendTime < (timeNow() - 8):
                self.packetToSend.append(pk)
                del self.recoveryQueue[seq]
        for seq in self.receivedWindow:
            if seq < self.windowStart:
                del self.receivedWindow[seq]
            else:
                break
        self.sendQueue()
        
    def disconnect(self, reason = "unknown"):
        self.listener.removeConnection(self, reason)
        
    def receive(self, buffer):
        self.isActive = True
        self.lastUpdate = timeNow()
        header = buffer[0]
        if (header & BitFlags.Valid) == 0:
            return
        elif header & BitFlags.Ack:
            return self.handleAck(buffer)
        elif header & BitFlags.Nack:
            return self.handleNack(buffer)
        else:
            return self.handleDatagram(buffer)
        
    def handleDatagram(self, buffer):
        dataPacket = DataPacket()
        dataPacket.buffer = buffer
        dataPacket.decode()
        if dataPacket.sequenceNumber < self.windowStart:
            return
        elif dataPacket.sequenceNumber > self.windowEnd:
            return
        elif dataPacket.sequenceNumber < len(self.receivedWindow):
            return
        diff = dataPacket.sequenceNumber - self.lastSequenceNumber
        if dataPacket.sequenceNumber < len(self.nackQueue):
            del self.nackQueue[dataPacket.sequenceNumber]
        self.ackQueue.append(dataPacket.sequenceNumber)
        self.receivedWindow.append(dataPacket.sequenceNumber)
        if diff != 1:
            i = self.lastSequenceNumber + 1
            while i < dataPacket.sequenceNumber:
                if i not in self.receivedWindow:
                    self.nackQueue.append(i)
                i += 1
        if diff >= 1:
            lastSequenceNumber = dataPacket.sequenceNumber
            self.windowStart += diff
            self.windowEnd += diff
        for packet in dataPacket.packets:
            self.receivePacket(packet)
            
    def handleAck(self, buffer):
        packet = Ack()
        packet.buffer = buffer
        packet.decode()
        for seq in packet.packets:
            if seq in self.recoveryQueue:
                for pk in self.recoveryQueue[seq].packets:
                    if isinstance(pk, EncapsulatedPacket) and pk.needACK and pk.messageIndex != None:
                        del self.needAck[pk.identifierAck]
                del recoveryQueue[seq]
                
    def handleNack(self, buffer):
        packet = Nack()
        packet.buffer = buffer
        packet.decode()
        for seq in packet.packets:
            if seq in self.recoveryQueue:
                pk = self.recoveryQueue[seq]
                pk.sequenceNumber = self.sequenceNumber
                self.sequenceNumber += 1
                self.packetToSend.append(pk)
                del self.recoveryQueue[seq]
                
    def receivePacket(self, packet):
        if packet.messageIndex == None:
            self.handlePacket(packet)
        else:
            if packet.messageIndex < self.reliableWindowStart:
                return
            elif packet.messageIndex > self.reliableWindowEnd:
                return
            if (packet.messageIndex - self.lastReliableIndex) == 1:
                self.lastReliableIndex += 1
                self.reliableWindowStart += 1
                self.reliableWindowEnd += 1
                self.handlePacket(packet)
                if self.reliableWindow.size > 0:
                    windows = deepcopy(self.reliableWindow)
                    reliableWindow = {}
                    windows.sort()
                    for k, v in windows.items():
                        reliableWindow[k] = v
                    self.reliableWindow = reliableWindow
                    for seqIndex, pk in self.reliableWindow:
                        if (seqIndex - self.lastReliableIndex) != 1:
                            break
                        self.lastReliableIndex += 1
                        self.reliableWindowStart += 1
                        self.reliableWindowEnd += 1
                        self.handlePacket(pk)
                        del self.reliableWindow[seqIndex]
            else:
                self.reliableWindow[packet.messageIndex] = packet
    def addEncapsulatedToQueue(self, packet, flags = self.priority["Normal"]):
        if (packet.needAck = (flags & 0b00001000) > 0) == True:
            pass
