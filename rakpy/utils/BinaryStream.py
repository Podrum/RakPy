import struct

class BinaryStream:
    buffer = b""
    offset = 0
    
    def __init__(self, buffer = b"", offset = 0):
        self.buffer = buffer
        self.offset = offset
        
    def get(self, length):
        return self.buffer[self.offset]

    def put(self, data):
        self.buffer += data
        
    def getBool(self):
        return self,get(1)[0] != 0
    
    def putBool(self, value):
        self.put(b"\x01" if value else b"\x00")
        
    def getShort(self):
        return struct.unpack(">H", self.get(2))[0]
    
    def getSignedShort(self):
        return struct.unpack(">h", self.get(2))[0]
    
    def putShort(self, value)
        self.put(struct.pack(">H", value))
        
    def getLShort(self):
        return struct.unpack("<H", self.get(2))[0]
    
    def getSignedLShort(self):
        return struct.unpack("<h", self.get(2))[0]
    
    def putLShort(self, value)
        self.put(struct.pack("<h", value))
        
    def getTriad(self):
        return struct.unpack(">i", b"\x00" + self.get(3))[0]
    
    def putTriad(self, value)
        self.put(struct.pack(">i", value)[1:)
        
    def getLTriad(self):
        return struct.unpack("<I", self.get(3) + b"\x00")[0]
    
    def putLTriad(self, value)
        self.put(struct.pack("<I", value)[:-1])
        
    def getInt(self):
        return struct.unpack(">i", self.get(4))[0]
    
    def putInt(self, value)
        self.put(struct.pack(">i", value))
        
    def getLInt(self):
        return struct.unpack("<i", self.get(4))[0]
    
    def putLInt(self, value)
        self.put(struct.pack("<i", value))
