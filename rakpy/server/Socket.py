import socket

class Socket:
    socket = None
    
    def __init__(self, address):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        try:
            self.socket.bind((address.getAddress(), address.getPort()))
        except socket.error as e:
            print("Cannot use this port! Is a server already on it?")
            print(str(e))
        else:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            #self.socket.setblocking(False)
       
    def getPacket(self):
        data = self.socket.recvfrom(65535)
        print(f"IN -> {data}")
        return data
          
    def putPacket(self, buffer, address):
        data = self.socket.sendto(buffer, address)
        print(f"OUT -> {data}")
        return data
      
    def closeSocket(self):
        self.socket.close()
