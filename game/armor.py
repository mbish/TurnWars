from serializable import Serializable


class Armor(Serializable):

    def __init__(self, name, starting_health):
        if(starting_health <= 0):
            raise BadArmorCreation("Cannot construct armor with health <= 0")
        self.health = starting_health
        self.starting_health = starting_health
        self.name = name

    def do_damage(self, damage):
        self.health -= damage
        if(self.health < 0):
            self.health = 0

    def get_health(self):
        return self.health

    def flat(self):
        return {
            'name': self.name,
            'health': self.health,
        }


class BadArmorCreation(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
