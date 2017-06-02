from os import listdir
from os.path import isfile, join

from twisted.protocols import basic
from twisted.internet import protocol
from game.server.match import Match
import json
import uuid
import traceback
from game.server.client import Client

dataDir = './data/basic'

class PublicProtocol(basic.Int32StringReceiver):
    def __init__(self, factory, MatchType):
        self.MatchType = MatchType
        self.factory = factory
        self.state = 'unregistered'

    def send(self, data):
        self.sendString(json.dumps(data).encode('utf-8'))

    def connectionMade(self):
        self.factory.connections.add(self)
        self.send({
            'type': 'welcome'
        })

    def terminate(self, message):
        self.send(message)
        self.transport.loseConnection()

    def connectionLost(self, reason):
        self.factory.connections.remove(self)

    def stringReceived(self, message):
        try:
            data = json.loads(message)
            if 'id' in data:
                client = self.factory.clients[data['id']]

            if data['type'] == "listMatches":
                self.send({
                    'type': 'matchList',
                    'matches': self.factory.list_matches()
                })

            if data['type'] == "listMaps":
                onlyfiles = [f for f in listdir("./data/basic/scenarios".format(dataDir))]
                self.send({
                    'type': 'mapList',
                    'maps': onlyfiles
                })
                

            if data['type'] == "register":
                if self.state == 'registered':
                    self.terminate('error, repeated registration')
                else:
                    new_client = Client(self)
                    self.factory.clients[new_client.id_string] = new_client
                    self.send({
                        'type': 'accept', 'id': str(new_client.id_string)
                    })
                    self.state = 'registered'

            if 'matchId' in data:
                match = self.factory.pass_to_match(data['matchId'], client, data)

            if data['type'] == "create":
                if 'scenario' in data:
                    scenario = data['scenario']
                else:
                    scenario = 'default.json'
                match_id = self.factory.create_match(client, scenario)
                self.send({
                    'type': 'matchCreated', 'matchId': match_id
                })

        except Exception as e:
            traceback.print_exception(Exception, e, None)
            #self.transport.loseConnection()


class Server(protocol.Factory):
    def __init__(self, match_type=Match):
        self.connections = set()
        self.clients = {}
        self.match_type = match_type
        self.matches = {}

    def buildProtocol(self, addr):
        return PublicProtocol(self, self.match_type)

    def get_match(self, match_id):
        return self.matches[match_id]

    def create_match(self, client, scenario):
        new_match = Match(client, scenario) 
        self.matches[new_match.id_string] = new_match
        return new_match.id_string

    def list_matches(self):
        return list(self.matches.keys())

    def pass_to_match(self, match_id, connection, data):
        if(data['type'] in ['join', 'action']):
            getattr(self.get_match(match_id), data['type'])(connection, data)
