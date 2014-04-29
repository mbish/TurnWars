from game.serializable import Serializable


class Building(Serializable):

    def __init__(self, name, revenue, buildable_units, coordinate):
        Serializable.__init__(self)
        self.name = name
        self.coordinate = coordinate
        self.buildable_units = buildable_units
        self.revenue = revenue

    def can_build(self, unit_name):
        return unit_name in self.buildable_units

    def get_revenue(self):
        return self.revenue

    def flat(self):
        return {
            'name': self.name,
            'coordinate': self.coordinate.flat(),
            'buildable_units': self.buildable_units
        }
