from game.tile import Tile
from game.serializable import Serializable
from factory import Factory, BadFactoryData, BadFactoryRequest


class TileFactory(Factory):

    def __init__(self, factory_data, tile_class=Tile):
        Factory.__init__(self, factory_data, tile_class)
        return

    def validate_data(self, data):
        if('cover' not in data or
           'non_passables' not in data or
           'events' not in data):
            return False
        else:
            return True

    def create(self, name):
        data = self.get_data(name)
        return self.creation_class(name, data['cover'],
                                   data['non_passables'], data['events'])
