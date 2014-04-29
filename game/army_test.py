from game.army import Army, InvalidArmyRequest
from nose.tools import assert_raises


class MockBuildingFactory:

    def create(self, building_name, coordinate):
        return "{0} {1}".format(building_name, coordinate)


class MockUnitFactory:

    def get_unit_cost(self, name):
        return 10

    def create(self, name, pos):
        return "{0} {1}".format(name, pos)

    def full_unit_info(self, _type):
        return "everything for {0}".format(_type)


class MockUnit:

    def __init__(self, coordinate="ignore"):
        self.uid = id(self)
        self.coordinate = coordinate
        self.was_reset = 0

    def reset(self):
        self.was_reset = 1

    def flat(self):
        return "Im a unit"


class MockBuilding:

    def __init__(self, coordinate):
        self.coordinate = coordinate

    def flat(self):
        return "Im a building {0}".format(self.coordinate)

    def get_revenue(self):
        return 10


def test_army():
    factory = MockUnitFactory()
    building_factory = MockBuildingFactory()
    army = Army('dragon', factory, building_factory, 20)
    building = MockBuilding(5)
    building2 = MockBuilding(7)
    building3 = MockBuilding(9)
    army.add_building(building)
    army.add_building(building2)
    army.add_building(building3)
    army.turn = 1
    return army


def buy_test():
    army = test_army()
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
    army = test_army()
    army.add_unit("footman")
    assert army.unit_table == ['footman']


def serializable_test():
    army = test_army()
    unit = MockUnit()
    army.add_unit(unit)
    json_string = army.as_json()
    assert json_string == (
        '{"units": ["Im a unit"], "buildings": ["Im a building 5", '
        '"Im a building 7", "Im a building 9"]}'
    )


def find_unit_test():
    army = test_army()
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
    army = test_army()
    assert army.has_building_at(5)
    assert army.has_building_at(7)
    assert army.has_building_at(9)
    assert not army.has_building_at(11)


def get_building_at_test():
    army = test_army()
    found = army._get_building_at(7)
    assert found.coordinate == 7
    found = army._get_building_at(5)
    assert found.coordinate == 5


def can_build_test():
    army = test_army()
    assert army.can_build(5, 5)
    assert not army.can_build(200, 5)
    assert not army.can_build(5, 15)
    army.turn = 0
    assert not army.can_build(5, 5)


def has_unit_at_test():
    unit = MockUnit("here I am")
    army = test_army()
    army.add_unit(unit)
    assert army.has_unit_at("here I am")
    assert not army.has_unit_at("")


def unit_info_test():
    army = test_army()
    unit = MockUnit()
    info = army.unit_info("the best type")
    assert info == "everything for the best type"


def take_turn_test():
    army = test_army()
    unit = MockUnit()
    army.turn = 0
    army.add_unit(unit)
    army.take_turn()
    assert army.turn
    assert unit.was_reset
    assert army.money == 50


def end_turn_test():
    army = test_army()
    assert army.turn
    army.end_turn()
    assert army.turn == 0


def is_turn_test():
    army = test_army()
    assert army.is_turn()
    army.end_turn()
    assert not army.is_turn()


def build_building_test():
    army = test_army()
    army.build_building('test', 'ignore')
    assert 'test ignore' in army.buildings
    army.add_building('ranch')
    assert 'ranch' in army.buildings
