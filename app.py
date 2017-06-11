from twisted.internet import reactor, endpoints, protocol
from game.server.server import \
    Server, \
    MatchManager, \
    PublicProtocol, \
    WebSocketServer
from autobahn.twisted.websocket import WebSocketServerFactory
from game.server.match import Match

manager = MatchManager(Match)
endpoints.serverFromString(reactor, "tcp:1025").listen(Server(manager))

webSocketServer = WebSocketServer(u"ws://192.168.2.21:1026", manager)
reactor.listenTCP(1026, webSocketServer)
reactor.run()
