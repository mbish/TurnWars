import json
from game.factories.factory import Factory
from game.board import Board
from game.exceptions import BadFactoryData
import types


class BoardFactory(Factory):

    def __init__(self, factory_data, tile_factory, creation_class=Board):
        Factory.__init__(self, factory_data, creation_class)
        self.tile_factory = tile_factory

    def validate_data(self, data):
        if 'tiles' not in data:
            raise BadFactoryData("tiles not found")
        elif not isinstance(data['tiles'], list):
            raise BadFactoryData("tiles is not a list")

        return True

    def create(self, name):
        data = self.get_data(name)
        tiles = []
        for row in range(len(data['tiles'])):
            tiles.append([])
            for tile in data['tiles'][row]:
                new_tile = self.tile_factory.create(tile)
                tiles[row].append(new_tile)

        return self.creation_class(tiles)
