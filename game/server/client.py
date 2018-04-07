import uuid
import hashlib
from game.server.names import random_name

class Client:
    def __init__(self, socket):
        self.id_string = hashlib.sha256(socket.ip.encode('utf-8')).hexdigest()[0:32] #uuid.uuid4().hex
        self.socket = socket
        self.spectating = False
        self.name = ''

    def send(self, message):
        self.socket.send(message)

    def setSpectator(self, isSpectating):
        self.spectating = isSpectating
