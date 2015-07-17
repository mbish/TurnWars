from game.building import Building


class MockCoordinate:
    def flat(self):
        return "here"


def can_build_test():
    building = Building('house', 10, ['footman'], 'ignore')
    assert building.can_build('footman')
    assert not building.can_build('tank')
    assert building.get_revenue() == 10


def serializable_test():
    building = Building('house', 10, ['footman'], MockCoordinate())
    assert building.as_json() == (
        '{"coordinate": "here", '
        '"buildable_units": ["footman"], "name": "house"}')
