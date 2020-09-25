from binutilspy.Binary import Binary
import os

class Server:
    id = Binary.readLong(os.urandom(8))
    name = None
    socket = None
    connections = {}
    shutdown = False   
