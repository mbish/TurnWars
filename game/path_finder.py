import types


def get_path(board, cost_table, from_position, to_position):
    evaluated = []
    queue = [from_position]
    path = {}
    score = {}
    score[from_position] = 0
    estimated_score = {}
    estimated_score[from_position] = score[from_position] + _path_length(
        from_position, to_position)

    while queue:
        current_index = queue.index(min(
            [x for x in estimated_score if x in queue],
            key=estimated_score.get))
        current = queue[current_index]
        if(current == to_position):
            return _traceback(path, to_position)

        del queue[current_index]
        evaluated.append(current)

        for neighbor in board.get_neighbors(current):
            if(neighbor in evaluated):
                continue

            cost = 0

            tile = board.get_tile_at_coordinate(
                neighbor.x, neighbor.y)
            if tile.tile_type in cost_table:
                cost = cost_table[tile.tile_type]

            temp_score = score[current] + cost

            if (neighbor not in queue or
                    neighbor in score and
                    temp_score < score[neighbor]):
                path[neighbor] = current
                score[neighbor] = temp_score
                estimated_score[neighbor] = (score[neighbor] +
                                             _path_length(neighbor,
                                                          to_position))
                if neighbor not in queue:
                    queue.append(neighbor)

    raise NoPathFound("Cannot find path between {} and {}".format(
        from_position, to_position))


def _traceback(path, coordinate):
    if coordinate in path:
        traceback = _traceback(path, path[coordinate])
        traceback.append(coordinate)
        return traceback
    else:
        return [coordinate]


def _path_length(start, goal):
    horizontal_distance = abs(start.x - goal.x)
    virtical_distance = abs(start.y - goal.y)
    return horizontal_distance + virtical_distance


class NoPathFound(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)
