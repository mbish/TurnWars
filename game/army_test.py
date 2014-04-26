from army import Army, InvalidArmyRequest
from nose.tools import assert_raises


class MockUnitFactory:

    def get_unit_cost(self, name):
        return 10

    def create(self, name, pos):
        return "{} {}".format(name, pos)


class MockUnit:

    def __init__(self):
        self.uid = id(self)

    def as_hash(self):
        return "Im a unit"


class MockBuilding:

    def __init__(self, coordinate):
        self.coordinate = coordinate


def buy_test():
    factory = MockUnitFactory()
    building = MockBuilding(5)
    army = Army('dragon', factory, [building], 20)
    unit = army.buy_unit("footman", 5)
    assert_raises(InvalidArmyRequest, army.buy_unit,
                  "footman", 4)
    assert unit == "footman 5"
    assert army.unit_table == ['footman 5']
    unit = army.buy_unit("footman", 5)
    assert army.unit_table == ['footman 5', 'footman 5']
    assert unit == "footman 5"
    assert_raises(InvalidArmyRequest, army.buy_unit,
                  "footman", 5)


def add_unit_test():
    factory = MockUnitFactory()
    army = Army('dragon', factory, [], 20)
    army.add_unit("footman")
    assert army.unit_table == ['footman']


def serializable_test():
    factory = MockUnitFactory()
    army = Army('dragon', factory, [], 20)
    unit = MockUnit()
    army.add_unit(unit)
    json_string = army.flat()
    assert army.as_json() == '{"units": ["Im a unit"]}'


def find_unit_test():
    factory = MockUnitFactory()
    army = Army('dragon', factory, [], 20)
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


def has_building_at_test():
    factory = MockUnitFactory()
    building = MockBuilding(4)
    building2 = MockBuilding(7)
    building3 = MockBuilding(9)
    army = Army('dragon', factory, [building, building2, building3], 20)
    assert army.has_building_at(4)
    assert army.has_building_at(7)
    assert army.has_building_at(9)
    assert not army.has_building_at(11)


def get_building_at_test():
    factory = MockUnitFactory()
    building = MockBuilding(4)
    building2 = MockBuilding(7)
    building3 = MockBuilding(9)
    army = Army('dragon', factory, [building, building2, building3], 20)
    found = army._get_building_at(7)
    assert found.coordinate == 7
    found = army._get_building_at(4)
    assert found.coordinate == 4
