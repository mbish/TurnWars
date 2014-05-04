from game.factories.scenario_builder import ScenarioBuilder


class MockScenario:

    def __init__(self, _list):
        self._list = _list

    def add_army(self, *arg):
        self._list.extend(*arg)

    def add_unit(self, *arg):
        self._list.extend(*arg)

    def add_building(self, *arg):
        self._list.extend(*arg)

    def set_starting_money(self, *arg):
        self._list.extend(*arg)


def add_army_test():
    builder = ScenarioBuilder("board", "army_factory", MockScenario)
    builder.add_army("dragon", "salamander")
    builder.add_unit("footman", "tank", "archer", "pikeman")
    builder.add_building("house", "barn")
    builder.set_starting_money("500")
    scenario = builder.get_instance()
    print scenario
    assert scenario == []
