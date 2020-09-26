from binutilspy.Binary import Binary
from rakpy.server.ServerSocket import ServerSocket
from rakpy.utils.InternetAddress import InternetAddress
import os
from threading import Thread

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
        
    def handleUnconnectedPing(data):
        decodedPacket = UnconnectedPing()
        decodedPacket.buffer = data
        decodedPacket.decode()
        if not decodedPacket.isValid:
            raise Exception("Invalid offline message")
        packet = UnconnectedPong()
        packet.time = decodedPacket.time
        packet.serverID = self.id
        packet.serverName = self.name
        packet.encode()
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
        
    def run(self):
        while True:
            if self.socket.getPacket() != None:
                data, address = self.socket.getPacket()
                self.handle(data, InternetAddress(address[0], address[1]))
