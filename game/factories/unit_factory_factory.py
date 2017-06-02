from game.factories.armor_factory import ArmorFactory
from game.factories.transport_factory import TransportFactory
from game.factories.weapon_factory import WeaponFactory
from game.factories.unit_factory import UnitFactory
from game.factories.factory import Factory

class UnitFactoryFactory(Factory):
    
    def __init__(self, factory_data, factory_class=UnitFactory):
        Factory.__init__(self, factory_data, factory_class)

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
        self.creation_class(
            data['units'],
            TransportFactory(data['transports']),
            WeaponFactory(data['weapons']),
            ArmorFactory(data['armor'])
        )
        return
