from game.scenario import Scenario


# TODO Add tests for scenario builder specifically the add_army
# and board interaction calls
class ScenarioBuilder:
    def __init__(self, board_factory, army_factory,
                 scenario_class=Scenario):
        self._instance = scenario_class()
        self.scenario_class = scenario_class
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

    def pop_instance(self):
        if not self._instance.board:
            raise BadScenarioRequest(
                "Cannot create a scenario with no board")

        if(not self._instance.validate_coordinates()):
            raise BadScenarioRequest(
                "Cannot create a scenario with invalid coordinates")

        if(self._instance.num_armies() < 2):
            raise BadScenarioRequest(
                "Cannot create a scenario with 1 or 0 armies")
        if(self._instance._unit_count() == 0 and
           self._instance._building_count() == 0):
            raise BadScenarioRequest(
                "Cannot create an empty scenario")

        instance = self._instance
        self._instance = self.scenario_class()
        return instance


class BadScenarioRequest(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
