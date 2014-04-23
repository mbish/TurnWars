from unit import Unit
import math
from coordinate import Coordinate
from serializable import Serializable


class Game(Serializable):
    
    def __init__(self, board, armies):
        if(len(armies) == 0):
            raise InvalidGameCreation("Cannot create a game with no armies")
        self.armies = armies
        self.board = board

    def _find_army(self, army_name):
        return next(army for army in self.armies if army.name == army_name)

    # not convinced this is the best place for this yet
    # also what about occupied tiles?
    def _get_path(self, unit_position, cost_table, coordinate):
        evaluated = []
        queue = []
        path = {}
        score = {}
        score[unit_position] = 0
        estimated_score = []
        estimated_score = score[unit_position] + self._path_length(
                unit_position, coordinate)

        while queue:
            current_index = queue.index(min(estimated_score))
            if(queue[current_index] == coordinate):
                return self._traceback(path, coordinate)

            current = queue.remove(current_index)
            evaluated.append(current)

            for neighbor in self.board.get_neighbors(current):
                if(neighbor in evaluated):
                    continue

                cost = 0

                tile = self.board.get_tile_at_coordinate(
                    neighbor.x, neighbor.y)
                if tile.tile_type in cost_table:
                    cost = cost_table[tile.tile_type]

                temp_score = score[current] + cost
                
                if neighbor not in queue or temp_score < score[neighbor]:
                    path[neighbor] = current
                    score[neighbor] = temp_score
                    estimated_score[neighbor] = (score[neighbor] + 
                        self._path_length(neighbor, coordinate))
                    if neighbor not in queue:
                        queue.append(neighbor)

        raise NoPathFound("Cannot find path between {} and {}".format(
            unit_position.as_json(), coordinate.as_json()))

    def _traceback(self, path, coordinate):
        if coordinate in path:
            traceback = self._traceback(path, path[coordinate])
            return traceback.append(coordinate)
        else:
            return coordinate

    def _path_length(self, start, goal):
        horizontal_distance = abs(start.x - goal.x)
        virtical_distance = abs(start.y - goal.y)
        return horizontal_distance + virtical_distance
        

    def _find_unit(self, army_name, unit_id):
        return self._find_army(army_name).find_unit(unit_id)

    def move(self, unit, coordinate):
        path = self._get_path(unit.get_coordinate(),
                              unit.get_transport_type(), coordinate)
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

class NoPathFound(Exception):
    
    def __init__(self, message):
        Exception.__init__(self, message)
