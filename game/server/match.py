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


    # TODO: send state to new players joinning if the match has started
    def join(self, player, data={}):
        self.players[player.id_string] = player 
        if(self.number_of_players() == self.players_needed):
            self.state = 'inProgress'
            self.broadcast_game()
        else:
            if(self.number_of_players() > self.players_needed):
                player.setSpectator(True)
                player.send({
                    'type': 'matchInProgress',
                    'gameState': self.game.flat(),
                    'matchState': self.state
                })
            self.broadcast(self.metadata())

    def action(self, client, data):
        if(self.players[data['playerId']].spectating):
            client.send({
                'type': 'invalidMessage',
                'message': 'spectators can\'t take actions',
                'matchState': self.state
            })
            return
        new_game_state = self.game.do(data)
        self.change_game_state() #new_game_state)

    def change_game_state(self):
        self.broadcast_game()

    def broadcast_game(self):
        self.broadcast({
            'type': 'gameStateChange',
            'gameState': self.game.flat(),
            'matchState': self.state
        })

    def broadcast(self, message):
        for player_id in self.players:
            self.players[player_id].send(message)

    def number_of_players(self):
        return len(self.players.keys())

    def stringReceived(self, msg):
        # needs to be fleshed out
        print(msg)

    def metadata(self):
        return {
            'type': 'matchLobby',
            'matchState': self.state,
            'playersJoined': self.number_of_players(),
            'playersNeeded': self.players_needed,
            'scenario': self.scenario_name,
            'id': self.id_string
        }
