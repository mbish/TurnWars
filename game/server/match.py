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
        self.army_assignments = {}
        self.players_needed = self.game.scenario.num_armies()
        self.join(player)


    def join(self, player, data={}):
        self.players[player.id_string] = player 
        player.setSpectator(True)
        self.spectate(player)
        self.broadcast(self.metadata())

    def assignArmy(self, player, data):
        if('army' not in data):
            raise Exception('No army specified')
        army_name = data.army 
        valid_army_names = [k.name for k in self.game.scenario.armies]
        if army_name in valid_army_names:
            if army_name not in self.army_assignments.values():
                self.army_assignments[player['playerId']] = army_name
            else:
                raise Exception('That army is already assigned')
        else:
            raise Exception('That is not a valid army')

    def spectate(self, player, data={}):
        self.army_assignments[player.id_string] = 'spectate'
        player.setSpectator(True)

    def start(self, player, data):
        if(self.ready_players() == self.players_needed):
            self.state = 'inProgress'
            self.broadcast_game()


    def action(self, client, data):
        print(data)
        if(data['name'] == 'refresh'):
            if(self.state == 'inProgress'):
                client.send({
                    'type': 'matchInProgress',
                    'gameState': self.game.flat(),
                    'matchState': self.state,
                    'matchId': self.id_string
                })
            else:
                client.send(self.metadata())
            return
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
            'matchState': self.state,
            'matchId': self.id_string
        })

    def broadcast(self, message):
        for player_id in self.players:
            self.players[player_id].send(message)

    def ready_players(self):
        return len(list(filter(lambda x: x != 'spectate', self.army_assignments.values())))

    def number_of_players(self):
        return len(self.players.keys())

    def stringReceived(self, msg):
        # needs to be fleshed out
        print(msg)

    def player_id_to_name(self, playerId):
        print(self.players[playerId])
        return self.players[playerId].name

    def safe_army_list(self):
        return {self.player_id_to_name(playerId): self.army_assignments[playerId] for playerId in self.army_assignments.keys()}

    def metadata(self, metatype='matchLobby'):
        return {
            'type': metatype,
            'matchState': self.state,
            'playersJoined': self.number_of_players(),
            'playersReady': self.ready_players(),
            'playersNeeded': self.players_needed,
            'army_assignments': self.safe_army_list(),
            'scenario': self.scenario_name,
            'matchId': self.id_string
        }
