import unittest

from feature_extraction.road_geometry_calculator import RoadGeometryCalculator 

class RoadGeometryCalculatorAngleTest(unittest.TestCase):

    def setUp(self):
        self.__road_geometry_calculator = RoadGeometryCalculator()

    def test_positive_angle(self):
        v1 = (1,0)
        v2 = (0,1)

        angle = self.__road_geometry_calculator.get_angle(v1, v2)

        self.assertGreater(angle, 0, "Angle must be positive")

    def test_negative_angle(self):
        v1 = (0,1)
        v2 = (1,0)

        angle = self.__road_geometry_calculator.get_angle(v1, v2)

        self.assertLess(angle, 0, "Angle must be negative")

    def test_negative_angle_both_vectors_direct_down(self):
        v1 = (3,-1)
        v2 = (3,-2)

        angle = self.__road_geometry_calculator.get_angle(v1, v2)
        
        self.assertLess(angle, 0, "Angle must be negative")

    def test_positive_angle_both_vectors_direct_down(self):
        v1 = (3,-2)
        v2 = (3,-1)

        angle = self.__road_geometry_calculator.get_angle(v1, v2)
        
        self.assertGreater(angle, 0, "Angle must be positive")

    def test_negative_angle_both_vectors_direct_down_with_negative_Xs(self):
        v1 = (-3,-2)
        v2 = (-3,-1)

        angle = self.__road_geometry_calculator.get_angle(v1, v2)

        self.assertLess(angle, 0, "Angle must be negative")

    def test_positive_angle_both_vectors_direct_down_with_negative_Xs(self):
        v1 = (-3,-1)
        v2 = (-3,-2)

        angle = self.__road_geometry_calculator.get_angle(v1, v2)

        self.assertGreater(angle, 0, "Angle must be positive")

    def test_negative_angle_both_vectors_direct_up_with_negative_Xs(self):
        v1 = (-3,1)
        v2 = (-3,2)

        angle = self.__road_geometry_calculator.get_angle(v1, v2)

        self.assertLess(angle, 0, "Angle must be negative")

    def test_positive_angle_both_vectors_direct_up_with_negative_Xs(self):
        v1 = (-3,2)
        v2 = (-3,1)

        angle = self.__road_geometry_calculator.get_angle(v1, v2)

        self.assertGreater(angle, 0, "Angle must be positive")


class RoadGeometryCalculatorRoadLengthTest(unittest.TestCase):
    def setUp(self):
        self.__road_geometry_calculator = RoadGeometryCalculator()

    def test_straint_horizontal_road(self):
        road_points = [(1,1),(2,1),(3,1),(4,1)]

        length = self.__road_geometry_calculator.get_road_length(road_points)
        expected_length = 3

        self.assertEqual(length, expected_length, "The length is not correct.")


if __name__ == "__main__":
    unittest.main()

