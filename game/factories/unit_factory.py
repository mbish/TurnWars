from game.unit import Unit
from game.coordinate import Coordinate
from game.factories.factory import Factory, BadFactoryRequest


class UnitFactory(Factory):

    def __init__(self, factory_data,
                 transport_factory, weapon_factory,
                 armor_factory, army, unit_class=Unit):
        self.transport_factory = transport_factory
        self.armor_factory = armor_factory
        self.weapon_factory = weapon_factory
        self.army = army
        Factory.__init__(self, factory_data, unit_class)

    def validate_data(self, data):
        if(self.transport_factory.can_make(data['transport']) and
           self.weapon_factory.can_make(data['weapon']) and
           self.armor_factory.can_make(data['armor']) and
           'cost' in data):
            return True
        else:
            return False

    def create(self, name, coordinate=Coordinate(0, 0)):
        data = self.get_data(name)
        return self.creation_class(
            name,
            self.transport_factory.create(data['transport']),
            self.weapon_factory.create(data['weapon']),
            self.armor_factory.create(data['armor']),
            coordinate,
            self.army)

    def get_factory(self, factory):
        result = self.armor_factory
        if(factory == "armor"):
            result = self.armor_factory
        elif(factory == "weapon"):
            result = self.weapon_factory
        elif(factory == "transport"):
            result = self.transport_factory
        else:
            raise BadFactoryRequest("Could not find factory for {0}".format(
                factory))

        return result

    def get_unit_cost(self, name):
        data = self.get_data(name)
        return data['cost']

    def equipment_info(self, name, equipment):
        unit_data = self.get_data(name)
        equipment_name = unit_data[equipment]
        equipment_data = (self.get_factory(equipment).
                          get_data(equipment_name))
        equipment_data['name'] = equipment_name
        return equipment_data

    def full_unit_info(self, name):
        unit_data = self.get_data(name)
        for equipment in ['transport', 'weapon', 'armor']:
            unit_data[equipment] = self.equipment_info(name, equipment)

        return unit_data
