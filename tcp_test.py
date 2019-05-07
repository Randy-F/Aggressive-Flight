
from socket import *
from time import ctime
import struct

# # native byteorder
# buffer = struct.pack("ihb", 1, 2, 3)
# print(repr(buffer))
# print(buffer))
# print()
# # data from a sequence, network byteorder
# data = [1, 2, 3]
# buffer = struct.pack("!ihb", *data)
# print(repr(buffer))
# print(struct.unpack("!ihb", buffer))


host = '127.0.0.1'
port = 8001
buffsize = 48
ADDR = (host,port)

tctime = socket(AF_INET,SOCK_STREAM)
tctime.bind(ADDR)
tctime.listen(3)

while True:
    print('Wait for connection ...')
    tctimeClient,addr = tctime.accept()
    print("Connection from :",addr)

    while True:
        data = tctimeClient.recv(buffsize) #.decode('utf-8', errors='ignore')
        print(data)
        print(struct.unpack("<dddddd", data))
        if not data:
            break
        # tctimeClient.send(('[%s] %s' % (ctime(),data)).encode())
    tctimeClient.close()
tctimeClient.close()