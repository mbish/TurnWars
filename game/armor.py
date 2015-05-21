from game.serializable import Serializable


class Armor(Serializable):

    def __init__(self, name, starting_health):
        if(starting_health <= 0):
            raise BadArmorCreation("Cannot construct armor with health <= 0")
        self.health = starting_health
        self.starting_health = starting_health
        self.name = name
        self.taken_this_turn = 0

    def do_damage(self, damage):
        self.health -= damage
        self.taken_this_turn += damage
        if(self.health < 0):
            self.health = 0

    def get_health(self):
        return self.health

    def reset(self):
        self.taken_this_turn = 0
        return

    def flat(self):
        return {
            'name': self.name,
            'health': self.health,
        }


class BadArmorCreation(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
