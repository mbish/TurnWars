import unittest
from game.building import Building


class MockCoordinate:
    def flat(self):
        return "here"


class BuildingTests(unittest.TestCase):
    def test_can_build(self):
        building = Building('house', 10, ['footman'], 'ignore')
        self.assertTrue(building.can_build('footman'))
        self.assertTrue(not building.can_build('tank'))
        self.assertTrue(building.get_revenue() == 10)


    def test_serializable(self):
        building = Building('house', 10, ['footman'], MockCoordinate())
        assert building.as_json() == ('{"buildable_units": ["footman"], '
                                      '"coordinate": "here", "name": "house"}')


if __name__ == '__main__':
    unittest.main()
