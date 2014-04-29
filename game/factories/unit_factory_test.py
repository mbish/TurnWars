from game.factories.unit_factory import UnitFactory
from game.factories.factory import BadFactoryRequest
from nose.tools import assert_raises


class MockUnit:

    def __init__(self, name, transport, weapon, armor, coordinate, army):
        self.name = name
        self.transport = transport
        self.weapon = weapon
        self.armor = armor
        self.coordinate = coordinate
        self.army = army

    def get_value(self):
        return "{0} {1} {2} {3} {4} {5}".format(
            self.name,
            self.weapon,
            self.transport,
            self.armor,
            self.coordinate,
            self.army,
        )


class MockFactory:

    def create(self, name):
        return name

    def can_make(self):
        return False

    def get_data(self, name):
        return {
            'data': "{0} data".format(name)
        }


class MockTransportFactory(MockFactory):

    def can_make(self, name):
        return name == 'foot'


class MockWeaponFactory(MockFactory):

    def can_make(self, name):
        return name == 'sword'


class MockArmorFactory(MockFactory):

    def can_make(self, name):
        return name == 'cloth'


def validate_test():
    factory_data = {
        'footman': {
            'transport': 'foot',
            'armor': 'cloth',
            'weapon': 'sword',
            'cost': 10,
        },
        'snowman': {
            'transport': 'ice',
            'armor': 'cloth',
            'weapon': 'sword',
            'cost': 20,
        },
        'goman': {
            'transport': 'foot',
            'armor': 'paper',
            'weapon': 'sword',
            'cost': 30,
        },
        'toeman': {
            'transport': 'foot',
            'armor': 'cloth',
            'weapon': 'toe',
            'cost': 40,
        }
    }
    factory = UnitFactory({}, MockTransportFactory(),
                          MockWeaponFactory(), MockArmorFactory(),
                          'dragon', MockUnit)
    assert factory.validate_data(factory_data['footman'])
    assert not factory.validate_data(factory_data['snowman'])
    assert not factory.validate_data(factory_data['goman'])
    assert not factory.validate_data(factory_data['toeman'])


def create_test():
    factory_data = {
        'footman': {
            'transport': 'foot',
            'armor': 'cloth',
            'weapon': 'sword',
            'cost': 10,
        },
    }
    factory = UnitFactory(factory_data, MockTransportFactory(),
                          MockWeaponFactory(), MockArmorFactory(),
                          'dragon', MockUnit)
    unit = factory.create('footman', 'middle')
    assert unit.get_value() == 'footman sword foot cloth middle dragon'
    unit = factory.create('footman')
    assert unit.coordinate.x == 0
    assert unit.coordinate.y == 0


def unit_cost_test():
    factory_data = {
        'footman': {
            'transport': 'foot',
            'armor': 'cloth',
            'weapon': 'sword',
            'cost': 20,
        },
    }
    factory = UnitFactory(factory_data, MockTransportFactory(),
                          MockWeaponFactory(), MockArmorFactory(),
                          'dragon', MockUnit)

    cost = factory.get_unit_cost('footman')
    assert cost == 20
    assert_raises(BadFactoryRequest, factory.get_unit_cost, 'other')


def get_factory_test():
    factory_data = {
        'footman': {
            'transport': 'foot',
            'armor': 'cloth',
            'weapon': 'sword',
            'cost': 20,
        },
    }
    factory = UnitFactory(factory_data, MockTransportFactory(),
                          MockWeaponFactory(), MockArmorFactory(),
                          'dragon', MockUnit)

    armor_factory = factory.get_factory('armor')
    assert armor_factory.can_make('cloth')
    weapon_factory = factory.get_factory('weapon')
    assert weapon_factory.can_make('sword')
    transport_factory = factory.get_factory('transport')
    assert transport_factory.can_make('foot')
    assert_raises(BadFactoryRequest, factory.get_factory, 'blahhhrg')


def equipment_info_test():
    factory_data = {
        'footman': {
            'transport': 'foot',
            'armor': 'cloth',
            'weapon': 'sword',
            'cost': 20,
        },
    }
    factory = UnitFactory(factory_data, MockTransportFactory(),
                          MockWeaponFactory(), MockArmorFactory(),
                          'dragon', MockUnit)

    transport_data = factory.equipment_info('footman', 'transport')
    assert transport_data == {
        'name': 'foot',
        'data': 'foot data'
    }

    armor_data = factory.equipment_info('footman', 'armor')
    assert armor_data == {
        'name': 'cloth',
        'data': 'cloth data'
    }


def full_unit_info_test():
    factory_data = {
        'footman': {
            'transport': 'foot',
            'armor': 'cloth',
            'weapon': 'sword',
            'cost': 20,
        },
    }
    factory = UnitFactory(factory_data, MockTransportFactory(),
                          MockWeaponFactory(), MockArmorFactory(),
                          'dragon', MockUnit)
    unit_data = factory.full_unit_info('footman')
    assert unit_data == {
        'armor': {
            'data': 'cloth data',
            'name': 'cloth'
        },
        'weapon': {
            'data': 'sword data',
            'name': 'sword',
        },
        'transport': {
            'data': 'foot data',
            'name': 'foot'
        },
        'cost': 20,
    }
