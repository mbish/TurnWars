from coordinate import Coordinate
from serializable import Serializable


class Board(Serializable):

    def __init__(self, tiles):
        if(len(tiles) == 0):
            raise InvalidBoardDimensions("Refusing to create empty board")

        row_length = len(tiles[0])
        for row in tiles:
            if(len(row) != row_length or len(row) == 0):
                raise InvalidBoardDimensions(
                    "Expected dimension {} got {}".format(
                        len(row), row_length))
        self.tiles = tiles
        return

    def get_dimensions(self):
        return Coordinate(len(self.tiles[0]), len(self.tiles))

    def get_tile_at_coordinate(self, x, y):
        return self.tiles[y][x]

    def get_neighbors(self, coordinate):
        neighbors = []
        if(self.is_on_board(coordinate.x + 1, coordinate.y)):
            neighbors.append(Coordinate(coordinate.x + 1, coordinate.y))
        if(self.is_on_board(coordinate.x - 1, coordinate.y)):
            neighbors.append(Coordinate(coordinate.x - 1, coordinate.y))
        if(self.is_on_board(coordinate.x, coordinate.y - 1)):
            neighbors.append(Coordinate(coordinate.x, coordinate.y + 1))
        if(self.is_on_board(coordinate.x, coordinate.y - 1)):
            neighbors.append(Coordinate(coordinate.x, coordinate.y - 1))

        return neighbors

    def is_on_board(self, x, y):
        x_on_board = False
        y_on_board = False
        if(x < len(self.tiles[0]) and
           x >= 0):
            x_on_board = True
        if(y < len(self.tiles) and
           y >= 0):
            y_on_board = True

        return True

    def flat(self):
        serial_tiles = []
        for row in range(len(self.tiles)):
            serial_tiles.append([])
            for col in range(len(self.tiles[row])):
                serial_tiles[row].append(self.tiles[row][col].flat())

        return serial_tiles


class InvalidBoardDimensions(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
