import path_finder
from coordinate import Coordinate


class MockTile:
    def __init__(self, _type):
        self.tile_type = _type


class MockBoard:
    def __init__(self):
        O = MockTile('plain')
        X = MockTile('wall')
        self.board = [[O, O, O, O, O, O],
                      [X, X, X, X, X, O],
                      [O, O, X, X, O, O],
                      [O, X, X, O, X, O],
                      [O, O, O, O, X, O],
                      [O, O, X, O, O, O],
                      [O, O, O, O, X, X]]

    def get_tile_at_coordinate(self, x, y):
        return self.board[y][x]

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
        'wall': 10000,
    }
    path = path_finder.get_path(board, cost_table,
                                Coordinate(0, 0), Coordinate(1, 2))
    assert cmp(path, (['{"y": 0, "x": 0}', '{"y": 0, "x": 1}',
                       '{"y": 0, "x": 2}', '{"y ": 0, "x": 3}',
                       '{"y": 0, "x": 4}', '{"y": 0, "x": 5}',
                       '{"y": 1, "x": 5}', '{"y": 2, "x": 5}',
                       '{"y": 3, "x": 5}', '{"y": 4, "x": 5}',
                       '{"y": 5, "x": 5}', '{"y": 5, "x": 4}',
                       '{"y": 5, "x": 3}', '{"y": 4, "x": 3}',
                       '{"y": 4, "x": 2}', '{"y": 4, "x": 1}',
                       '{"y ": 4, "x": 0}', '{"y": 3, "x": 0}',
                       '{"y": 2, "x": 0}', '{"y": 2, "x": 1}'])) == 1
