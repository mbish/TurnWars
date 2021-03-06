from game.serializable import Serializable
from game.exceptions import BadTransportCreation, BadTransportRequest


class Transport(Serializable):

    def __init__(self, name, spaces_per_turn, cost_table, starting_fuel=-1):
        if(spaces_per_turn < 0):
            raise BadTransportCreation("Cannot create transport with movement \
                    less than 0")
        self.spaces_left = spaces_per_turn
        self.spaces_per_turn = spaces_per_turn
        self.fuel = starting_fuel
        self.starting_fuel = starting_fuel
        self.name = name
        self.cost_table = cost_table
        self.moved_this_turn = False

    def uses_fuel(self):
        return self.fuel != -1

    def move(self, distance):
        if(distance > self.spaces_left):
            raise BadTransportRequest(
                "Cant move {0} with spaces {1} left".format(distance,
                                                            self.spaces_left))
        if(self.uses_fuel()):
            if(self.fuel < distance):
                raise BadTransportRequest(
                    "Cannot move {0} with fuel {1} left".format(distance,
                                                                self.fuel))
            self.use_fuel(distance)

        self.spaces_left -= distance
        self.moved_this_turn = True

    def get_name(self):
        return self.name

    def refuel(self):
        if(self.uses_fuel()):
            self.fuel = self.starting_fuel

    def reset(self):
        self.spaces_left = self.spaces_per_turn
        self.moved_this_turn = False

    def flat(self):
        return {
            'name': self.name,
            'spaces_left': self.spaces_left,
            'fuel': self.fuel,
            'hasMoved': self.moved_this_turn
        }

    def has_moved(self):
        return self.moved_this_turn

    def get_spaces_left(self):
        if(self.uses_fuel()):
            return min(self.spaces_left, self.fuel)
        else:
            return self.spaces_left

    def use_fuel(self, amount):
        if(not self.uses_fuel()):
            return
        if(amount > self.fuel):
            raise BadTransportRequest(
                "Cannot use {1} fuel only have {0}".format(amount, self.fuel))
        self.fuel -= amount

