from game.factories.army_factory import ArmyFactory


class MockArmy:
    def __init__(self, name, unitf, buildingf):
        self.name = "{0} with {1} and {2}".format(name, unitf.name, buildingf)


class MockUnitFactory:
    def __init__(self, name):
        self.name = name


def test_factory():
    factory_data = {
        'dragon': 1,
    }
    unitf = MockUnitFactory("unit factory")
    buildingf = "building factory"
    factory = ArmyFactory(factory_data, unitf, buildingf, MockArmy)
    return factory


def validate_data_test():
    factory = test_factory()
    assert factory.validate_data(factory.factory_data['dragon'])


def get_unit_factory_test():
    factory = test_factory()
    assert factory._get_unit_factory("new").army == "new"
    assert factory._get_unit_factory("new").name == "unit factory"


def get_buliding_factory_test():
    factory = test_factory()
    assert factory._get_building_factory() == "building factory"


def create_test():
    factory = test_factory()
    army = factory.create('dragon')
    assert army.name == "dragon with unit factory and building factory"
