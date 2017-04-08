from game.factories.scenario_builder import ScenarioBuilder
from game.exceptions import BuildInvalid
from nose.tools import assert_raises


class MockBoardFactory:
    def create(self, name):
        return name


class MockArmyFactory:
    def create(self, name):
        self.name = name
        return self.name


class MockScenario:

    def __init__(self):
        self.objects = []
        self.armies = 2
        self.buildings = 2
        self.units = 2
        self.board = []
        self.coordinates_valid = True

    def validate(self):
        if not self.validate_coordinates():
            raise Exception

    def get_board(self):
        return self.board

    def add_army(self, *arg):
        self.objects.append(*arg)

    def add_unit(self, *arg):
        self.objects.extend(arg)

    def add_building(self, *arg):
        self.objects.extend(arg)

    def set_starting_money(self, *arg):
        self.objects.extend(arg)

    def num_armies(self):
        return self.armies

    def _unit_count(self):
        return self.units

    def set_board(self, board):
        self.board = board

    def validate_coordinates(self):
        return self.coordinates_valid

    def _building_count(self):
        return self.buildings


def add_army_test():
    builder = ScenarioBuilder(MockBoardFactory(),
                              MockArmyFactory(), MockScenario)
    builder.add_army("dragon")
    builder.add_army("salamander")
    builder.add_unit("footman", "tank", "archer", "pikeman")
    builder.add_building("house", "barn")
    builder.set_starting_money("500")
    builder.set_board('hi')
    scenario = builder.pop_instance()
    assert scenario.objects == ['dragon', 'salamander',
                                'footman', 'tank', 'archer', 'pikeman',
                                'house', 'barn', '500']


def set_board_test():
    builder = ScenarioBuilder(MockBoardFactory(),
                              MockArmyFactory(), MockScenario)
    builder.set_board("this is a board")
    assert builder.pop_instance().board == "this is a board"


def pop_instance_board_test():
    builder = ScenarioBuilder(MockBoardFactory(),
                              MockArmyFactory(), MockScenario)
    builder.set_board("this is a board")
    assert builder.pop_instance().board == "this is a board"


def pop_instance_clear_test():
    builder = ScenarioBuilder(MockBoardFactory(),
                              MockArmyFactory(), MockScenario)
    builder.set_board("this is a board")
    assert builder.pop_instance().board == "this is a board"


def pop_instance_failure_test():
    builder = ScenarioBuilder(MockBoardFactory(),
                              MockArmyFactory(), MockScenario)
    builder._instance.coordinates_valid = False
    builder.set_board("this is a board")
    assert_raises(BuildInvalid, builder.pop_instance)
    builder._instance.coordinates_valid = True
    builder.pop_instance()
