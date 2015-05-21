from game.board import Board, InvalidBoardDimensions
from game.coordinate import Coordinate
from nose.tools import assert_raises, eq_


class MockTile:

    def __init__(self, new_tile_type="none"):
        self.tile_type = new_tile_type

    def flat(self):
        return "serial {0}".format(self.tile_type)


def empty_board_test():
    tiles = []
    assert_raises(InvalidBoardDimensions, Board, tiles)
    tiles = [[], [], []]
    assert_raises(InvalidBoardDimensions, Board, tiles)


def non_square_board_test():
    tiles = []
    for row in range(0, 10):
        tiles.append([])
        for col in range(0, row):
            tiles[row].append(MockTile("{0} {1}".format(row, col)))

    assert_raises(InvalidBoardDimensions, Board, tiles)


def normal_board_test():
    tiles = []
    for row in range(0, 100):
        tiles.append([])
        for col in range(0, 10):
            tiles[row].append(MockTile("{0} {1}".format(row, col)))

    board = Board(tiles)
    coordinates = board.get_dimensions()
    assert coordinates.x == 10
    assert coordinates.y == 100


def get_tile_test():
    tiles = []
    for row in range(0, 30):
        tiles.append([])
        for col in range(0, 5):
            tiles[row].append(MockTile("{0} {1}".format(col, row)))

    board = Board(tiles)
    tile = board.get_tile_at_coordinate(Coordinate(1, 4))
    assert tile.tile_type == "1 4"
    tile = board.get_tile_at_coordinate(Coordinate(3, 10))
    assert tile.tile_type == "3 10"
    tile = board.get_tile_at_coordinate(Coordinate(0, 0))
    assert tile.tile_type == "0 0"
    tile = board.get_tile_at_coordinate(Coordinate(4, 29))
    assert tile.tile_type == "4 29"
    assert_raises(IndexError, board.get_tile_at_coordinate,
                  Coordinate(100, 100))


def json_test():
    tiles = []
    for row in range(0, 2):
        tiles.append([])
        for col in range(0, 2):
            tiles[row].append(MockTile("{0} {1}".format(col, row)))

    board = Board(tiles)
    json_string = (
        '[["serial 0 0", "serial 1 0"], '
        '["serial 0 1", "serial 1 1"]]'
    )
    serial_board = board.as_json()
    assert serial_board == json_string


def get_neighbors_test():
    tiles = []
    for row in range(0, 30):
        tiles.append([])
        for col in range(0, 5):
            tiles[row].append(MockTile("{0} {1}".format(col, row)))

    board = Board(tiles)
    neighbors = board.get_neighbors(Coordinate(0, 0))
    eq_(neighbors, [(1, 0), (0, 1)])
