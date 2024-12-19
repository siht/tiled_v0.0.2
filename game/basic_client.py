from time import sleep
from twisted.spread import pb
from twisted.internet import reactor

from preferences import (
    PORT,
    DIRECTION_UP,
    DIRECTION_DOWN,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
)

factory = pb.PBClientFactory()
server = None

def gotServer(serv):
    global server
    server = serv

connection = reactor.connectTCP('localhost', PORT, factory)
reactor.callLater(4, reactor.crash)

reactor.run()
d = factory.getRootObject()
d.addCallback(gotServer)
reactor.iterate()

print(server)

d = server.callRemote('GameStartRequest')
print(d)
reactor.iterate()
sleep(5)
d = server.callRemote('CharactorMoveRequest', DIRECTION_UP)
print(d)
reactor.iterate()
sleep(5)
d = server.callRemote('CharactorMoveRequest', DIRECTION_RIGHT)
print(d)
reactor.iterate()
sleep(5)
d = server.callRemote('CharactorMoveRequest', DIRECTION_DOWN)
print(d)
reactor.iterate()
sleep(5)
d = server.callRemote('CharactorMoveRequest', DIRECTION_LEFT)
print(d)
reactor.iterate()
