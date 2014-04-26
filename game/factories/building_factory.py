from game.serializable import Serializable
from factory import Factory
from game.coordinate import Coordinate
from game.building import Building


class BuildingFactory(Factory):

    def __init__(self, factory_data, building_class=Building):
        Factory.__init__(self, factory_data, building_class)

    def validate_data(self, data):
        if('buildable_units' not in data):
            return False
        else:
            return True

    def create(self, name, coordinate=Coordinate(0, 0)):
        data = self.get_data(name)
        return self.creation_class(name, data['buildable_units'], coordinate)
