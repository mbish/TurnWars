from time import time
from game.coordinate import Coordinate
from game.serializable import Serializable
from game.exceptions import NoPathFound


class Game(Serializable):

    def __init__(self, scenario, path_finder, timer=time):
        self.scenario = scenario
        self.path_finder = path_finder
        self.timer = timer
        self.players = []

    def _get_board(self):
        return self.scenario.get_board()

    def _find_army(self, army_name):
        return self.scenario._find_army(army_name)

    def _find_unit(self, unit_id):
        return self.scenario.find_unit(unit_id)

    def _uid_at(self, coordinate):
        return self.unit_at(coordinate).uid

    def unit_at(self, coordinate):
        try:
            return self.scenario.unit_at(coordinate)
        except StopIteration:
            return None

    def assignArmy(self, playerId):
        self.players.append(playerId)



    # this does need to be a full unit any uid lookup
    # should be done outside of this function
    def move(self, unit, coordinate):
        if(self.scenario.space_occupied(coordinate)):
            return
        army = self.scenario._find_army(unit.army)
        if(not army.is_turn()):
            return
        transport = army.equipment_info(unit.name, 'transport')
        cost_table = transport['cost_table']
        try:
            path = self.path_finder.get_path(cost_table,
                                             unit.get_coordinate(),
                                             coordinate)
            if(self.path_finder.path_cost(path, cost_table) <=
               unit.movement_range()):
                unit.move(coordinate, len(path))
        except NoPathFound as e:
            print(e)
            return

    def attack(self, attacker, defender):
        attacking_army = self._find_army(attacker.army)
        if(not attacking_army.is_turn()):
            return
        if(attacker.army != defender.army):
            attacker.attack(defender)

    def build(self, army, unit_name, location):
        if(not self.scenario.space_occupied(location)):
            army.buy_unit(unit_name, location)

    def do(self, message):
        try:
            if('playerId' not in message):
                raise Exception("No player ID in message")
            self.canonicalize(message)
            if(message['name'] == 'move'):
                unit = message['unit']
                move_to = Coordinate(message['to']['x'], message['to']['y'])
                self.move(unit, move_to)
            elif(message['name'] == 'attack'):
                attacker = message['attacker']
                defender = message['defender']
                self.attack(attacker, defender)
            elif(message['name'] == 'build'):
                army = self._find_army(message['army'])
                location = Coordinate(message['at']['x'], message['at']['y'])
                self.build(army, message['unit_name'], location)
            elif(message['name'] == 'end_turn'):
                army = self._find_army(message['army'])
                if(army.is_turn()):
                    army.end_turn()
                self.scenario.next_army()

        except Exception as e:
            # need to do a better job of error reporting here
            print(e)
            return self.flat()

        return self.flat()

    def playerNumber(self, playerId):
        print(self.players)
        return self.players.index(playerId)

    # This is really a utility function and may get split out from the
    # truely model-modifying functions above
    def tiles_in_range(self, unit):
        army = self._find_army(unit.army)
        transport = army.equipment_info(unit.name, 'transport')
        cost_table = transport['cost_table']
        spaces_left = unit.get_spaces_left()
        return self.path_finder.tiles_in_range(self._get_board(),
                                               cost_table,
                                               unit.get_coordinate(),
                                               spaces_left)

    # maps between various verions of the message protocol
    def canonicalize(self, message):
        if('type' in message and 'name' not in message):
            message['name'] = message['type']
            del message['type']
        for unit_key in ['unit', 'attacker', 'defender']:
            if unit_key in message:
                if isinstance(message[unit_key], dict):
                    if('x' in message[unit_key] and 'y' in message[unit_key]):
                        location = Coordinate(message[unit_key]['x'],
                                              message[unit_key]['y'])
                        message[unit_key] = self.unit_at(location)
                    elif('id' in message[unit_key]):
                        message[unit_key] = self._find_unit(message[unit_key]['id'])
                if(message[unit_key].army != self.scenario.armies[self.playerNumber(message['playerId'])].name):
                    raise Exception("Player not in control of army")

    def flat(self):
        return {
            'scenario': self.scenario.flat(),
            'timestamp': int(self.timer())
        }
