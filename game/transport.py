from serializable import Serializable
class Transport(Serializable):
    name = ''
    spaces_left = 0
    spaces_per_turn = 0
    fuel = -1
    starting_fuel = -1

    def __init__(self, name, spaces_per_turn, starting_fuel=-1):
        if(spaces_per_turn < 0):
            raise BadTransportCreation("Cannot create transport with movement \
                    less than 0")
        self.spaces_left = spaces_per_turn
        self.spaces_per_turn = spaces_per_turn
        self.fuel = starting_fuel
        self.starting_fuel = starting_fuel
        self.name = name

    def uses_fuel(self):
        return self.fuel != -1

    def move(self, distance):
        if(distance > self.spaces_left):
            raise BadTransportRequest("Cant move {} with spaces {} left".format(
                                          distance, self.spaces_left))
        if(self.uses_fuel()):
            if(self.fuel < distance):
                raise BadTransportRequest(
                        "Cannot move {} with fuel {} left".format(distance,
                                                                  self.fuel))
            self.use_fuel(distance)

        self.spaces_left -= distance

    def refuel(self):
        if(self.uses_fuel()):
            self.fuel = self.starting_fuel

    def reset(self):
        self.spaces_left = self.spaces_per_turn

    def flat(self):
        return {
            'name': self.name,
            'spaces_left': self.spaces_left,
            'fuel': self.fuel,
        }

    def get_spaces_left(self):
        if(self.uses_fuel()):
            return min(self.spaces_left, self.fuel)
        else:
            return self.spaces_left

    def use_fuel(self, amount):
        if(not self.uses_fuel()):
            return
        if(amount > self.fuel):
            raise BadTransportRequest("Cannot use {} fuel only have {}".format(
                                        amount, self.fuel))
        self.fuel -= amount


class BadTransportRequest(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class BadTransportCreation(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
