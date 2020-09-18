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
