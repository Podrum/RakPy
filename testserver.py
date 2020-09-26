from rakpy.server.Server import Server
from rakpy.utils.InternetAddress import InternetAddress
from rakpy.utils.MinecraftServerName import MinecraftServerName

server = Server(InternetAddress("0.0.0.0", 19132))

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
name = mcsn.toString()

server.name = name
