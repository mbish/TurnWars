from game.unit import Unit
from game.coordinate import Coordinate
from factory import Factory

class UnitFactory(Factory):
    transport_factory = 0
    weapon_factory = 0
    armor_factory = 0
    army = ''
    
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
               self.armor_factory.can_make(data['armor'])):
            return True
        else:
            return False

    def create(self, name, coordinate=Coordinate(0,0)):
        data = self.get_data(name)
        return self.creation_class(
                name,
                self.transport_factory.create(data['transport']),
                self.weapon_factory.create(data['weapon']),
                self.armor_factory.create(data['armor']),
                coordinate,
                self.army)
