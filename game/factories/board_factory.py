import json
from game.factories.factory import Factory
from game.board import Board
import types


class BoardFactory(Factory):

    def __init__(self, factory_data, tile_factory, creation_class=Board):
        Factory.__init__(self, factory_data, creation_class)
        self.tile_factory = tile_factory

    def validate_data(self, data):
        valid = True
        if('tiles' not in data):
            valid = False
        elif(not isinstance(data['tiles'], types.ListType)):
            valid = False
        elif(not isinstance(data['tiles'], types.ListType)):
            valid = False

        return valid

    def create(self, name):
        data = self.get_data(name)
        tiles = []
        for row in range(len(data['tiles'])):
            tiles.append([])
            for tile in data['tiles'][row]:
                new_tile = self.tile_factory.create(tile)
                tiles[row].append(new_tile)

        return self.creation_class(tiles)
