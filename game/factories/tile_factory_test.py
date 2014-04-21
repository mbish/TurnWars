from tile_factory import TileFactory
from factory import BadFactoryData, BadFactoryRequest
from nose.tools import assert_raises


class MockTile:
    name = ''
    cover = 0
    non_passable = {}
    events = {}

    def __init__(self, name, cover, non_passable, events):
        self.name = name
        self.cover = cover
        self.non_passable = non_passable
        self.events = events
        return

    def get_value(self):
        return "{} {} {} {}".format(self.name, self.cover,
                                    len(self.non_passable), len(self.events))


def bad_constructor_test():

    factory_data = {
        'bad_key': {
            'cover': 4,
            'non_passables': {}
        }
    }
    assert_raises(BadFactoryData, TileFactory, factory_data, MockTile)
    factory_data = {
        'bad_key': {
            'non_passables': {},
            'events': {}
        }
    }
    assert_raises(BadFactoryData, TileFactory, factory_data, MockTile)
    factory_data = {
        'bad_key': {
            'events': {},
            'cover': 4,
        }
    }
    assert_raises(BadFactoryData, TileFactory, factory_data, MockTile)


def make_factory_data():
    return {
        'forest': {
            'cover': 5,
            'non_passables': {
                'tred': 1
            },
            'events': {}
        },
        'plains': {
            'cover': 0,
            'non_passables': {},
            'events': {}
        }
    }


def creation_test():
    factory_data = make_factory_data()
    factory = TileFactory(factory_data, MockTile)
    tile = factory.create('forest')
    assert tile.get_value() == "forest 5 1 0"
    tile = factory.create('plains')
    assert tile.get_value() == "plains 0 0 0"
    assert_raises(BadFactoryRequest, factory.create, 'non_existant')


def get_data_test():
    factory_data = make_factory_data()
    factory = TileFactory(factory_data, MockTile)
    assert_raises(BadFactoryRequest, factory.create, 'non_existant')
    tile = factory.create('forest')


def serializable_test():
    factory_data = make_factory_data()
    factory = TileFactory(factory_data, MockTile)
    json_string = (
        '{"plains": {"non_passables": {}, "cover": 0, "events": {}}, '
        '"forest": {"non_passables": {"tred": 1}, "cover": 5, "events": {}}}'
    )
    assert factory.as_json() == json_string
