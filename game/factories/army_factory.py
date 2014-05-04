from copy import deepcopy
from game.army import Army
from game.factories.factory import Factory, BadFactoryData, BadFactoryRequest


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

    def _get_unit_factory(self, name):
        unit_factory = deepcopy(self.unit_factory)
        unit_factory.army = name
        return unit_factory

    def _get_building_factory(self):
        return self.building_factory

    def create(self, name):
        unit_factory = self._get_unit_factory(name)
        building_factory = self._get_building_factory()
        return self.creation_class(name, unit_factory, building_factory)
