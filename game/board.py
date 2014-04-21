from coordinate import Coordinate
from serializable import Serializable


class Board(Serializable):
    tiles = [[]]

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
        print len(self.tiles)
        return self.tiles[y][x]

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
