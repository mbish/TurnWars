from game.loader import Loader
from game.factories.unit_factory_factory import UnitFactoryFactory
from game.factories.building_factory import BuildingFactory
from game.factories.tile_factory import TileFactory
from game.factories.army_factory import ArmyFactory
from game.factories.board_factory import BoardFactory
from game.factories.scenario_builder import ScenarioBuilder
from game.coordinate import Coordinate
from game.game_engine import Game
from game.path_finder import PathFinder
from game.exceptions import NoPathFound


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

    building_factory = BuildingFactory(building_data)

    unit_factory_factory = UnitFactoryFactory({
        'dragon': {
            'units': unit_data,
            'transports': transport_data,
            'weapons': weapon_data,
            'armor': armor_data
        },
        'salamander': {
            'units': unit_data,
            'transports': transport_data,
            'weapons': weapon_data,
            'armor': armor_data
        },
    })

    tile_factory = TileFactory(tile_data)
    army_factory = ArmyFactory(army_data, unit_factory_factory,
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
            scenario.add_building(army_name, building)

        scenario.set_starting_money(army['money'], army_name)

    scenario = scenario.pop_instance()

    # I don't love this, it's sort of like glue
    path_finder = PathFinder(scenario.get_board())
    return Game(scenario, path_finder)
