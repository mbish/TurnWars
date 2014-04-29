from game.serializable import Serializable
from game.factories.factory import Factory
from game.armor import Armor


class ArmorFactory(Factory):

    def __init__(self, factory_data, armor_class=Armor):
        Factory.__init__(self, factory_data, armor_class)

    def validate_data(self, data):
        if('starting_health' not in data):
            return False
        else:
            return True

    def create(self, name):
        data = self.get_data(name)
        return self.creation_class(name, data['starting_health'])
