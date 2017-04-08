from game.serializable import Serializable
from game.factories.factory import Factory
from game.exceptions import BadFactoryData
from game.weapon import Weapon


class WeaponFactory(Factory):

    def __init__(self, factory_data, weapon_class=Weapon):
        Factory.__init__(self, factory_data, weapon_class)
        return

    def validate_data(self, data):
        if 'uses' not in data:
            raise BadFactoryData("uses not found")
        if 'attack_strength' not in data:
            raise BadFactoryData("attack_strength not found")
        else:
            return True

    def create(self, name):
        data = self.get_data(name)
        if('range' not in data):
            data['range'] = 1
        if('uses_per_turn' not in data):
            data['uses_per_turn'] = 1
        if('non_targetables' in data):
            return self.creation_class(name, data['uses'],
                                       data['attack_strength'],
                                       data['range'],
                                       data['uses_per_turn'],
                                       data['non_targetables'])
        else:
            return self.creation_class(name, data['uses'],
                                       data['attack_strength'],
                                       data['range'],
                                       data['uses_per_turn'])
