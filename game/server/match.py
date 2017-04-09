from twisted.protocols import basic
import uuid
from game.game_engine import Game
from game.loader import Loader
from game.game_loader import *

class Match(basic.Int32StringReceiver):
    def __init__(self, player, scenario_name):
        self.players = {}
        self.id_string = uuid.uuid4().hex
        self.state = 'waiting'
        self.scenario_name = scenario_name
        self.game = load_scenario({
            "armor_data": "armor.json",
            "weapon_data": "weapon.json",
            "transport_data": "transport.json",
            "building_data": "building.json",
            "unit_data": "unit.json",
            "tile_data": "tile.json",
            "army_data": "army.json",
            "board_data": "board.json",
            "layout_data": "scenarios/{0}".format(scenario_name) #XXX sanatize
        }, Loader("./data/basic"))
        self.players_needed = self.game.scenario.num_armies()
        self.join(player)


    def join(self, player, data={}):
        self.players[player.id_string] = player 
        if(self.number_of_players() == self.players_needed):
            self.change_state('inProgress')
            self.broadcast_game()
        else:
            self.broadcast({
                'state': self.state,
                'playersJoined': self.number_of_players(),
                'playersNeeded': self.players_needed,
                'scenario': self.scenario_name
            })

    def action(self, client, data):
        self.game.do(data)

    def change_state(self, new_state):
        self.state = new_state
        self.broadcast({
            'type': 'stateChange',
            'newState': new_state
        })

    def broadcast_game(self):
        self.broadcast(self.game.flat())

    def broadcast(self, message):
        for player_id in self.players:
            self.players[player_id].send(message)

    def number_of_players(self):
        return len(self.players.keys())

    def stringReceived(self, msg):
        # needs to be fleshed out
        print(msg)
