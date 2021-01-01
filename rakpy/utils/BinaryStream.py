import struct

class BinaryStream:
    buffer = b""
    offset = 0
    
    def __init__(self, buffer = b"", offset = 0):
        self.buffer = buffer
        self.offset = offset
        
    def get(self, length):
        self.offset += length
        return self.buffer[self.offset - length:self.offset]

    def put(self, data):
        self.buffer += data
        
    def getByte(self):
        return struct.unpack("B", self.get(1))[0]
    
    def getSignedByte(self):
        return struct.unpack("b", self.get(1))[0]

    def putByte(self, value):
        self.put(bytes([value & 0xff]))
        
    def getBool(self):
        return self.getByte() != 0
    
    def putBool(self, value):
        self.putByte(1 if value else 0)
        
    def getShort(self):
        return struct.unpack(">H", self.get(2))[0]
    
    def getSignedShort(self):
        return struct.unpack(">h", self.get(2))[0]
    
    def putShort(self, value):
        self.put(struct.pack(">H", value))
        
    def getLShort(self):
        return struct.unpack("<H", self.get(2))[0]
    
    def getSignedLShort(self):
        return struct.unpack("<h", self.get(2))[0]
    
    def putLShort(self, value):
        self.put(struct.pack("<h", value))
        
    def getTriad(self):
        return struct.unpack(">i", b"\x00" + self.get(3))[0]
    
    def putTriad(self, value):
        self.put(struct.pack(">i", value))[1:]
        
    def getLTriad(self):
        return struct.unpack("<I", self.get(3) + b"\x00")[0]
    
    def putLTriad(self, value):
        self.put(struct.pack("<I", value)[:-1])
        
    def getInt(self):
        return struct.unpack(">i", self.get(4))[0]
    
    def putInt(self, value):
        self.put(struct.pack(">i", value))
        
    def getLInt(self):
        return struct.unpack("<i", self.get(4))[0]
    
    def putLInt(self, value):
        self.put(struct.pack("<i", value))

    def getFloat(self):
        return struct.unpack(">f", self.get(4))[0]
    
    def getRoundedFloat(self):
        return round(self.getFloat())
    
    def putFloat(self, value):
        self.put(struct.pack(">f", value))
        
    def getLFloat(self):
        return struct.unpack("<f", self.get(4))[0]
    
    def getRoundedLFloat(self):
        return round(self.getLFloat())
    
    def putLFloat(self, value):
        self.put(struct.pack("<f", value))

    def getDouble(self):
        return struct.unpack(">d", self.get(8))[0]
    
    def putDouble(self, value):
        self.put(struct.pack(">d", value))
        
    def getLDouble(self):
        return struct.unpack("<d", self.get(8))[0]
    
    def putLDouble(self, value):
        self.put(struct.pack("<d", value))

    def getLong(self):
        return struct.unpack(">q", self.get(8))[0]
    
    def putLong(self, value):
        self.put(struct.pack(">q", value))
        
    def getLLong(self):
        return struct.unpack("<q", self.get(8))[0]
    
    def putLLong(self, value):
        self.put(struct.pack("<q", value))
