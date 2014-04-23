from unit import Unit
import math
from coordinate import Coordinate
from serializable import Serializable
import path_finder


class Game(Serializable):

    def __init__(self, board, armies):
        if(len(armies) == 0):
            raise InvalidGameCreation("Cannot create a game with no armies")
        self.armies = armies
        self.board = board

    def _find_army(self, army_name):
        return next(army for army in self.armies if army.name == army_name)

    def _find_unit(self, army_name, unit_id):
        return self._find_army(army_name).find_unit(unit_id)

    def move(self, unit, coordinate):
        army = self._find_army(unit.army)
        transport = army.equipment_info(unit.name, 'transport')
        movement_cost = transport['movement_cost']
        path = path_finder.get_path(self.board, unit.get_coordinate(),
                                    movement_cost, coordinate)
        if(len(path) <= unit.movement_range):
            unit.move(coordinate, len(path))

    def do(self, message):
        if(message.name == 'move'):
            unit = self._find_unit(message.army_name, message.unit_id)
            to = Coordinate(message.to.x, message.to.y)
            self.move(unit, to)

        return self.flat()

    def flat(self):
        return {
            'armies': [army.as_hash() for army in self.armies],
            'board': self.board.as_hash()
        }


class InvalidGameCreation(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)
