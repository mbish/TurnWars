from game.factories.board_factory import BoardFactory
from game.exceptions import BadFactoryData
from nose.tools import assert_raises


class MockTileFactory:

    def create(self, tile):
        return "{0} created".format(tile)


class MockBoard:

    def __init__(self, tiles):
        self.tiles = tiles


# def load_from_json_test():
#     tile_factory = MockTileFactory()
#     loader = BoardLoader(tile_factory, MockBoard)
#     assert_raises(BadLoaderData, loader.load_from_json, '{"test": "value"}')
#     assert_raises(BadLoaderData, loader.load_from_json,
#                   '{"test": ["value"]}')
#     board = loader.load_from_json('{"tiles": [["tile1", "tile2"]]}')
#     assert board.tiles == [['tile1 created', 'tile2 created']]
