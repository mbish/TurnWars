from game.weapon import Weapon
from game.exceptions import BadWeaponRequest, BadWeaponCreation
from nose.tools import assert_raises


def bad_constructor_test():
    assert_raises(BadWeaponCreation, Weapon, 'sword', -1, 4, 3)
    assert_raises(BadWeaponCreation, Weapon, 'sword', 10, -4, 3)
    assert_raises(BadWeaponCreation, Weapon, 'sword', 10, -4, -2)


def use_test():
    weapon = Weapon('sword', 5, 4, 3, 5)
    assert weapon.uses == 5
    weapon.use(5)
    assert weapon.uses == 0
    assert_raises(BadWeaponRequest, weapon.use)
    assert not weapon.can_use(0)


def reset_test():
    weapon = Weapon('sword', 5, 4, 3, 1)
    assert_raises(BadWeaponRequest, weapon.use, 5)
    assert weapon.use(1)
    assert weapon.uses_left == 0
    weapon.reset()
    assert weapon.use(1)


def targeting_test():
    weapon = Weapon('sword', 5, 4, 3, 1, {'plane': 0})
    assert not weapon.can_target('plane')


def serializable_test():
    weapon = Weapon('sword', 5, 4, 3, {'plane': 0})
    json_string = ('{"attack_strength": 4, "name": "sword",'
            ' "non_targetables": "", "range": 3, "uses_left": {"plane": 0}}')

    print(weapon.as_json())
    assert weapon.as_json() == json_string


def attack_range_test():
    weapon = Weapon('sword', 5, 4, 3, {'plane': 0})
    assert weapon.attack_range() == 3
