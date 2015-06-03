from game.game_engine import Game
from game.path_finder import NoPathFound


class MockBoard:
    def as_hash(self):
        return ""


class MockScenario:
    def __init__(self, armies):
        self.armies = armies

    def _find_army(self, army_name):
        return next(army for army in self.armies if army.name == army_name)

    def space_occupied(self, coordinate):
        for army in self.armies:
            if(army.has_unit_at(coordinate)):
                return True

        return False

    def as_hash(self):
        return "a serialized scenario"


class MockArmy:
    def __init__(self, name):
        self.name = name
        self.units = []

    def find_unit(self, uid):
        return "a {0} {1} unit".format(self.name, uid)

    def equipment_info(self, name, _type):
        return {
            'movement_cost': 0
        }

    def buy_unit(self, unit, location):
        self.units.append("{0} {1}".format(unit, location))

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


def find_unit_test():
    army1 = MockArmy('dragon')
    army2 = MockArmy('salamander')
    army3 = MockArmy('rat')
    army4 = MockArmy('phoenix')
    game = Game([], MockScenario([army1, army2, army3, army4]), [])
    unit = game._find_unit('rat', 'test')
    assert unit == "a rat test unit"
    unit = game._find_unit('dragon', 'best')
    assert unit == "a dragon best unit"
    unit = game._find_unit('phoenix', 'stressed')
    assert unit == "a phoenix stressed unit"


def move_test():
    army1 = MockArmy('dragon')
    army3 = MockArmy('rat')
    path_finder = MockPathFinder([1, 2, 3], 10)
    game = Game([], MockScenario([army1, army3]), path_finder)
    unit = MockUnit(5, 'dragon')
    game.move(unit, "A new place")
    assert unit.pos != "A new place"
    unit = MockUnit(10, 'rat')
    game.move(unit, "A new place")
    assert unit.pos == "A new place"
    game.move(unit, "not here")
    assert unit.pos == "A new place"


def move2_test():
    army1 = MockArmy('dragon')
    army2 = MockArmy('salamander')
    path_finder = MockPathFinder([1, 2, 3], 10, True)
    game = Game([], MockScenario([army1, army2]), path_finder)
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
    game = Game([], MockScenario([army1, army2]), [])
    game.build(army1, 'footman', 'here')
    assert army1.units == ['footman here']
    game.build(army1, 'footman', 'again')
    assert army1.units == ['footman here', 'footman again']
    game.build(army1, 'footman', 'not here')
    assert army1.units == ['footman here', 'footman again']


# tests that the message handling code never chokes on bad input
def messages_test():
    army1 = MockArmy('dragon')
    army2 = MockArmy('salamander')
    game = Game(MockBoard(), MockScenario([army1, army2]), [])
    flat = game.do({
        'name': 'build',
        'army_name': 'dragon',
        'unit_name': 'footman',
        'at': {
            'x': [],
            'y': 'not a number'
        }
    })
    assert flat == {'board': '', 'scenario': ['a serialized scenario']}
    flat = game.do({
        'name': 'nonsense',
        'at': {
            'x': -1,
            'y': 0
        }
    })
    assert flat == {'board': '', 'scenario': ['a serialized scenario']}
    flat = game.do({
        'name': 'move',
    })
    assert flat == {'board': '', 'scenario': ['a serialized scenario']}
    flat = game.do({
        'name': 'end_turn',
    })
    assert flat == {'board': '', 'scenario': ['a serialized scenario']}
    flat = game.do({
        'name': 'attack',
    })
    assert flat == {'board': '', 'scenario': ['a serialized scenario']}
    game.build(army1, 'footman', 'here')
    flat = game.do({
        'name': 'move',
        'army_name': 'dragon',
        'unit_id': 'footman',
        'to': {
            'x': 0,
            'y': 0
        }
    })
    flat = game.do({
        'name': 'attack',
        'attacking_army': 'dragon',
        'attacker_id': 'footman',
        'defending_army': 'salamander',
        'defender_id': 'footman'
    })
    assert flat == {'board': '', 'scenario': ['a serialized scenario']}
