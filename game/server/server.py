from twisted.protocols import basic
from twisted.internet import protocol
from match import Match

class PublicProtocol(basic.Int32StringReceiver):
    def __init__(self, factory, MatchType):
        self.MatchType = MatchType
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.add(self)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def stringReceived(self, line):
        print line

class Server(protocol.Factory):
    def __init__(self, match_type=Match):
        self.clients = set()
        self.match_type = match_type

    def buildProtocol(self, addr):
        return PublicProtocol(self, self.match_type)
