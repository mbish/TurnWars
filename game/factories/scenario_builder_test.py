from game.factories.scenario_builder import ScenarioBuilder


class MockScenario:

    def __init__(self, board, list):
        self.list = list
        self.armies = 2
        self.units = 2

    def add_army(self, *arg):
        self.list.extend(arg)

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


def add_army_test():
    builder = ScenarioBuilder("board", ["army_factory"], MockScenario)
    builder.add_army("dragon", "salamander")
    builder.add_unit("footman", "tank", "archer", "pikeman")
    builder.add_building("house", "barn")
    builder.set_starting_money("500")
    scenario = builder.get_instance()
    assert scenario.list == ['army_factory', 'dragon', 'salamander',
                             'footman', 'tank', 'archer', 'pikeman', 'house',
                             'barn', '500']
