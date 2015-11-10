import uuid

class Client:
    def __init__(self, socket):
        self.id_string = uuid.uuid4()
        self.socket = socket
