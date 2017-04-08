from game.serializable import Serializable
from game.factories.factory import Factory
from game.coordinate import Coordinate
from game.building import Building
from game.exceptions import BadFactoryData


class BuildingFactory(Factory):

    def __init__(self, factory_data, building_class=Building):
        Factory.__init__(self, factory_data, building_class)

    def validate_data(self, data):
        if('buildable_units' not in data):
            raise BadFactoryData("buildable_units not found")
        elif('revenue' not in data):
            raise BadFactoryData("revenue not found")
        else:
            return True

    def create(self, name, coordinate=Coordinate(0, 0)):
        data = self.get_data(name)
        return self.creation_class(name, data['revenue'],
                                   data['buildable_units'], coordinate)
