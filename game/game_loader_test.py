from game.game_loader import GameLoader


class MockProduct:
    def __init__(self, name):
        self.name = name


class MockFactory:
    def __init__(self, data, name="none_given", creation_class=MockProduct):
        self.name = name
        self.data = data


class MockUnitFactory:
    def __init__(self, data, transport_factory, weapon_factory, armor_factory,
                 name="none_given", creation_class=MockProduct):
        self.transport_factory = transport_factory
        self.weapon_factory = weapon_factory
        self.armor_factory = armor_factory
        self.name = name
        self.creation_class = creation_class
        self.data = data


def test_gameloader():
    loader = GameLoader()
    loader.set_metadata("transport", MockFactory, MockProduct, {},
                        "this is a transport factory")
    loader.set_metadata("armor", MockFactory, MockProduct, {},
                        "this is an armor factory")
    loader.set_metadata("weapon", MockFactory, MockProduct, {},
                        "this is an weapon factory")
    loader.set_metadata("unit", MockUnitFactory, MockProduct,
                        {
                            "transport_factory": "transport", 
                            "armor_factory": "armor",
                            "weapon_factory": "weapon",
                        },
                        "this is a unit factory")
    return loader


def set_metadata_test():
    loader = test_gameloader()
    assert loader.metadata["transport"].get_data() == (
        "this is a transport factory")
    assert loader.metadata["transport"].get_creation_class() == (
        MockProduct)
    assert loader.metadata["transport"].get_dependencies() == (
        {})
    assert loader.metadata["transport"].get_factory_class() == (
        MockFactory)
    assert loader.metadata["unit"].get_dependencies() == {
        "transport_factory": "transport",
        "armor_factory": "armor",
        "weapon_factory": "weapon",
    }


def build_factory_test():
    loader = test_gameloader()
    unit_factory = loader._build_factory("unit")
    assert unit_factory.transport_factory.data == "this is a transport factory"
    assert isinstance(unit_factory, MockUnitFactory)
