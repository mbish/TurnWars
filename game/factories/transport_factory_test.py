from transport_factory import TransportFactory
from factory import BadFactoryData
from nose.tools import assert_raises


class MockClass:

    def __init__(self, name, spaces_per_turn, starting_fuel=-1):
        self.spaces_per_turn = spaces_per_turn
        self.starting_fuel = starting_fuel
        self.name = name

    def get_value(self):
        return "{} {} {}".format(self.name,
                                 self.spaces_per_turn,
                                 self.starting_fuel)


def validation_test():
    factory_data = {
        'foot': {
            'spaces_per_turn': 5,
        },
        'fake': {
            'starting_fuel': 3,
        }
    }
    factory = TransportFactory({}, MockClass)
    assert factory.validate_data(factory_data['foot'])
    assert not factory.validate_data(factory_data['fake'])


def creation_test():
    factory_data = {
        'foot': {
            'spaces_per_turn': 5,
        },
        'tire': {
            'spaces_per_turn': 10,
            'starting_fuel': 100,
        },
    }
    factory = TransportFactory(factory_data, MockClass)
    transport = factory.create('foot')
    assert transport.get_value() == 'foot 5 -1'
    transport = factory.create('tire')
    print transport.get_value()
    assert transport.get_value() == 'tire 10 100'
