import uuid

class Client:
    def __init__(self, socket):
        self.id_string = uuid.uuid4().hex
        self.socket = socket
        self.spectating = False

    def send(self, message):
        self.socket.send(message)

    def setSpectator(self, isSpectating):
        self.spectating = isSpectating
