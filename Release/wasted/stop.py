import socket
from time import sleep
  
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.connect(('localhost', UDP_PORT))
sock.send(str.encode("stop"))

sock.close()

UDP_PORT = 5006
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.connect(('localhost', UDP_PORT))
sock.send(str.encode("stop"))

sock.close()

UDP_PORT = 5007
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.connect(('localhost', UDP_PORT))
sock.send(str.encode("stop"))

sock.close()

# UDP_PORT = 5008
# sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# sock.connect(('localhost', UDP_PORT))
# sock.send(str.encode("stop"))

# sock.close()