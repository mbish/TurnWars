from game.serializable import Serializable


class Scenario(Serializable):

    def __init__(self, on_board_check, army_factory):
        self.on_board_check = on_board_check
        self.armies = []
        self.army_factory = army_factory

    def num_armies(self):
        return len(self.armies)

    def add_army(self, name):
        army = self.army_factory.create(name)
        if(len(self.armies) == 0):
            army.take_turn()
        self.armies.append(army)
        return len(self.armies)

    def _find_army(self, army_name):
        army = next(army for army in self.armies if army.name == army_name)
        return army

    def unit_at(self, coordinate):
        for army in self.armies:
            unit = army.unit_at(coordinate)
            if(unit):
                return unit

    def add_unit(self, army_name, data):
        data.object_type = "unit"
        self._add_object(army_name, data)

    def add_building(self, army_name, data):
        data.object_type = "building"
        self._add_object(army_name, data)

    def _add_object(self, army_name, data):
        army = self._find_army(army_name)
        if(self.on_board_check(data.coordinate)):
            self._build_type(army, data)
        else:
            raise BadScenarioData(
                "Cannot place {0} at {1}".format(
                    data.name,
                    data.coordinate.flat()))

    def space_occupied(self, coordinate):
        for army in self.armies:
            if(army.has_unit_at(coordinate)):
                return True

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

    def _build_type(self, army, data):
        if(data.object_type == "unit"):
            return army.build_unit(data.name, data.coordinate)
        elif(data.object_type == "building"):
            return army.build_building(data.name, data.coordinate)
        else:
            raise BadScenarioData(
                "Do not know how to build {0}".format(data.object_type))

    def set_starting_money(self, money, army_name=0):
        if(army_name):
            army = self._find_army(army_name)
            army.money = money
        else:
            for army in self.armies:
                army.money = money


class BadScenarioData(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
