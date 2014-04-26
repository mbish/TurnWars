from serializable import Serializable


class Unit(Serializable):

    def __init__(self, name, transport, weapon, armor, coordinate, army):
        self.name = name
        self.transport = transport
        self.weapon = weapon
        self.armor = armor
        self.coordinate = coordinate
        self.army = army
        self.uid = id(self)
        if(self.get_health() <= 0):
            self.dead = True
        else:
            self.dead = False

    def reset(self):
        self.transport.reset()
        self.weapon.reset()
        self.armor.reset()

    def get_coordinate(self):
        return self.coordinate

    def set_coordinate(self, coordinate):
        self.coordinate = coordinate

    def move(self, coordinate, distance):
        self.transport.move(distance)
        return self.set_coordinate(coordinate)

    def do_damage(self, damage):
        self.armor.do_damage(damage)
        if(self.get_health() <= 0):
            self.dead = True

    def is_dead(self):
        return self.dead

    def get_health(self):
        return self.armor.get_health()

    def movement_range(self):
        return self.transport.get_spaces_left()

    def attack_range(self):
        return self.attack_range()

    def get_transport_type(self):
        return self.transport.get_name()

    def can_move(self, distance):
        return self.movement_range() >= distance

    def get_attack_strength(self):
        return self.weapon.get_attack_strength()

    # consider moving distance check into game object
    # for move elaberate attack patterns
    def attack(self, target):
        distance = self.coordinate.get_distance(target.coordinate)
        if(self.weapon.can_use(distance)):
            damage = self.weapon.get_strength()
            target.do_damage(damage)
            self.weapon.use()

    def flat(self):
        return {
            'name': self.name,
            'transport': self.transport.flat(),
            'weapon': self.weapon.flat(),
            'armor': self.armor.flat(),
            'coordinate': self.coordinate.flat(),
            'army': self.army,
            'id': self.uid
        }
