from game.serializable import Serializable
from game.coordinate import Coordinate


class Scenario(Serializable):

    def __init__(self):
        self.armies = []
        self.object_coordinates = []
        self.board = 0

    def validate(self):
        if not self.board:
            raise BadScenarioData(
                "Cannot create a scenario with no board")

        if self.num_armies() < 2:
            raise BadScenarioData(
                "Cannot create a scenario with 1 or 0 armies")
        if(self._unit_count() == 0 and
           self._building_count() == 0):
            raise BadScenarioData(
                "Cannot create an empty scenario")
        for army in self.armies:
            if army.num_units() == 0 and army.num_buildings() == 0:
                raise BadScenarioData(
                    ("Army {0} must start with at least one unit " +
                     "or building").format(army.name))

        self.validate_coordinates()

    def num_armies(self):
        return len(self.armies)

    def set_board(self, board):
        self.board = board

    def get_board(self):
        if self.board:
            return self.board
        else:
            msg = "Attempt to get board when no board has been set"
            raise BadScenarioData(msg)

    def validate_coordinates(self):
        for coordinate in self.object_coordinates:
            if(not self.get_board().is_on_board(coordinate)):
                msg = "Cannot have object at x:{0} y:{0}".format(
                    coordinate.x, coordinate.y)
                raise BadScenarioData(msg)

        return True

    def add_army(self, army):
        if(self.num_armies() == 0):
            army.take_turn()
        self.armies.append(army)
        return len(self.armies)

    def find_unit(self, unit_id):
        for army in self.armies:
            if(army.find_unit(unit_id)):
                return army.find_unit(unit_id)

    def _find_army(self, army_name):
        army = next(army for army in self.armies if army.name == army_name)
        return army

    def unit_at(self, coordinate):
        for army in self.armies:
            unit = army.get_unit_at(coordinate)
            if(unit):
                return unit

    def add_unit(self, army_name, data):
        self._add_object(army_name, data, "unit")

    def add_building(self, army_name, data):
        self._add_object(army_name, data, "building")

    def _add_object(self, army_name, data, object_type):
        location = Coordinate(data['x'], data['y'])
        if(self.space_occupied(location)):
            msg = "Attempt to occupy a location that is already taken"
            raise BadScenarioData(msg)
        army = self._find_army(army_name)
        self._build_type(army, data, location, object_type)
        self.object_coordinates.append(location)

    def space_occupied(self, coordinate):
        for army in self.armies:
            if(army.has_unit_at(coordinate)):
                return True
        return False

    def _unit_count(self, army_name=0):
        count = 0
        to_count = []
        if(army_name):
            to_count = [self._find_army(army_name)]
        else:
            to_count = self.armies

        for army in to_count:
            count += army.num_units()

        return count

    def _building_count(self, army_name=0):
        count = 0
        to_count = []
        if(army_name):
            to_count = [self._find_army(army_name)]
        else:
            to_count = self.armies

        for army in to_count:
            count += army.num_buildings()

        return count

    def _build_type(self, army, data, location, object_type):
        if object_type == "unit":
            return army.build_unit(data['name'], location)
        elif object_type == "building":
            return army.build_building(data['name'], location)
        else:
            raise BadScenarioData(
                "Do not know how to build {0}".format(object_type)
            )

    def set_starting_money(self, money, army_name=0):
        if army_name:
            army = self._find_army(army_name)
            army.money = money
        else:
            for army in self.armies:
                army.money = money


class BadScenarioData(Exception):
    def __init__(self, message):
        print message
        super(BadScenarioData, self).__init__(message)
