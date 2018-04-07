import json
import sys
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import stdio
from twisted.protocols import basic

playerId = None
if len(sys.argv) > 1:
    playerId = sys.argv[1]

class TWCli(basic.LineReceiver):
    from os import linesep as delimiter

    def __init__(self, web_client):
        self.web_client = web_client
        self.web_client.postStringReceived = self._prompt
        self.web_client.postStringSent = self._prompt
        self.web_client.match_id = None

    def join(self, message):
        [matchId] = message
        self.web_client.match_id = matchId
        return {
            'type': 'join',
            'playerId': self.web_client.getId(),
            'matchId': matchId
        }

    def create(self, message):
        response = {
            'playerId': self.web_client.getId(),
            'type': 'create'
        }
        if(len(message)):
            response['scenario'] = message.pop()

        return response

    def refresh(self, message):
        if(message):
            [match] = message
        else:
            match = self.web_client.match_id
        return {
            'playerId': self.web_client.getId(),
            'type': 'action',
            'name': 'refresh',
            'matchId': match
        }

    def listMatches(self, message):
        response = {
            'type': 'listMatches'
        }
        return response

    def listMaps(self, message):
        response = {
            'type': 'listMaps'
        }
        return response

    def _prompt(self, data=""):
        self.transport.write(b'\r>>> ')

    def connectionMade(self):
        self._prompt()

    def dataReceived(self, data):
        message = self._parseMessage(data.decode('utf-8').strip('\n'))
        self._send(message)

    def _parseMessage(self, message):
        parts = message.split(' ')
        command = parts[0]
        return getattr(self, command)(parts[1:])

    def _send(self, message):
        self.web_client.send(message)
        self._prompt()
        return

    

class WebClient(basic.Int32StringReceiver):
    def __init__(self):
        self.state = 'unregistered'
        self.id = 0
        self.postStringReceived = lambda: None
        self.postStringSent = lambda: None

    def stringReceived(self, data):
        print("\rV", data.decode('utf-8'))
        getattr(self, self.state)(json.loads(data.decode('utf-8')))
        self.postStringReceived(data)

    def send(self, data):
        print("\r^", data)
        message = json.dumps(data).encode('utf-8')
        self.sendString(message)
        self.postStringSent(data)

    def registered(self, data):
        if 'type' in data and data['type'] == 'matchLobby':
            self.match_id = data['matchId']
        return

    def unregistered(self, data):
        if('type'in data):
            if(data['type'] == 'welcome'):
                if(playerId):
                    self.send({
                        'type': 'register',
                        'playerId': playerId
                    })
                else:
                    self.send({
                        'type': 'register',
                    })
            if(data['type'] == 'accept'):
                self.id = data['playerId']
                self.state = 'registered'

    def getId(self):
        return self.id

class ClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print('Started to connect.')

    def buildProtocol(self, addr):
        print('Connected.')
        web_client = WebClient()
        stdio.StandardIO(TWCli(web_client))
        return web_client

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)

reactor.connectTCP('localhost', 1025, ClientFactory())
reactor.run()
