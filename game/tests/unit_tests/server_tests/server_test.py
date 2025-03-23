from game.server import server
from nose.tools import assert_raises
from os.path import isfile

class MockManager:
    def __init__(self):
        self.clients = {}

    def list_matches(self):
        return "a match list"

    def pass_to_match(self, matchId, client, data):
        pass

    def create_match(self, client, scenario):
        pass

class MockClient:
    def __init__(self, socket=None):
        self.socket = socket

def missing_type_test():
    manager = MockManager()
    client = server.ClientConnection(manager)
    result = client.handleMessage({}, [])
    assert result['type'] == 'exception'

def list_matches_test():
    manager = MockManager()
    client = server.ClientConnection(manager)
    data = {
        'type': 'listMatches'
    }
    result = client.handleMessage(data, [])
    assert result['matches'] == 'a match list'

def list_maps_test():
    manager = MockManager()
    client = server.ClientConnection(manager)
    data = {
        'type': 'listMaps'
    }
    result = client.handleMessage(data, [])

    for f in result['maps']:
        assert isfile('./{0}/scenarios/{1}'.format(server.dataDir, f['name']))

def repeat_register_test():
    manager = MockManager()
    client = server.ClientConnection(manager)
    client.state = 'registered'
    data = {
        'type': 'register'
    }
    result = client.handleMessage(data, [])
    assert result['type'] == 'exception'

def returning_player_test():
    playerId = '1'
    manager = MockManager()
    manager.clients[playerId] = MockClient()
    client = server.ClientConnection(manager)
    data = {
        'type': 'register',
        'playerId': playerId
    }
    result = client.handleMessage(data, 'new socket!')
    print(result)
    assert manager.clients[playerId].socket == 'new socket!'

def unknown_exception_test():
    playerId = '1'
    manager = MockManager()
    manager.clients[playerId] = {}
    client = server.ClientConnection(manager)
    data = {
        'type': 'register',
        'playerId': playerId
    }
    result = client.handleMessage(data, 'new socket!')
    print result
    assert result['type'] == 'exception'
