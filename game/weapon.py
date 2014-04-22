from serializable import Serializable


class Weapon(Serializable):

    def __init__(self, name, uses, attack_strength, non_targetables=''):
        Serializable.__init__(self)
        if(attack_strength < 0 or uses < 0):
            raise BadWeaponCreation("Cannot create weapon with \
                uses {} and attack_strength {}".format(
                uses, attack_strength))
        self.name = name
        self.uses = uses
        self.attack_strength = attack_strength
        self.non_targetables = non_targetables

    def use(self, times=1):
        if(not self.can_use()):
            raise BadWeaponRequest("Cannot use weapon again")
        self.uses -= times

    def can_use(self):
        return self.uses > 0

    def flat(self):
        return {
            'name': self.name,
            'attack_strength': self.attack_strength,
            'non_tragetables': self.non_targetables
        }

    def can_target(self, unit_type):
        return not (unit_type in self.non_targetables)


class BadWeaponRequest(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)


class BadWeaponCreation(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)
