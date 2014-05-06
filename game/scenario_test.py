from game.scenario import Scenario, BadScenarioData
from nose.tools import assert_raises


class MockObject:

    def __init__(self, name, position):
        self.name = name
        self.coordinate = position

    def flat(self):
        return self.name


class MockArmy:

    def __init__(self, name):
        self.name = name
        self.turn = 0
        self.units = []
        self.buildings = []

    def take_turn(self):
        self.turn = 1

    def build_unit(self, name, pos):
        unit = "unit {0} {1}".format(name, pos)
        self.units.append(unit)

    def build_building(self, name, pos):
        unit = "building {0} {1}".format(name, pos)
        self.buildings.append(unit)


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
    unit1 = MockObject("footman", "ignore")
    scenario.add_unit("rat", unit1)
    rat = scenario._find_army("rat")
    assert "unit footman ignore" in rat.units

    scenario.add_unit("dragon", unit1)
    dragon = scenario._find_army("dragon")
    assert "unit footman ignore" in dragon.units
    assert "unit footman ignore" in rat.units

    unit2 = MockObject("horse", "here")
    scenario.add_unit("dragon", unit2)
    assert "unit horse here" in dragon.units
    assert "unit horse here" not in rat.units


def add_building_test():
    scenario = test_scenario()
    scenario.add_army(MockArmy("dragon"))
    scenario.add_army(MockArmy("rat"))
    building1 = MockObject("house", "ignore")
    scenario.add_building("rat", building1)
    rat = scenario._find_army("rat")
    assert "building house ignore" in rat.buildings
