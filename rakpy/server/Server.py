from binutilspy.Binary import Binary
from rakpy.protocol.PacketIdentifiers import PacketIdentifiers
from rakpy.protocol.UnconnectedPing import UnconnectedPing
from rakpy.protocol.UnconnectedPong import UnconnectedPong

from rakpy.server.Connection import Connection
from rakpy.server.ServerSocket import ServerSocket
from rakpy.utils.InternetAddress import InternetAddress
import os
from threading import Thread
from time import sleep, time as timeNow

class Server(Thread):
    protocol = 10
    raknetTps = 100
    raknetTickLength = 1 / raknetTps
    
    id = Binary.readLong(os.urandom(8))
    name = None
    socket = None
    connections = {}
    shutdown = False   
    
    def __init__(self, address):
        super().__init__()
        self.socket = ServerSocket(address)
        self.listen(address)
        self.start()
        
    def handleUnconnectedPing(self, data):
        decodedPacket = UnconnectedPing()
        decodedPacket.buffer = data
        decodedPacket.decode()
        if not decodedPacket.isValid:
            raise Exception("Invalid offline message")
        packet = UnconnectedPong()
        packet.time = decodedPacket.time
        packet.serverId = self.id
        packet.serverName = self.name
        packet.encode()
        return packet.buffer
    
    def handleOpenConnectionRequest1(self, data):
        decodedPacket = OpenConnectionRequest1()
        decodedPacket.buffer = data
        decodedPacket.decode()
        if not decodedPacket.isValid:
            raise Exception("Invalid offline message")
        if decodedPacket.protocol != self.protocol:
            packet = IncompatibleProtocolVersion()
            packet.protocol = self.protocol
            packet.serverId = self.id
            packet.encode()
            return packet.buffer
        packet = OpenConnectionReply1()
        packet.serverId = self.id
        packet.mtu = decodedPacket.mtu
        packet.encode()
        return packet.buffer
    
    def handleOpenConnectionRequest2(self, data, address):
        decodedPacket = OpenConnectionRequest2()
        decodedPacket.buffer = data
        decodedPacket.decode()
        if not decodedPacket.isValid:
            raise Exception("Invalid offline message")
        packet = OpenConnectionReply2()
        packet.serverId = self.id
        packet.mtu = decodedPacket.mtu
        packet.clientAddress = address
        packet.encode()
        token = f"{address.getAddress}:{address.getPort}"
        connection = Connection(self, decodedPacket.mtu, address)
        self.connections[token] = connection
        return packet.buffer
        
    def handle(self, data, address):
        header = data[0]
        token = f"{address.getAddress}:{address.getPort}"
        if token in self.connections:
            connection = self.connections[token]
            connection.receive(data)
        else:
            if header == PacketIdentifiers.UnconnectedPing:
                socket.sendBuffer(self.handleUnconnectedPing(data), (address.getAddress(), address.getPort()))
            elif header == PacketIdentifiers.OpenConnectionRequest1:
                socket.sendBuffer(self.handleOpenConnectionRequest1(data), (address.getAddress(), address.getPort()))
            elif header == PacketIdentifiers.OpenConnectionRequest2:
                socket.sendBuffer(self.handleOpenConnectionRequest2(data, address), (address.getAddress(), address.getPort()))
       
    def removeConnection(self, connection, reason):
        address = connection.address
        token = f"{address.getAddress}:{address.getPort}"
        if token in self.connections:
            self.connections[token].close()
            del self.connections[token]
        # Todo Add close connection event
        
    def tick(self):
        if not self.shutdown:
            for token, connection in self.connections.items():
                connection.update(timeNow())
        else:
            return
        sleep(self.raknetTickLength * 1000)
        
    def run(self):
        while True:
            if self.socket.getPacket() != None:
                data, address = self.socket.getPacket()
                self.handle(data, InternetAddress(address[0], address[1]))
                self.tick()
