from unit import Unit
import math
from coordinate import Coordinate
from serializable import Serializable
from path_finder import NoPathFound, PathFinder


class Game(Serializable):

    def __init__(self, board, armies, path_finder):
        if(len(armies) == 0):
            raise InvalidGameCreation("Cannot create a game with no armies")
        self.armies = armies
        self.board = board
        self.path_finder = path_finder

    def _find_army(self, army_name):
        return next(army for army in self.armies if army.name == army_name)

    def _find_unit(self, army_name, unit_id):
        return self._find_army(army_name).find_unit(unit_id)

    def move(self, unit, coordinate):
        if(self.space_occupied(coordinate)):
            return
        army = self._find_army(unit.army)
        transport = army.equipment_info(unit.name, 'transport')
        movement_cost = transport['movement_cost']
        try:
            path = self.path_finder.get_path(unit.get_coordinate(),
                                             movement_cost, coordinate)
            if(self.path_finder.path_cost(self.board, path, movement_cost) <=
               unit.movement_range()):
                unit.move(coordinate, len(path))
        except NoPathFound:
            return

    def attack(self, attacker, defender):
        if(attacker.army != defender.army):
            attacker.attack(defender)

    def build(self, army, unit_name, location):
        if(not self.space_occupied(location)):
            army.buy_unit(unit_name, location)

    def space_occupied(self, coordinate):
        for army in self.armies:
            if(army.has_unit_at(coordinate)):
                return True

    def do(self, message):
        try:
            if(message.name == 'move'):
                unit = self._find_unit(message.army_name, message.unit_id)
                to = Coordinate(message.to.x, message.to.y)
                self.move(unit, to)
            elif(message.name == 'attack'):
                attacker = self._find_unit(message.attacking_army,
                                           message.attacker_id)
                defender = self._find_unit(message.defending_army,
                                           message.defender_id)
                self.attack(attacker, defender)
            elif(message.name == 'build'):
                army = self._find_army(message.army_name)
                location = Coordinate(message.at.x, message.at.y)
                self.build(army, message.unit_name, location)
            elif(message.name == 'end_turn'):
                army = self._find_army(message.army_name)
                if(army.is_turn()):
                    army.end_turn()

        except Exception:
            return self.flat()

        return self.flat()

    # This is really a utility function and may get split out from the
    # truely model-modifying functions above
    def tiles_in_range(self, unit):
        army = self._find_army(unit.army)
        transport = army.equipment_info(unit.name, 'transport')
        movement_cost = transport['movement_cost']
        spaces_left = unit.get_spaces_left()
        return self.path_finder.tiles_in_range(self.board, movement_cost,
                                               unit.get_coordinate(),
                                               spaces_left)

    def flat(self):
        return {
            'armies': [army.as_hash() for army in self.armies],
            'board': self.board.as_hash()
        }


class InvalidGameCreation(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)
