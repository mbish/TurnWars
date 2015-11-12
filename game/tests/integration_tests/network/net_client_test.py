from twisted.internet import reactor, defer
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.protocols import basic
import json

class ClientProtocolTest(basic.Int32StringReceiver):
    def __init__(self):
        self.results = []

    def stringReceived(self, data):
        callback = self.results.pop(0)
        callback.callback(json.loads(data))

    def send(self, data):
        callback = defer.Deferred()
        self.results.append(callback)
        self.sendString(json.dumps(data))
        return callback
