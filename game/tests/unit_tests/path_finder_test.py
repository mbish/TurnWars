from game.path_finder import NoPathFound, PathFinder
from game.coordinate import Coordinate
from nose.tools import assert_raises


class MockTile:
    def __init__(self, _type):
        self.tile_type = _type


class MockBoard:
    def __init__(self):
        O = MockTile('plain')
        X = MockTile('wall')
        self.board = [[O, O, O, O, O, O],
                      [X, X, X, X, X, O],
                      [O, O, X, O, X, O],
                      [O, X, X, X, X, O],
                      [O, O, O, O, X, O],
                      [O, O, X, O, O, O],
                      [O, O, O, O, X, X]]

    def get_tile_at_coordinate(self, coordinate):
        return self.board[coordinate.y][coordinate.x]

    def is_on_board(self, coordinate):
        if(coordinate.x < len(self.board[0]) and
           coordinate.y < len(self.board) and
           coordinate.x >= 0 and
           coordinate.y >= 0):
            return True
        else:
            return False

    def get_neighbors(self, coordinate):
        neighbors = []
        if(coordinate.x < len(self.board[0]) - 1):
            neighbors.append(Coordinate(coordinate.x + 1, coordinate.y))
        if(coordinate.x > 0):
            neighbors.append(Coordinate(coordinate.x - 1, coordinate.y))
        if(coordinate.y < len(self.board) - 1):
            neighbors.append(Coordinate(coordinate.x, coordinate.y + 1))
        if(coordinate.y > 0):
            neighbors.append(Coordinate(coordinate.x, coordinate.y - 1))

        return neighbors


def get_path_test():
    board = MockBoard()
    cost_table = {
        'plain': 1,
    }
    finder = PathFinder(board)
    path = finder.get_path(cost_table,
                           Coordinate(0, 0), Coordinate(1, 2))

    json_path = [tile.as_json() for tile in path]
    print json_path
    assert json_path == ['{"y": 0, "x": 1}',
                         '{"y": 0, "x": 2}', '{"y": 0, "x": 3}',
                         '{"y": 0, "x": 4}', '{"y": 0, "x": 5}',
                         '{"y": 1, "x": 5}', '{"y": 2, "x": 5}',
                         '{"y": 3, "x": 5}', '{"y": 4, "x": 5}',
                         '{"y": 5, "x": 5}', '{"y": 5, "x": 4}',
                         '{"y": 5, "x": 3}', '{"y": 4, "x": 3}',
                         '{"y": 4, "x": 2}', '{"y": 4, "x": 1}',
                         '{"y": 4, "x": 0}', '{"y": 3, "x": 0}',
                         '{"y": 2, "x": 0}', '{"y": 2, "x": 1}']

    assert_raises(NoPathFound, finder.get_path, cost_table,
                  Coordinate(0, 0), Coordinate(3, 2))

    path = finder.get_path(cost_table,
                           Coordinate(0, 0), Coordinate(2, 0))
    json_path = [tile.as_json() for tile in path]
    assert json_path == ['{"y": 0, "x": 1}', '{"y": 0, "x": 2}']

    path = finder.get_path(cost_table,
                           Coordinate(0, 0), Coordinate(0, 0))
    assert path == []


def get_range_test():
    board = MockBoard()
    cost_table = {
        'plain': 1,
    }
    finder = PathFinder(board)
    path = finder.tiles_in_range(cost_table,
                                 Coordinate(0, 0), 3)

    json_path = [tile.as_json() for tile in path]
    assert json_path == ['{"y": 0, "x": 1}', '{"y": 0, "x": 2}',
                         '{"y": 0, "x": 3}']

    cost_table = {
        'plain': 2,
    }
    path = finder.tiles_in_range(cost_table,
                                 Coordinate(0, 0), 4)

    json_path = [tile.as_json() for tile in path]
    assert json_path == ['{"y": 0, "x": 1}', '{"y": 0, "x": 2}']

    path = finder.tiles_in_range(cost_table,
                                 Coordinate(0, 6), 2)

    json_path = [tile.as_json() for tile in path]
    assert json_path == ['{"y": 5, "x": 0}', '{"y": 6, "x": 1}']

    path = finder.tiles_in_range(cost_table,
                                 Coordinate(0, 6), 4)

    json_path = [tile.as_json() for tile in path]
    assert json_path == ['{"y": 4, "x": 0}', '{"y": 5, "x": 0}',
                         '{"y": 5, "x": 1}', '{"y": 6, "x": 1}',
                         '{"y": 6, "x": 2}']

    path = finder.tiles_in_range(cost_table,
                                 Coordinate(0, 0), 0)
    assert path == []
