from twisted.internet import reactor, endpoints, protocol
from server import Server

endpoints.serverFromString(reactor, "tcp:1025").listen(Server())
reactor.run()
