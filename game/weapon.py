from game.serializable import Serializable
from game.exceptions import BadWeaponCreation, BadWeaponRequest


class Weapon(Serializable):

    # eventually reach will take a "pattern" object
    # which will designate a specific pattern of tiles in
    # via an arbitrarily sized 2-dimensional matrix centered
    # at the unit for now just a linear range
    def __init__(self, name, uses, attack_strength, reach=1,
                 uses_per_turn=1, non_targetables=''):
        Serializable.__init__(self)
        if(attack_strength < 0 or uses < 0 or reach < 0):
            raise BadWeaponCreation("Cannot create weapon with \
                uses {0} and attack_strength {1}".format(
                uses, attack_strength))
        self.name = name
        self.uses = uses
        self.attack_strength = attack_strength
        self.non_targetables = non_targetables
        self.reach = reach
        self.uses_per_turn = uses_per_turn
        self.used_this_turn = 0
        self.uses_left = uses_per_turn

    def use(self, times=1):
        if(self.uses - times < 0 or self.uses_left - times < 0):
            raise BadWeaponRequest("Cannot use weapon again")
        self.uses_left -= times
        self.uses -= times
        return True

    def can_use(self, distance):
        return (self.uses > 0 and
                distance <= self.attack_range() and
                self.uses_left > 0)

    def reset(self):
        self.uses_left = self.uses_per_turn

    def attack_range(self):
        return self.reach

    def get_strength(self):
        return self.attack_strength

    def flat(self):
        return {
            'name': self.name,
            'attack_strength': self.attack_strength,
            'non_targetables': self.non_targetables,
            'range': self.reach,
            'uses_left': self.uses_left,
        }

    def can_target(self, unit_type):
        return not (unit_type in self.non_targetables)
