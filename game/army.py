from factories.unit_factory import UnitFactory
from serializable import Serializable


class Army(Serializable):

    def __init__(self, name, unit_factory, money=0):
        Serializable.__init__(self)
        self.unit_factory = unit_factory
        self.money = money
        self.unit_table = []
        self.name = name

    def buy_unit(self, unit_name, coordinate):
        cost = self.unit_factory.get_unit_cost(unit_name)
        new_unit = 0
        if(self.money >= cost):
            self.money -= cost
            new_unit = self.unit_factory.create(unit_name, coordinate)
            self.add_unit(new_unit)
        else:
            raise InvalidArmyRequest(
                "Cannot buy unit {} with money {} cost is {}".format(
                    unit_name, self.money, cost)
            )
        return new_unit

    def add_unit(self, unit):
        self.unit_table.append(unit)

    def flat(self):
        return {
            'units': [unit.as_hash() for unit in self.unit_table],
        }

    def find_unit(self, unit_id):
        found_unit = next(unit for unit in self.unit_table if
                          id(unit) == unit_id)
        return found_unit


class InvalidArmyRequest(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)
