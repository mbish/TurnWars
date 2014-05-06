from game.loader import Loader
from game.factories.armor_factory import ArmorFactory
from game.factories.weapon_factory import WeaponFactory 
from game.factories.unit_factory import UnitFactory
from game.factories.building_factory import BuildingFactory
from game.factories.tile_factory import TileFactory
from game.factories.army_factory import ArmyFactory
from game.factories.board_factory import BoardFactory
from game.factories.scenario_builder import ScenarioBuilder
from game.factories.transport_factory import TransportFactory


def bootstrap_game():
    factory_loader = Loader()
    armor_data = factory_loader.load_from_file("data/armor.json")
    weapon_data = factory_loader.load_from_file("data/weapon.json")
    transport_data = factory_loader.load_from_file("data/transport.json")
    building_data = factory_loader.load_from_file("data/building.json")
    unit_data = factory_loader.load_from_file("data/unit.json")
    tile_data = factory_loader.load_from_file("data/tile.json")
    army_data = factory_loader.load_from_file("data/army.json")
    board_data = factory_loader.load_from_file("data/board.json")

    armor_factory = ArmorFactory(armor_data)
    weapon_factory = WeaponFactory(weapon_data)
    transport_factory = TransportFactory(transport_data)
    building_factory = BuildingFactory(building_data)
    unit_factory = UnitFactory(unit_data, transport_factory, weapon_factory,
                               armor_factory)
    tile_factory = TileFactory(tile_data)
    army_factory = ArmyFactory(army_data, unit_factory,
                               building_factory)
    board_factory = BoardFactory(board_data, tile_factory)
