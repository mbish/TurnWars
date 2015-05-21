from game.coordinate import Coordinate, BadCoordinateCreation
from game.serializable import Serializable


class Board(Serializable):

    def __init__(self, tiles):
        if(len(tiles) == 0):
            raise InvalidBoardDimensions("Refusing to create empty board")

        row_length = len(tiles[0])
        for row in tiles:
            if(len(row) != row_length or len(row) == 0):
                raise InvalidBoardDimensions(
                    "Expected dimension {0} got {1}".format(
                        len(row), row_length))
        self.tiles = tiles
        return

    def get_dimensions(self):
        return Coordinate(len(self.tiles[0]), len(self.tiles))

    def get_tile_at_coordinate(self, coordinate):
        return self.tiles[coordinate.y][coordinate.x]

    def get_neighbors(self, coordinate):
        neighbors = []
        x = coordinate.x
        y = coordinate.y
        potential_neighbors = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        for neighbor in potential_neighbors:
            try:
                if(self.is_on_board(Coordinate(neighbor[0], neighbor[1]))):
                    neighbors.append(neighbor)
            except BadCoordinateCreation:
                pass

        return neighbors

    def is_on_board(self, coordinate):
        x_on_board = False
        y_on_board = False
        if(coordinate.x < len(self.tiles[0]) and
           coordinate.x >= 0):
            x_on_board = True
        if(coordinate.y < len(self.tiles) and
           coordinate.y >= 0):
            y_on_board = True

        return x_on_board and y_on_board

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
