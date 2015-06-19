from game.coordinate import Coordinate
from game.serializable import Serializable
from game.path_finder import NoPathFound, PathFinder


class Game(Serializable):

    def __init__(self, scenario, path_finder=PathFinder):
        self.path_finder = path_finder
        self.scenario = scenario

    def _get_board(self):
        return self.scenario.get_board()

    def _find_unit(self, unit_id):
        return self.scenario.find_unit(unit_id)

    def _uid_at(self, coordinate):
        return self.unit_at(coordinate).uid

    def unit_at(self, coordinate):
        return self.scenario.unit_at(coordinate)

    def move(self, unit, coordinate):
        if(self.scenario.space_occupied(coordinate)):
            return
        army = self.scenario._find_army(unit.army)
        transport = army.equipment_info(unit.name, 'transport')
        movement_cost = transport['movement_cost']
        try:
            path = self.path_finder.get_path(unit.get_coordinate(),
                                             movement_cost, coordinate)
            if(self.path_finder.path_cost(self._get_board(),
                                          path, movement_cost) <=
               unit.movement_range()):
                unit.move(coordinate, len(path))
        except NoPathFound:
            return

    def attack(self, attacker, defender):
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
                army = self.scenario._find_army(message['army_name'])
                location = Coordinate(message['at']['x'], message['at']['y'])
                self.build(army, message['unit_name'], location)
            elif(message['name'] == 'end_turn'):
                army = self.scenario._find_army(message['army_name'])
                if(army.is_turn()):
                    army.end_turn()

        except Exception:
            return self.flat()

        return self.flat()

    # This is really a utility function and may get split out from the
    # truely model-modifying functions above
    def tiles_in_range(self, unit):
        army = self.scenario._find_army(unit.army)
        transport = army.equipment_info(unit.name, 'transport')
        movement_cost = transport['movement_cost']
        spaces_left = unit.get_spaces_left()
        return self.path_finder.tiles_in_range(self._get_board(),
                                               movement_cost,
                                               unit.get_coordinate(),
                                               spaces_left)

    # maps between various verions of the message protocol
    def canonicalize(self, message):
        if 'unit' in message:
            if isinstance(message['unit'], 'dict'):
                if('x' in message['unit'] and 'y' in message['unit']):
                    location = Coordinate(message['unit']['x'],
                                          message['unit', 'y'])
                    message['unit'] = self._uid_at(location)
                elif('id' in message['unit']):
                    message['unit'] = self._find_unit(message['unit']['id'])

    def flat(self):
        return {
            'board': self._get_board().as_hash(),
            'scenario': [self.scenario.as_hash()],
        }


class InvalidGameCreation(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)
