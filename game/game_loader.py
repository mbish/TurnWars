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
from game.coordinate import Coordinate
from game.game_engine import Game


def load_scenario(scenario_metadata, loader):
    armor_data = loader.load(scenario_metadata["armor_data"])
    weapon_data = loader.load(scenario_metadata["weapon_data"])
    transport_data = loader.load(scenario_metadata["transport_data"])
    building_data = loader.load(scenario_metadata["building_data"])
    unit_data = loader.load(scenario_metadata["unit_data"])
    tile_data = loader.load(scenario_metadata["tile_data"])
    army_data = loader.load(scenario_metadata["army_data"])
    board_data = loader.load(scenario_metadata["board_data"])
    layout_data = loader.load(scenario_metadata["layout_data"])

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

    scenario = ScenarioBuilder(board_factory, army_factory)
    scenario.set_board(layout_data['board'])
    for army in layout_data['armies']:
        army_name = army['name']
        scenario.add_army(army_name)
        for unit in army['units']:
            scenario.add_unit(army_name, unit)
        for building in army['buildings']:
            print "adding building"
            print building
            scenario.add_building(army_name, building)

        scenario.set_starting_money(army['money'], army_name)

    scenario = scenario.pop_instance()
    return Game(scenario)
