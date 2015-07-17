from game.game_loader import *
from nose.tools import assert_raises, eq_


class MockLoader:
    def __init__(self):
        return

    def load(self, val):
        return val


def test_scenario():
    return {
        'armor_data': {
            'plate': {
                'starting_health': 10
            }
        },
        'weapon_data': {
            'sword': {
                'uses': 1,
                'uses_per_turn': 1,
                'attack_strength': 1
            },
            'flack': {
                'uses': 10,
                'attack_strength': 1,
                'non_targetables': [
                    'foot'
                ]
            }
        },
        'transport_data': {
            'foot': {
                'spaces_per_turn': 2
            },
            'tires': {
                'spaces_per_turn': 5
            }
        },
        'building_data': {
            'fort': {
                'buildable_units': [
                    'footman'
                ],
                'revenue': 100,
            }
        },
        'unit_data': {
            'footman': {
                'transport': 'foot',
                'weapon': 'sword',
                'armor': 'plate',
                'cost': 100
            }
        },
        'tile_data': {
            'grass': {
                'non_passables': [],
                'events': [],
                'cover': 0
            },
            'rocks': {
                'non_passables': ['tires'],
                'events': [],
                'cover': 0
            }
        },
        'army_data': {
        },
        'board_data': {
            'basic': {
                'tiles': [
                    ['grass', 'grass', 'grass', 'grass', 'grass', 'grass'],
                    ['grass', 'grass', 'grass', 'grass', 'grass', 'grass'],
                    ['grass', 'grass', 'grass', 'grass', 'grass', 'grass'],
                    ['grass', 'grass', 'grass', 'grass', 'grass', 'grass']
                ]
            }
        },
        'layout_data': {
            'board': 'basic',
            'armies': [
                {
                    'name': 'dragon',
                    'units': [{
                        'name': 'footman',
                        'x': 1,
                        'y': 0
                    }],
                    'buildings': [
                    ],
                    'money': 1000
                },
                {
                    'name': 'salamander',
                    'units': [{
                        'name': 'footman',
                        'x': 0,
                        'y': 0
                    }],
                    'buildings': [
                    ],
                    'money': 1000
                }
            ],
        }
    }


def load_scenario_test():
    load_scenario(test_scenario(), MockLoader())
    return


def no_tiles_test():
    scenario = test_scenario()
    scenario['board_data']['basic'].pop("tiles")
    assert_raises(Exception, load_scenario, scenario, MockLoader())
    return


def bad_tiles_test():
    scenario = test_scenario()
    scenario['board_data']['basic'].pop("tiles")
    scenario['board_data']['basic']['tiles'] = [
        ['bad', 'grass'],
    ]
    assert_raises(Exception, load_scenario, scenario, MockLoader())
    return


def missing_factories_test():
    for factory_key in ['weapon_data', 'army_data', 'board_data',
                        'layout_data', 'armor_data', 'transport_data',
                        'building_data', 'unit_data', 'tile_data']:
        scenario = test_scenario()
        scenario.pop(factory_key)
        assert_raises(Exception, load_scenario, scenario, MockLoader())
    return


def missing_layout_test():
    scenario = test_scenario()
    scenario['layout_data'].pop('board')
    assert_raises(Exception, load_scenario, scenario, MockLoader())

    scenario = test_scenario()
    scenario['layout_data']['board'] = 'advanced'
    assert_raises(Exception, load_scenario, scenario, MockLoader())

    scenario = test_scenario()
    scenario['layout_data']['armies'][0]['units'] = []
    assert_raises(Exception, load_scenario, scenario, MockLoader())

    scenario = test_scenario()
    scenario['layout_data']['armies'][1]['units'] = []
    assert_raises(Exception, load_scenario, scenario, MockLoader())

    scenario = test_scenario()
    scenario['layout_data']['armies'][0]['buildings'] = [{
        'name': 'fort',
        'x': 1,
        'y': 0,
    }]
    scenario['layout_data']['armies'][0]['units'] = []
    load_scenario(scenario, MockLoader())
