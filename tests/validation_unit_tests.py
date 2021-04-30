import unittest
from code_pipeline.validation import TestValidator
from code_pipeline.tests_generation import RoadTestFactory
import inspect

class ValidationTest(unittest.TestCase):

    def test_road_that_stars_outside_the_map(self):
        """
        creates a road that start from outside the map. By convention the map is defined as
        (0,0), (map_size, map_size)
        :return:
        """
        print("Running test", inspect.stack()[0][3])

        road_points = []
        road_points.append((-10, -10))
        road_points.append((50, 50))

        the_test = RoadTestFactory.create_road_test(road_points)

        validator = TestValidator(map_size=200)
        is_valid, validation_msg = validator.validate_test(the_test)

        self.assertFalse(is_valid)

    def test_road_that_ends_outside_the_map(self):
        """
        creates a road that start inside the map but ends outside it.
        :return:
        """
        print("Running test", inspect.stack()[0][3])

        road_points = []
        road_points.append((50, 50))
        road_points.append((-10, -10))

        the_test = RoadTestFactory.create_road_test(road_points)

        validator = TestValidator(map_size=200)
        is_valid, validation_msg = validator.validate_test(the_test)

        self.assertFalse(is_valid)

    def test_road_that_is_entirely_outside_the_map(self):
        """
        creates a road that stays entirely outside the map
        :return:
        """

        print("Running test", inspect.stack()[0][3])

        road_points = []
        road_points.append((-50, -50))
        road_points.append((-10, -10))

        the_test = RoadTestFactory.create_road_test(road_points)

        validator = TestValidator(map_size=200)
        is_valid, validation_msg = validator.validate_test(the_test)

        self.assertFalse(is_valid)

    def test_road_that_is_entirely_inside_the_map(self):
        """
        creates a road that stays entirely outside the map
        :return:
        """

        print("Running test", inspect.stack()[0][3])

        road_points = []
        road_points.append((50, 50))
        road_points.append((10, 10))

        the_test = RoadTestFactory.create_road_test(road_points)

        validator = TestValidator(map_size=200)
        is_valid, validation_msg = validator.validate_test(the_test)

        self.assertTrue(is_valid, validation_msg)

    def test_road_side_partially_outside(self):
        """
        creates a road that stays entirely outside the map
        :return:
        """

        print("Running test", inspect.stack()[0][3])

        road_points = []
        road_points.append((1, 10))
        road_points.append((1, 50))

        the_test = RoadTestFactory.create_road_test(road_points)

        validator = TestValidator(map_size=200)
        is_valid, validation_msg = validator.validate_test(the_test)

        self.assertFalse(is_valid)

    def test_road_self_intersect(self):
        """
        creates a road that stays entirely outside the map
        :return:
        """

        print("Running test", inspect.stack()[0][3])

        road_points = []
        road_points.append((10, 10))
        road_points.append((20, 20))
        road_points.append((10, 20))
        road_points.append((20, 10))

        the_test = RoadTestFactory.create_road_test(road_points)

        validator = TestValidator(map_size=200)

        is_valid, validation_msg = validator.validate_test(the_test)

        self.assertFalse(is_valid)

    def test_road_self_overlapping(self):
        """
        creates a road that stays entirely outside the map
        :return:
        """

        print("Running test", inspect.stack()[0][3])

        road_points = []
        road_points.append((10, 70))
        road_points.append((10, 80))
        road_points.append((15, 95))
        road_points.append((15, 80))
        road_points.append((15, 70))

        the_test = RoadTestFactory.create_road_test(road_points)

        validator = TestValidator(map_size=200)
        is_valid, validation_msg = validator.validate_test(the_test)

        self.assertFalse(is_valid)


if __name__ == '__main__':
    unittest.main()