import json
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import stdio
from twisted.protocols import basic

class TWCli(basic.LineReceiver):
    from os import linesep as delimiter

    def __init__(self, web_client):
        self.web_client = web_client

    def connectionMade(self):
        self.transport.write(b'>>> ')

    def dataReceived(self, data):
        message = self.parse_message(data.decode('utf-8').strip('\n'))
        self.send(message)

    def parse_message(self, message):
        parts = message.split(' ')
        command = parts[0]
        return getattr(self, command)(parts[1:])

    def join(self, message):
        [matchId] = message
        return {
            'type': 'join',
            'id': self.web_client.get_id(),
            'matchId': matchId
        }

    def create(self, message):
        response = {
            'id': self.web_client.get_id(),
            'type': 'create'
        }
        if(len(message)):
            response['scenario'] = message.pop()

        return response

    def send(self, message):
        self.web_client.send(message)
        self.transport.write(b'>>> ')
        return

    

class WebClient(basic.Int32StringReceiver):
    def __init__(self):
        self.state = 'unregistered'
        self.id = 0

    def stringReceived(self, data):
        print("V", data.decode('utf-8'))
        getattr(self, self.state)(json.loads(data.decode('utf-8')))

    def send(self, data):
        print("^", data)
        message = json.dumps(data).encode('utf-8')
        self.sendString(message)

    def registered(self, data):
        return

    def unregistered(self, data):
        if('type'in data):
            if(data['type'] == 'welcome'):
                self.send({
                    'type': 'register'
                })
            if(data['type'] == 'accept'):
                self.id = data['id']
                self.state = 'registered'

    def get_id(self):
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
