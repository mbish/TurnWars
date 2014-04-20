from weapon_factory import WeaponFactory
from nose.tools import assert_raises

class MockClass:
    uses = 0
    attack_strength = 0
    name = ''
    non_targetables = {}
    def __init__(self, name, uses, attack_strength, non_targetables={}):
        self.name = name
        self.uses = uses
        self.attack_strength = attack_strength
        self.non_targetables = non_targetables

    def get_value(self):
        return "{} {} {} {}".format(self.name, self.uses, 
                                    self.attack_strength, 
                                    len(self.non_targetables))

def validation_test():
    factory_data = {
        'cannon': {
            'uses': 3,
            'attack_strength': 10,
            'non_targetables': {},
        },
        'no_uses': {
            'attack_strength': 2,
            'non_targetables': {},
        },
        'no_strength': {
            'uses': 1,
            'non_targetables': {},
        },
        'no_list': {
            'uses': 20,
            'attack_strength': 22,
        },
    }
    factory = WeaponFactory({}, MockClass)
    assert factory.validate_data(factory_data['cannon']) == True
    assert factory.validate_data(factory_data['no_uses']) == False
    assert factory.validate_data(factory_data['no_strength']) == False
    assert factory.validate_data(factory_data['no_list']) == True

def create_test():
    factory_data = {
        'cannon': {
            'uses': 3,
            'attack_strength': 10,
            'non_targetables': {},
        },
        'rod': {
            'uses': 20,
            'attack_strength': 22,
        },
    }
    factory = WeaponFactory(factory_data, MockClass)
    weapon = factory.create('cannon')
    assert weapon.get_value() == 'cannon 3 10 0'
    weapon = factory.create('rod')
    assert weapon.get_value() == 'rod 20 22 0'
