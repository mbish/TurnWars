from twisted.protocols import basic

class Match(basic.Int32StringReceiver):
    def __init__(self, client):
        self.join(client)
        self.clients = {}

    def join(self, client):
        self.clients[client.string_id] = client

    def stringReceived(self, msg):
        # needs to be fleshed out
        print msg
