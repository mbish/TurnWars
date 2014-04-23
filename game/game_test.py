from game import Game, InvalidGameCreation
from nose.tools import assert_raises


class MockArmy:
    def __init__(self, name):
        self.name = name

    def find_unit(self, uid):
        return "a {} {} unit".format(self.name, uid)


def bad_constructor_test():
    assert_raises(InvalidGameCreation, Game, [], [])


def find_army_test():
    army1 = MockArmy('dragon')
    army2 = MockArmy('salamander')
    army3 = MockArmy('rat')
    army4 = MockArmy('phoenix')
    game = Game([], [army1, army2, army3, army4])
    found_army = game._find_army('dragon')
    assert found_army.name == 'dragon'
    found_army = game._find_army('rat')
    assert found_army.name == 'rat'


def find_unit_test():
    army1 = MockArmy('dragon')
    army2 = MockArmy('salamander')
    army3 = MockArmy('rat')
    army4 = MockArmy('phoenix')
    game = Game([], [army1, army2, army3, army4])
    unit = game._find_unit('rat', 'test')
    assert unit == "a rat test unit"
    unit = game._find_unit('dragon', 'best')
    assert unit == "a dragon best unit"
    unit = game._find_unit('phoenix', 'stressed')
    assert unit == "a phoenix stressed unit"
