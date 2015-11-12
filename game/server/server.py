from twisted.protocols import basic
from twisted.internet import protocol
from match import Match
import json
from client import Client

class PublicProtocol(basic.Int32StringReceiver):
    def __init__(self, factory, MatchType):
        self.MatchType = MatchType
        self.factory = factory

    def connectionMade(self):
        self.factory.connections.add(self)

    def connectionLost(self, reason):
        self.factory.connections.remove(self)

    def stringReceived(self, line):
        try:
            data = json.loads(line)
            if data['type'] == "register":
                new_client = Client(self)
                self.factory.clients[new_client.id_string] = new_client
                self.sendString(json.dumps({
                    'type': 'accept', 'id': str(new_client.id_string)
                }))

            if 'id' in data:
                client = self.factory.clients[data['id']]
                if data['type'] == "join":
                    if 'id' in data:
                        self.factory.join_client(data['id'], client)
                if data['type'] == "create":
                    match_id = self.factory.create_match(client)
        except None:
            self.transport.loseConnection()


class Server(protocol.Factory):
    def __init__(self, match_type=Match):
        self.connections = set()
        self.clients = {}
        self.match_type = match_type
        self.matches = {}

    def buildProtocol(self, addr):
        return PublicProtocol(self, self.match_type)

    def get_match(self, identifier):
        return self.matches['identifier']

    def create_match(self, client):
        new_match = Match(client)
        self.matches[new_match.id_string] = new_match
        return new_match.id_string

    def join_client(self, match_id, connection):
        self.get_match(match_id).join(connection)
