from unit_factory import UnitFactory

class MockUnit:
    name = ''
    transport = ''
    weapon = ''
    armor = ''
    coordinate = ''
    army = ''

    def __init__(self, name, transport, weapon, armor, coordinate, army):
        self.name = name
        self.transport = transport
        self.weapon = weapon
        self.armor = armor
        self.coordinate = coordinate
        self.army = army

    def get_value(self):
        return "{} {} {} {} {} {}".format(
                self.name,
                self.weapon,
                self.transport,
                self.armor,
                self.coordinate,
                self.army,
        )
        

class MockFactory:
    def create(self, name):
        return name
    def can_make(self):
        return False

class MockTransportFactory(MockFactory):
    def can_make(self, name):
       return name == 'foot' 

class MockWeaponFactory(MockFactory):
    def can_make(self, name):
       return name == 'sword' 

class MockArmorFactory(MockFactory):
    def can_make(self, name):
       return name == 'cloth' 

def validate_test():
    factory_data = {
        'footman': {
            'transport': 'foot',
            'armor': 'cloth',
            'weapon': 'sword',
        },
        'snowman': {
            'transport': 'ice',
            'armor': 'cloth',
            'weapon': 'sword',
        },
        'goman': {
            'transport': 'foot',
            'armor': 'paper',
            'weapon': 'sword',
        },
        'toeman': {
            'transport': 'foot',
            'armor': 'cloth',
            'weapon': 'toe',
        }
    }
    factory = UnitFactory({}, MockTransportFactory(),
                          MockWeaponFactory(), MockArmorFactory(),
                          'dragon', MockUnit)
    assert factory.validate_data(factory_data['footman']) == True
    assert factory.validate_data(factory_data['snowman']) == False
    assert factory.validate_data(factory_data['goman']) == False
    assert factory.validate_data(factory_data['toeman']) == False

def create_test():
    factory_data = {
        'footman': {
            'transport': 'foot',
            'armor': 'cloth',
            'weapon': 'sword',
        },
    }
    factory = UnitFactory(factory_data, MockTransportFactory(),
                          MockWeaponFactory(), MockArmorFactory(),
                          'dragon', MockUnit)
    unit = factory.create('footman', 'middle')
    assert unit.get_value() == 'footman sword foot cloth middle dragon'
    unit = factory.create('footman')
    assert unit.coordinate.x == 0
    assert unit.coordinate.y == 0
