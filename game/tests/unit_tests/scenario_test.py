from game.scenario import Scenario
from game.exceptions import BadScenarioData
from nose.tools import assert_raises


class MockCoordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class MockArmy:

    def __init__(self, name):
        self.name = name
        self.turn = 0
        self.units = []
        self.buildings = []

    def take_turn(self):
        self.turn = 1

    def build_unit(self, name, pos):
        unit = "unit {0} {1} {2}".format(name, pos.x, pos.y)
        self.units.append(unit)

    def build_building(self, name, pos):
        unit = "building {0} {1} {2}".format(name, pos.x, pos.y)
        self.buildings.append(unit)

    def has_unit_at(self, coordinate):
        return coordinate.x == 8

    def num_units(self):
        return len(self.units)

    def num_buildings(self):
        return len(self.buildings)


class MockBoard:

    def __init__(self, value):
        self.value = value

    def is_on_board(self, coordinate):
        return self.value


class MockArmyFactory:

    def create(self, name):
        return MockArmy(name)


def test_scenario(board=(lambda x: True)):
    scenario = Scenario()
    return scenario


def add_army_test():
    scenario = test_scenario()
    scenario.add_army(MockArmy("dragon"))
    assert scenario.armies[0].name == "dragon"
    assert scenario.armies[0].turn == 1
    scenario.add_army(MockArmy("rat"))
    assert scenario.armies[1].name == "rat"
    assert scenario.armies[1].turn == 0


def find_army_test():
    scenario = test_scenario()
    scenario.add_army(MockArmy("dragon"))
    scenario.add_army(MockArmy("rat"))
    scenario.add_army(MockArmy("salamander"))
    army = scenario._find_army("dragon")
    assert army.name == "dragon"
    army = scenario._find_army("rat")
    assert army.name == "rat"
    army = scenario._find_army("salamander")
    assert army.name == "salamander"


def add_unit_test():
    scenario = test_scenario()
    scenario.add_army(MockArmy("dragon"))
    scenario.add_army(MockArmy("rat"))
    unit1 = {
        'name': 'footman',
        'x': 0,
        'y': 1
    }
    scenario.add_unit("rat", unit1)
    rat = scenario._find_army("rat")
    assert "unit footman 0 1" in rat.units

    scenario.add_unit("dragon", unit1)
    dragon = scenario._find_army("dragon")
    assert "unit footman 0 1" in dragon.units
    assert "unit footman 0 1" in rat.units

    unit2 = {
        'name': "horse",
        'x': 3,
        'y': 1
    }
    scenario.add_unit("dragon", unit2)
    assert "unit horse 3 1" in dragon.units
    assert "unit horse 3 1" not in rat.units


def add_building_test():
    scenario = test_scenario()
    scenario.add_army(MockArmy("dragon"))
    scenario.add_army(MockArmy("rat"))
    building1 = {
        'name': "house",
        'x': 6,
        'y': 0
    }
    scenario.add_building("rat", building1)
    rat = scenario._find_army("rat")
    assert "building house 6 0" in rat.buildings


def set_board_test():
    scenario = test_scenario()
    scenario.set_board("this is a board")
    assert scenario.get_board() == "this is a board"


def get_board_blank_test():
    scenario = test_scenario()
    assert_raises(BadScenarioData, scenario.get_board)


def validating_bad_board_test():
    scenario = test_scenario()
    scenario.set_board(MockBoard(False))
    scenario.object_coordinates.append(MockCoordinate(0, 0))
    assert_raises(BadScenarioData, scenario.validate_coordinates)


def validating_good_board_test():
    scenario = test_scenario()
    scenario.set_board(MockBoard(True))
    assert scenario.validate_coordinates()


def space_occupied_test():
    scenario = test_scenario()
    scenario.add_army(MockArmy("dragon"))
    scenario.add_army(MockArmy("rat"))
    scenario.add_unit('dragon', {
        'name': "footman",
        'x': 2,
        'y': 0
    })
    assert_raises(BadScenarioData, scenario.add_unit, 'dragon', {
        'name': "footman",
        'x': 8,
        'y': 1
    })
    assert_raises(BadScenarioData, scenario.add_building, 'dragon', {
        'name': "tower",
        'x': 8,
        'y': 0
    })


def unit_count_test():
    scenario = test_scenario()
    assert scenario._unit_count() == 0
    scenario.add_army(MockArmy("dragon"))
    scenario.add_unit('dragon', {
        'name': "footman",
        'x': 1,
        'y': 0
    })
    assert scenario._unit_count() == 1
    scenario.add_building('dragon', {
        'name': "tower",
        'x': 1,
        'y': 0
    })
    assert scenario._unit_count() == 1


def building_count_test():
    scenario = test_scenario()
    assert scenario._building_count() == 0
    scenario.add_army(MockArmy("dragon"))
    scenario.add_building('dragon', {
        'name': "tower",
        'x': 1,
        'y': 0
    })
    assert scenario._building_count() == 1
    scenario.add_unit('dragon', {
        'name': "footman",
        'x': 1,
        'y': 0
    })
    assert scenario._building_count() == 1
    scenario.add_building('dragon', {
        'name': "tower",
        'x': 1,
        'y': 0
    })
    assert scenario._building_count() == 2
