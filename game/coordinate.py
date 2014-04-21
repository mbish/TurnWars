from serializable import Serializable


class Coordinate(Serializable):
    x = 0
    y = 0

    def __init__(self, x, y):
        if(x < 0 or y < 0):
            raise BadCoordinateCreation("Cannot create coordinate with values \
                    x: {} and y: {}".format(x, y))
        self.x = x
        self.y = y

    def flat(self):
        return {
            'x': self.x,
            'y': self.y,
        }


class BadCoordinateCreation(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
