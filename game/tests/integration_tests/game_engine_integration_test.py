from game.game_engine import Game
from game.loader import Loader
from game.game_loader import *

def test_game():
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
    game.assignArmy('test-player')
    game.assignArmy('test-player2')
    return game


def out_of_bounds_test():
    game = test_game()
    game.do({
        'name': 'move',
        'unit': {
            'x': 1,
            'y': 0
        },
        'to': {
            'x': 1,
            'y': -1
       }
    })
    assert game.unit_at(Coordinate(1, 0)).name == 'footman'

def onto_buildings_test():
    game = test_game()
    game.do({
        'playerId': 'test-player',
        'name': 'move',
        'unit': {
            'x': 1,
            'y': 0
        },
        'to': {
            'x': 0,
            'y': 0
        }
    })
    assert game.unit_at(Coordinate(0, 0)).name == 'footman'

def double_move_test():
    game = test_game()
    game.do({
        'playerId': 'test-player',
        'name': 'move',
        'unit': {
            'x': 1,
            'y': 0
        },
        'to': {
            'x': 2,
            'y': 1
        }
    })
    assert game.unit_at(Coordinate(2, 1)).name == 'footman'
    game.do({
        'playerId': 'test-player',
        'name': 'move',
        'unit': {
            'x': 2,
            'y': 1
        },
        'to': {
            'x': 3,
            'y': 1
        }
    })
    assert game.unit_at(Coordinate(2, 1)).name == 'footman'
    assert game.unit_at(Coordinate(3, 1)) == None

def out_of_turn_test():
    game = test_game()
    game.do({
        'name': 'move',
        'unit': {
            'x': 10,
            'y': 11
        },
        'to': {
            'x': 10,
            'y': 10
        }
    })
    assert game.unit_at(Coordinate(10, 10)) == None


def unit_collision_test():
    game = test_game()
    game.do({
        'name': 'move',
        'unit': {
            'x': 5,
            'y': 5
        },
        'to': {
            'x': 6,
            'y': 5
        }
    })
    assert game.unit_at(Coordinate(5, 5)).name == "footman"
    assert game.unit_at(Coordinate(6, 5)).name == "footman"


def unit_attack_test():
    game = test_game()
    game.do({
        'playerId': 'test-player',
        'name': 'attack',
        'army': 'dragon',
        'attacker': {
            'x': 5,
            'y': 5
        },
        'defender': {
            'x': 6,
            'y': 5
        }
    })
    assert game.unit_at(Coordinate(6, 5)).get_health() == 9
