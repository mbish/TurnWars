from army import Army, InvalidArmyRequest
from nose.tools import assert_raises


class MockUnitFactory:

    def get_unit_cost(self, name):
        return 10

    def create(self, name, pos):
        return "{} {}".format(name, pos)


class MockUnit:

    def as_hash(self):
        return "Im a unit"


def buy_test():
    factory = MockUnitFactory()
    army = Army('dragon', factory, 20)
    unit = army.buy_unit("footman", 'ignore')
    assert unit == "footman ignore"
    assert army.unit_table == ['footman ignore']
    unit = army.buy_unit("footman", 'ignore')
    assert army.unit_table == ['footman ignore', 'footman ignore']
    assert unit == "footman ignore"
    assert_raises(InvalidArmyRequest, army.buy_unit, "footman", 'ignore')


def add_unit_test():
    factory = MockUnitFactory()
    army = Army('dragon', factory, 20)
    army.add_unit("footman")
    assert army.unit_table == ['footman']


def serializable_test():
    factory = MockUnitFactory()
    army = Army('dragon', factory, 20)
    unit = MockUnit()
    army.add_unit(unit)
    json_string = army.flat()
    assert army.as_json() == '{"units": ["Im a unit"]}'


def find_unit_test():
    factory = MockUnitFactory()
    army = Army('dragon', factory, 20)
    unit = MockUnit()
    army.add_unit(unit)
    unit2 = MockUnit()
    army.add_unit(unit2)
    unit3 = MockUnit()
    army.add_unit(unit3)
    found_unit = army.find_unit(id(unit))
    assert id(found_unit) == id(unit)
    found_unit = army.find_unit(id(unit2))
    assert id(found_unit) == id(unit2)
