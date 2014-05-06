from game.factories.scenario_builder import ScenarioBuilder


class MockBoardFactory:
    def create(self, name):
        return name


class MockArmyFactory:
    def create(self, name):
        self.name = name
        return self.name


class MockScenario:

    def __init__(self):
        self.list = []
        self.armies = 2
        self.units = 2
        self.board = []

    def get_board(self):
        return self.board

    def add_army(self, *arg):
        self.list.append(*arg)

    def add_unit(self, *arg):
        self.list.extend(arg)

    def add_building(self, *arg):
        self.list.extend(arg)

    def set_starting_money(self, *arg):
        self.list.extend(arg)

    def num_armies(self):
        return self.armies

    def _unit_count(self):
        return self.units

    def set_board(self, board):
        self.board = board

    def validate_coordinates(self):
        return True


def add_army_test():
    builder = ScenarioBuilder(MockBoardFactory(),
                              MockArmyFactory(), MockScenario)
    builder.add_army("dragon")
    builder.add_army("salamander")
    builder.add_unit("footman", "tank", "archer", "pikeman")
    builder.add_building("house", "barn")
    builder.set_starting_money("500")
    builder.set_board('hi')
    scenario = builder.get_instance()
    assert scenario.list == ['dragon', 'salamander',
                             'footman', 'tank', 'archer', 'pikeman', 'house',
                             'barn', '500']
