from game.serializable import Serializable


class Army(Serializable):

    def __init__(self, name, unit_factory, building_factory, money=0):
        Serializable.__init__(self)
        self.unit_factory = unit_factory
        self.building_factory = building_factory
        self.money = money
        self.unit_table = []
        self.name = name
        self.buildings = []
        self.turn = 0

    def num_units(self):
        return len(self.unit_table)

    def num_buildings(self):
        return len(self.buildings)

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
            new_unit = self.build_unit(unit_name, coordinate)
        else:
            raise InvalidArmyRequest(
                "Cannot buy unit {0}".format(
                    unit_name, self.money, cost)
            )
        return new_unit

    def build_building(self, building_name, coordinate):
        new_building = self.building_factory.create(building_name, coordinate)
        self.add_building(new_building)
        return new_building

    def build_unit(self, unit_name, coordinate):
        new_unit = self.unit_factory.create(unit_name, coordinate)
        self.add_unit(new_unit)
        return new_unit

    def can_build(self, cost, coordinate):
        result = True
        if(not self.turn):
            result = False
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

    def add_building(self, building):
        self.buildings.append(building)

    def find_unit(self, unit_id):
        found_unit = next(unit for unit in self.unit_table if
                          unit.uid == unit_id)
        return found_unit

    def get_unit_at(self, coordinate):
        found_unit = next(unit for unit in self.unit_table if
                          unit.at(coordinate))
        return found_unit
        return (coordinate in
                [unit.coordinate for unit in self.unit_table])

    def income(self):
        amount = 0
        for building in self.buildings:
            amount += building.get_revenue()
        return amount

    def take_turn(self):
        for unit in self.unit_table:
            unit.reset()
        self.money += self.income()
        self.turn = 1

    def end_turn(self):
        self.turn = 0
        return

    def is_turn(self):
        return self.turn

    def flat(self):
        return {
            'units': [unit.flat() for unit in self.unit_table],
            'buildings': [building.flat() for building in self.buildings]
        }


class InvalidArmyRequest(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)
