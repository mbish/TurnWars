from game.coordinate import Coordinate, BadCoordinateCreation
from nose.tools import assert_raises


def bad_constructor_test():
    assert_raises(BadCoordinateCreation, Coordinate, -1, 1)
    assert_raises(BadCoordinateCreation, Coordinate, 1, -1)


def serializable_test():
    coordinate = Coordinate(5, 5)
    assert coordinate.as_json() == '{"x": 5, "y": 5}'


def comparison_test():
    coord1 = Coordinate(5, 5)
    coord2 = Coordinate(5, 2)
    coord3 = Coordinate(2, 5)
    coord4 = Coordinate(5, 5)
    assert coord1 == coord4
    assert coord1 != coord2
    assert coord2 != coord3
    assert coord3 != coord1

    coords = [coord1, coord4, coord2, coord3]
    assert Coordinate(5, 5) in coords
    assert Coordinate(1, 5) not in coords
