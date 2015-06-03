from game.factories.factory import Factory
from nose.tools import assert_raises

class MockClass:

    def __init__(self, data):
        self.data = data

    def get_value(self):
        return "{0}".format(self.data)


def validate_test():
    factory = Factory({}, MockClass)
    assert_raises(NotImplementedError, factory.validate_data, '')
    assert_raises(NotImplementedError, factory.create, '')
