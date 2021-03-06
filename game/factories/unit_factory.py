from game.unit import Unit
from game.coordinate import Coordinate
from game.factories.factory import Factory
from game.exceptions import BadFactoryRequest, BadFactoryData


class UnitFactory(Factory):

    def __init__(self, factory_data,
                 transport_factory, weapon_factory,
                 armor_factory, unit_class=Unit):
        self.transport_factory = transport_factory
        self.armor_factory = armor_factory
        self.weapon_factory = weapon_factory
        Factory.__init__(self, factory_data, unit_class)

    def validate_data(self, data):
        if not self.transport_factory.can_make(data['transport']):
            raise BadFactoryData("transport_factory cannot make transport")
        elif not self.weapon_factory.can_make(data['weapon']):
            raise BadFactoryData("weapon_factory cannot make weapon")
        elif not self.armor_factory.can_make(data['armor']):
            raise BadFactoryData("armor_factory cannot make weapon")
        elif 'cost' not in data:
            raise BadFactoryData("cost not found")
        return True

    def create(self, name, army, coordinate=Coordinate(0, 0)):
        data = self.get_data(name)
        return self.creation_class(
            name,
            self.transport_factory.create(data['transport']),
            self.weapon_factory.create(data['weapon']),
            self.armor_factory.create(data['armor']),
            coordinate, army)

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

    def flat(self):
        return {
            'armor': self.armor_factory.flat(),
            'weapon': self.weapon_factory.flat(),
            'transport': self.transport_factory.flat(),
            'units': self.factory_data
        }
