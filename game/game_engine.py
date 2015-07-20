from game.coordinate import Coordinate
from game.serializable import Serializable
from game.path_finder import NoPathFound, PathFinder


class Game(Serializable):

    def __init__(self, scenario, path_finder=PathFinder):
        self.scenario = scenario
        self.path_finder = path_finder(self._get_board())

    def _get_board(self):
        return self.scenario.get_board()

    def _find_army(self, army_name):
        return self.scenario._find_army(army_name)

    def _find_unit(self, unit_id):
        return self.scenario.find_unit(unit_id)

    def _uid_at(self, coordinate):
        return self.unit_at(coordinate).uid

    def unit_at(self, coordinate):
        return self.scenario.unit_at(coordinate)

    def move(self, unit, coordinate):
        if(self.scenario.space_occupied(coordinate)):
            return
        unit = self._find_unit(unit)
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
            else:
                print "no path found"
        except NoPathFound as e:
            print "exception"
            print e
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
        self.canonicalize(message)
        try:
            if(message['name'] == 'move'):
                unit = message['unit']
                move_to = Coordinate(message['to']['x'], message['to']['y'])
                self.move(unit, move_to)
            elif(message['name'] == 'attack'):
                attacker = self._find_unit(message['attacker'])
                defender = self._find_unit(message['defender'])
                self.attack(attacker, defender)
            elif(message['name'] == 'build'):
                army = self._find_army(message['army'])
                location = Coordinate(message['at']['x'], message['at']['y'])
                self.build(army, message['unit_name'], location)
            elif(message['name'] == 'end_turn'):
                army = self._find_army(message['army'])
                if(army.is_turn()):
                    army.end_turn()

        except Exception as e:
            # need to do a better job of error reporting here
            return self.flat()

        return self.flat()

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
        if 'unit' in message:
            if isinstance(message['unit'], dict):
                if('x' in message['unit'] and 'y' in message['unit']):
                    location = Coordinate(message['unit']['x'],
                                          message['unit']['y'])
                    print "got uid of unit"
                    message['unit'] = self._uid_at(location)
                elif('id' in message['unit']):
                    message['unit'] = self._find_unit(message['unit']['id'])

    def flat(self):
        return {
            'scenario': self.scenario.flat(),
        }


class InvalidGameCreation(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)
