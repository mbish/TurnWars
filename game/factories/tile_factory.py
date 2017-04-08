from game.tile import Tile
from game.serializable import Serializable
from game.factories.factory import Factory
from game.exceptions import BadFactoryData


class TileFactory(Factory):

    def __init__(self, factory_data, tile_class=Tile):
        Factory.__init__(self, factory_data, tile_class)
        return

    def validate_data(self, data):
        if 'cover' not in data:
            raise BadFactoryData("cover not found")
        elif 'non_passables' not in data:
            raise BadFactoryData("non_passables not found")
        elif 'events' not in data:
            raise BadFactoryData("events not found")
        else:
            return True

    def create(self, name):
        data = self.get_data(name)
        return self.creation_class(name, data['cover'],
                                   data['non_passables'], data['events'])
