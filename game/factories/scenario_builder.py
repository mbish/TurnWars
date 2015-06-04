from game.scenario import Scenario
from game.factories.builder import Builder


# TODO Add tests for scenario builder specifically the add_army
# and board interaction calls
class ScenarioBuilder(Builder):
    def __init__(self, board_factory, army_factory,
                 scenario_class=Scenario):
        Builder.__init__(self, scenario_class)
        self.army_factory = army_factory
        self.board_factory = board_factory

    def set_board(self, name):
        board = self.board_factory.create(name)
        self._instance.set_board(board)

    def add_army(self, name):
        army = self.army_factory.create(name)
        self._instance.add_army(army)
        return self

    def add_unit(self, *args):
        self._instance.add_unit(*args)
        return self

    def add_building(self, *args):
        self._instance.add_building(*args)
        return self

    def set_starting_money(self, *args):
        self._instance.set_starting_money(*args)
        return self
