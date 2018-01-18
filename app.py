from twisted.internet import reactor, endpoints, protocol
from game.server.server import \
    Server, \
    MatchManager, \
    PublicProtocol, \
    WebSocketServer
from autobahn.twisted.websocket import WebSocketServerFactory
from game.server.match import Match

tcpPort = 1025
websocketPort = 1026
serverAddress = "192.168.2.20"

manager = MatchManager(Match)
endpoints.serverFromString(reactor, "tcp:{0}".format(tcpPort)).listen(Server(manager))

webSocketServer = WebSocketServer(u"ws://{0}:{1}".format(serverAddress, websocketPort), manager)
reactor.listenTCP(1026, webSocketServer)
print("Server listening on address {0} for websocket on port {1} and tcp on port {2}".format(serverAddress, tcpPort, websocketPort))
reactor.run()
