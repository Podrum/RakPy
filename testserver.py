from rakpy.server.Server import Server
from rakpy.server.ServerInterface import ServerInterface
from rakpy.utils.InternetAddress import InternetAddress
from rakpy.utils.MinecraftServerName import MinecraftServerName

class TestServer(ServerInterface):
    server = None
    name = None
    
    def __init__(self):
        self.server = Server(InternetAddress("0.0.0.0", 19132), self)
        self.name = self.makeName()
        self.server.name = self.name
        
    def makeName(self):
        mcsn = MinecraftServerName()
        mcsn.edition = "MCPE"
        mcsn.name = "MyServer"
        mcsn.motd = "MyServer"
        mcsn.protocol = 408
        mcsn.version = "1.16.20"
        mcsn.players["online"] = 0
        mcsn.players["max"] = 0
        mcsn.gamemode = "Creative"
        mcsn.serverId = 0
        return mcsn.toString()
      
    def onOpenConnection(self, connection):
        print("OPEN_CONNECTION")
        
    def onCloseConnection(self, address, reason):
        print("CLOSED_CONNECTION")
        
    def onEncapsulated(self, packet, address):
        print("ENCAPSULATED")
        
TestServer()
