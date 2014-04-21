from coordinate import Coordinate, BadCoordinateCreation
from nose.tools import assert_raises


def bad_constructor_test():
    assert_raises(BadCoordinateCreation, Coordinate, -1, 1)
    assert_raises(BadCoordinateCreation, Coordinate, 1, -1)


def serializable_test():
    coordinate = Coordinate(5, 5)
    assert coordinate.as_json() == '{"y": 5, "x": 5}'
