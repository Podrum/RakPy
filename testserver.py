import os
from rakpy.server.Server import Server
from rakpy.server.Interface import Interface
from rakpy.utils.InternetAddress import InternetAddress
import signal

class TestServer(Interface):
    server = None
    name = None
    
    def __init__(self):
        edition = input("Choose Edition [mcbe/mcpi] ")
        if edition.lower() == "mcbe":
            self.name = "MCPE;Dedicated Server;390;1.14.60;0;10;13253860892328930865;Bedrock level;Survival;1;19132;19133;"
        elif edition.lower() == "mcpi":
            self.name = "MCCPP;Demo;Dedicated Server | 0/10"
        else:
            print("Invalid Edition")
            os.kill(os.getpid(), signal.SIGTERM)
        self.server = Server(InternetAddress(".".join(["0", "0", "0", "0"]), 19132), self)
        self.server.name = self.name
      
    def onOpenConnection(self, connection):
        print("OPEN_CONNECTION")
        
    def onCloseConnection(self, address, reason):
        print("CLOSED_CONNECTION")
        
    def onEncapsulated(self, packet, address):
        print("ENCAPSULATED")
        
TestServer()
