import unittest

from feature_extraction import RoadGeometryCalculator 

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




if __name__ == "__main__":
    unittest.main()

