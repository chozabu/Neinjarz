import socket
from pickle import dumps,loads
import zlib
from zlib import compress,decompress
import select

isServer = False
isClient = False

clients = []

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server = "127.0.0.1"
#server = "192.168.1.3"
port = 4332
def checkdata():
    global isServer, isClient, port, server, sock
    return select.select([sock], [], [], 0)[0] != []

def sendserv(event, data):
    global isServer, isClient, port, server, sock
    if isClient:
        #print "sendin data to:", (server,port)
        sock.sendto(compress(dumps([event,data]),1), 0, (server,port))
        return True
    return False

def sendto(event, data, destination):
    global isServer, isClient, port, server, sock
    if isServer:
        #print "sendin data to:", destination
        sock.sendto(compress(dumps([event,data]),1), 0, destination)
        return True
    return False

def sendall(event,data):
    global isServer, isClient, port, server, sock, clients
    if isClient:return
    datas = compress(dumps([event,data]),1)
    for c in clients:
        if c.netdata != None:sock.sendto(datas, 0, c.netdata)

def initNet():
    global isServer#, isClient, port, server, sock
    if isServer:
        try:
            sock.bind(('', port))
            print( "servin on port:", port )
        except socket.error:
            print( "failed to serve" )
            isServer = False
def nextpacket():
    #global isServer, isClient, port, server, sock
    try:
        packet, peer = sock.recvfrom(0x300000)#aint there a recv all?
    except socket.error:
        print( "error recevin..." )
    try:
        packet = decompress(packet)
        packet = loads(packet)
    except zlib.error:
        print( "error decompressing, increase packet recv buffer?" )
        return None,None
    return packet, peer
