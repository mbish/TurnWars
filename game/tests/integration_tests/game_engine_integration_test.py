from game.game_engine import Game
from game.loader import Loader
from game.game_loader import *


def game_integration_test():
    game = load_scenario({
        "armor_data": "armor.json",
        "weapon_data": "weapon.json",
        "transport_data": "transport.json",
        "building_data": "building.json",
        "unit_data": "unit.json",
        "tile_data": "tile.json",
        "army_data": "army.json",
        "board_data": "board.json",
        "layout_data": "scenarios/basic_integration.json"
    }, Loader("./game/tests/integration_tests/resources"))
    game.do({
        'name': 'move',
        'unit': {
            'x': 1,
            'y': 0
        },
        'to': {
            'x': 2,
            'y': 0
        }
    }),
