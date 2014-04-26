from factories.unit_factory import UnitFactory
from serializable import Serializable


class Army(Serializable):

    def __init__(self, name, unit_factory, buildings, money=0):
        Serializable.__init__(self)
        self.unit_factory = unit_factory
        self.money = money
        self.unit_table = []
        self.name = name
        self.buildings = buildings
        self.turn = 0

    def has_building_at(self, coordinate):
        return (coordinate in
                [building.coordinate for building in self.buildings])

    def _get_building_at(self, coordinate):
        return next(building for building in
                    self.buildings if building.coordinate == coordinate)

    def has_unit_at(self, coordinate):
        return (coordinate in
                [unit.coordinate for unit in self.unit_table])

    def buy_unit(self, unit_name, coordinate):
        cost = self.unit_factory.get_unit_cost(unit_name)
        new_unit = 0
        if(self.can_build(cost, coordinate)):
            self.money -= cost
            new_unit = self.unit_factory.create(unit_name, coordinate)
            self.add_unit(new_unit)
        else:
            raise InvalidArmyRequest(
                "Cannot buy unit {} with money {} cost is {}".format(
                    unit_name, self.money, cost)
            )
        return new_unit

    def can_build(self, cost, coordinate):
        result = True
        if(self.money < cost):
            result = False
        if(not self.has_building_at(coordinate)):
            result = False

        return result

    def unit_info(self, unit_type):
        return self.unit_factory.full_unit_info(unit_type)

    def equipment_info(self, unit_type, equipment):
        return self.unit_factory.equipment_info(unit_type, equipment)

    def add_unit(self, unit):
        self.unit_table.append(unit)

    def find_unit(self, unit_id):
        found_unit = next(unit for unit in self.unit_table if
                          unit.uid == unit_id)
        return found_unit

    def take_turn(self):
        self.turn = 1

    def end_turn(self):
        for unit in self.unit_table:
            unit.reset()

    def is_turn(self):
        return self.turn

    def flat(self):
        return {
            'units': [unit.as_hash() for unit in self.unit_table],
        }


class InvalidArmyRequest(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)
