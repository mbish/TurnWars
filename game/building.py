from serializable import Serializable


class Building(Serializable):

    def __init__(self, name, buildable_units, coordinate):
        Serializable.__init__(self)
        self.name = name
        self.coordinate = coordinate
        self.buildable_units = buildable_units

    def can_build(self, unit_name):
        return unit_name in self.buildable_units

    def flat(self):
        return {
            'name': self.name,
            'coordinate': self.coordinate.flat(),
            'buildable_units': self.buildable_units
        }
