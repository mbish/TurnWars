from game.factories.building_factory import BuildingFactory
from game.factories.factory import BadFactoryData
from nose.tools import assert_raises


class MockBuliding:
    def __init__(self, name, revenue, buildable_units, coordinate):
        self.name = name
        self.coordinate = coordinate
        self.buildable_units = buildable_units
        return


def validation_test():
    factory_data = {
        'fort': {
            'buildable_units': ['footman'],
            'revenue': 100
        },
    }
    factory = BuildingFactory(factory_data, MockBuliding)
    assert factory.can_make('fort')

    factory_data = {
        'fort': {
        },
    }
    assert_raises(BadFactoryData, BuildingFactory, factory_data, MockBuliding)

    factory_data = {
        'fort': {
            'revenue': 100
        }
    }
    assert_raises(BadFactoryData, BuildingFactory, factory_data, MockBuliding)


def creation_test():
    factory_data = {
        'fort': {
            'buildable_units': ['footman'],
            'revenue': 100
        },
    }
    factory = BuildingFactory(factory_data, MockBuliding)
    building = factory.create('fort')
    assert building.name == 'fort'
    assert building.buildable_units == ['footman']
    assert building.coordinate.x == 0
    assert building.coordinate.y == 0
    building = factory.create('fort', 'ignore')
    assert building.name == 'fort'
    assert building.coordinate == 'ignore'
    assert building.buildable_units == ['footman']
