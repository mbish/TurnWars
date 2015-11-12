from twisted.protocols import basic
import uuid

class Match(basic.Int32StringReceiver):
    def __init__(self, client):
        self.clients = {}
        self.id_string = uuid.uuid4()
        self.join(client)

    def join(self, client):
        self.clients[client.id_string] = client

    def stringReceived(self, msg):
        # needs to be fleshed out
        print msg
