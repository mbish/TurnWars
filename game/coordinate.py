from game.serializable import Serializable


class Coordinate(Serializable):

    def __init__(self, x, y):
        if(x < 0 or y < 0):
            raise BadCoordinateCreation("Cannot create coordinate with values \
                    x: {0} and y: {1}".format(x, y))
        self.x = x
        self.y = y

    def get_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    # the comparison operators were overriden to assist in path finding
    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return self.x.__hash__()+self.y.__hash__()

    def flat(self):
        return {
            'x': self.x,
            'y': self.y,
        }


class BadCoordinateCreation(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
