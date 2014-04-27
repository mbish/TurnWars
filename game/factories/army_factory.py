from game.army import Army
from factory import Factory, BadFactoryData, BadFactoryRequest


# TODO Tests
class ArmyFactory(Factory):

    # for now everyone gets the same unit and building factory
    # until I feel as though I need a unit factory factory
    def __init__(self, factory_data, unit_factory,
                 building_factory, army_class=Army):
        Factory.__init__(self, factory_data, army_class)
        self.unit_factory = unit_factory
        self.building_factory = building_factory
        return

    def validate_data(self, data):
        return True

    def get_unit_factory(self):
        return self.unit_factory

    def get_building_factory(self):
        return self.building_factory

    def create(self, name):
        data = self.get_data(name)
        unit_factory = self.get_unit_factory()
        building_factory = self.get_building_factory()
        return self.creation_class(name, unit_factory, building_factory)
