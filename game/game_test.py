from game import Game, InvalidGameCreation
from path_finder import NoPathFound
from nose.tools import assert_raises


class MockArmy:
    def __init__(self, name):
        self.name = name
        self.units = []

    def find_unit(self, uid):
        return "a {} {} unit".format(self.name, uid)

    def equipment_info(self, name, _type):
        return {
            'movement_cost': 0
        }

    def buy_unit(self, unit, location):
        self.units.append("{} {}".format(unit, location))

    def has_unit_at(self, location):
        return location == "not here"


class MockUnit:
    def __init__(self, _range, army):
        self.pos = 0
        self._range = _range
        self.army = army
        self.name = "none"
        self.health = 100

    def get_coordinate(self):
        return

    def movement_range(self):
        return self._range

    def move(self, to, dist):
        self.pos = to

    def attack(self, target):
        target.health -= 10


class MockPathFinder:

    def __init__(self, path, cost, throw_exception=False):
        self.path = path
        self.cost = cost
        self.throw_exception = throw_exception

    def path_cost(self, board, path, costs):
        return self.cost

    def get_path(self, coordinate, costs, coordinate2):
        if(self.throw_exception):
            raise NoPathFound("Mock path finder just cannot right now")
        return self.path


def bad_constructor_test():
    assert_raises(InvalidGameCreation, Game, [], [], [])


def find_army_test():
    army1 = MockArmy('dragon')
    army2 = MockArmy('salamander')
    army3 = MockArmy('rat')
    army4 = MockArmy('phoenix')
    game = Game([], [army1, army2, army3, army4], [])
    found_army = game._find_army('dragon')
    assert found_army.name == 'dragon'
    found_army = game._find_army('rat')
    assert found_army.name == 'rat'


def find_unit_test():
    army1 = MockArmy('dragon')
    army2 = MockArmy('salamander')
    army3 = MockArmy('rat')
    army4 = MockArmy('phoenix')
    game = Game([], [army1, army2, army3, army4], [])
    unit = game._find_unit('rat', 'test')
    assert unit == "a rat test unit"
    unit = game._find_unit('dragon', 'best')
    assert unit == "a dragon best unit"
    unit = game._find_unit('phoenix', 'stressed')
    assert unit == "a phoenix stressed unit"


def move_test():
    army1 = MockArmy('dragon')
    army2 = MockArmy('salamander')
    army3 = MockArmy('rat')
    army4 = MockArmy('phoenix')
    path_finder = MockPathFinder([1, 2, 3], 10)
    game = Game([], [army1, army3], path_finder)
    unit = MockUnit(5, 'dragon')
    game.move(unit, "A new place")
    assert unit.pos != "A new place"
    unit = MockUnit(10, 'rat')
    game.move(unit, "A new place")
    assert unit.pos == "A new place"


def move2_test():
    army1 = MockArmy('dragon')
    army2 = MockArmy('salamander')
    path_finder = MockPathFinder([1, 2, 3], 10, True)
    game = Game([], [army1, army2], path_finder)
    unit = MockUnit(100, 'dragon')
    game.move(unit, "There")
    assert unit.pos != "There"


def attack_test():
    army1 = MockArmy('dragon')
    army2 = MockArmy('salamander')
    game = Game([], [army1, army2], [])
    unit1 = MockUnit(100, 'dragon')
    unit2 = MockUnit(10, 'salamander')
    unit3 = MockUnit(100, 'dragon')
    game.attack(unit1, unit2)
    assert unit2.health == 90
    game.attack(unit1, unit3)
    assert unit3.health == 100


def build_test():
    army1 = MockArmy('dragon')
    army2 = MockArmy('salamander')
    game = Game([], [army1, army2], [])
    game.build(army1, 'footman', 'here')
    assert army1.units == ['footman here']
    game.build(army1, 'footman', 'again')
    assert army1.units == ['footman here', 'footman again']
    game.build(army1, 'footman', 'not here')
    assert army1.units == ['footman here', 'footman again']
