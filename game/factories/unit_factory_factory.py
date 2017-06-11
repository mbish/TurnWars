from game.factories.armor_factory import ArmorFactory
from game.factories.transport_factory import TransportFactory
from game.factories.weapon_factory import WeaponFactory
from game.factories.unit_factory import UnitFactory
from game.factories.factory import Factory

class UnitFactoryFactory(Factory):
    
    def __init__(self, factory_data, factory_class=UnitFactory,
            transport_class=TransportFactory,
            weapon_class=WeaponFactory,
            armor_class=ArmorFactory):
        Factory.__init__(self, factory_data, factory_class)
        self.transport_class = transport_class
        self.weapon_class = weapon_class
        self.armor_class = armor_class

    def validate_data(self, data):
        if 'units' not in data:
            raise BadFactoryData("units not found for unit factory")
        if 'transports' not in data:
            raise BadFactoryData("transport not found for unit factory")
        if 'weapons' not in data:
            raise BadFactoryData("weapons not found for unit factory")
        if 'armor' not in data:
            raise BadFactoryData("armor not found for unit factory")

    def create(self, name):
        data = self.get_data(name)
        return self.creation_class(
            data['units'],
            self.transport_class(data['transports']),
            self.weapon_class(data['weapons']),
            self.armor_class(data['armor'])
        )
