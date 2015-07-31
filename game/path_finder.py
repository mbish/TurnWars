import types
from game.coordinate import Coordinate, BadCoordinateCreation


class PathFinder:

    def __init__(self, board):
        self.board = board

    def get_path(self, cost_table, from_position, to_position):
        evaluated = []
        queue = [from_position]
        path = {}
        score = {}
        score[from_position] = 0
        estimated_score = {}
        estimated_score[from_position] = (score[from_position] +
                                          self._path_length(from_position,
                                                            to_position))

        while queue:
            current_index = queue.index(min(
                [x for x in estimated_score if x in queue],
                key=estimated_score.get))
            current = queue[current_index]
            if(current == to_position):
                result = self._traceback(path, to_position)
                result.remove(from_position)
                return result

            del queue[current_index]
            evaluated.append(current)

            for neighbor in self.board.get_neighbors(current):
                if(neighbor in evaluated):
                    continue

                cost = 0

                tile = self.board.get_tile_at_coordinate(neighbor)
                if tile.tile_type in cost_table:
                    cost = cost_table[tile.tile_type]
                else:
                    continue

                temp_score = score[current] + cost

                if (neighbor not in queue or
                        (neighbor in score and
                         temp_score < score[neighbor])):
                    path[neighbor] = current
                    score[neighbor] = temp_score
                    estimated_score[neighbor] = (score[neighbor] +
                                                 self._path_length(
                                                     neighbor,
                                                     to_position))
                    if neighbor not in queue:
                        queue.append(neighbor)

        raise NoPathFound("Cannot find path between {0} and {1}".format(
            from_position, to_position))

    def _is_path(self, cost_table, from_position, to_position):
        is_path = True
        try:
            self.get_path(cost_table, from_position, to_position)
        except NoPathFound:
            is_path = False

        return is_path

    def path_cost(self, path, cost_table):
        cost = 0
        for coordinate in path:
            tile = self.board.get_tile_at_coordinate(coordinate)
            cost += cost_table[tile.tile_type]

        return cost

    # consider adding "region to consider" for special movement
    def tiles_in_range(self, cost_table, from_position, max_cost):
        can_move_to = []

        # add 1 to max cost so we're working on a closed interval
        for x in range(-max_cost, max_cost + 1):
            for y in range(-max_cost, max_cost + 1):
                if y == 0 and x == 0 or abs(y) + abs(x) > max_cost:
                    continue
                try:
                    to_position = Coordinate(from_position.x + x,
                                             from_position.y + y)
                except BadCoordinateCreation:
                    continue

                if self.board.is_on_board(to_position):
                    try:
                        path = self. get_path(cost_table, from_position,
                                              to_position)

                        if from_position in path:
                            path.remove(from_position)
                        if self.path_cost(path, cost_table) <= max_cost:
                            can_move_to.append(to_position)
                    except NoPathFound:
                        continue

        return can_move_to

    def _traceback(self, path, coordinate):
        if coordinate in path:
            traceback = self._traceback(path, path[coordinate])
            traceback.append(coordinate)
            return traceback
        else:
            return [coordinate]

    def _path_length(self, start, goal):
        horizontal_distance = abs(start.x - goal.x)
        virtical_distance = abs(start.y - goal.y)
        return horizontal_distance + virtical_distance


class NoPathFound(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)
