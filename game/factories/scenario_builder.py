from game.scenario import Scenario


# TODO Add tests for scenario builder
class ScenarioBuilder:
    def __init__(self, board, army_factory, scenario_class=Scenario):
        self._instance = scenario_class(board, army_factory)

    def add_army(self, *args):
        self._instance.add_army(*args)
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

    def get_instance(self):
        if(self._instance.num_armies() < 2):
            raise BadScenarioRequest(
                "Cannot create a scenario with 1 or 0 armies")
        if(self._instance._unit_count() == 0 and
           self._instance._building_count() == 0):
            raise BadScenarioRequest(
                "Cannot create an empty scenario")
        return self._instance


class BadScenarioRequest(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
