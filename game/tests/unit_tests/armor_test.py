from game.armor import Armor
from game.exceptions import BadArmorCreation
from nose.tools import assert_raises


def damage_test():
    armor = Armor('shirt', 5)
    assert armor.get_health() == 5
    armor.do_damage(5)
    assert armor.get_health() == 0
    armor.do_damage(5)
    assert armor.get_health() == 0
    assert armor.taken_this_turn == 10
    armor.reset()
    assert armor.taken_this_turn == 0


def serializable_test():
    armor = Armor('shirt', 5)
    assert armor.as_json() == '{"health": 5, "name": "shirt"}'


def bad_creation_test():
    assert_raises(BadArmorCreation, Armor, 'shirt', -1)
