from game.serializable import Serializable
from factory import Factory
from game.weapon import Weapon


class WeaponFactory(Factory):

    def __init__(self, factory_data, weapon_class=Weapon):
        Factory.__init__(self, factory_data, weapon_class)
        return

    def validate_data(self, data):
        if('uses' not in data or
                'attack_strength' not in data):
            return False
        else:
            return True

    def create(self, name):
        data = self.get_data(name)
        if('non_targetables' in data):
            return self.creation_class(name, data['uses'],
                                       data['attack_strength'],
                                       data['non_targetables'])
        else:
            return self.creation_class(name, data['uses'],
                                       data['attack_strength'])
