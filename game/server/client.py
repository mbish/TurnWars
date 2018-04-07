import uuid
import hashlib

class Client:
    def __init__(self, socket):
        self.id_string = hashlib.sha256(socket.ip.encode('utf-8')).hexdigest()[0:32] #uuid.uuid4().hex
        self.socket = socket
        self.spectating = False

    def send(self, message):
        self.socket.send(message)

    def setSpectator(self, isSpectating):
        self.spectating = isSpectating
