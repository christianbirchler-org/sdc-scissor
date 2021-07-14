import math

# TODO: provide a factory that implements the singleton pattern or use the
#       interfaces in a static fashion. I still have to decide this.
class RoadGeometryCalculator:
    def extract_turn_angles(self, road_points):
        """
        Extract angles of raod points and ad them to the instance variable
        """
        angles = []
        # iterate over "all" road points
        for i in range(2, len(road_points)):
            # calculate angle between previous direction and vector from
            # previous point to the current one
            
            point_before = road_points[i-2]
            mid_point = road_points[i-1]
            point_after = road_points[i]

            prev_direction = self.get_direction(point_before, mid_point)
            current_direction = self.get_direction(mid_point, point_after)

            turn_angle = self.get_angle(prev_direction, current_direction)
            angles.append(turn_angle)

        return angles

    # TODO
    def is_right_turn(self, prev_angle, current_angle):
        pass

    def get_angle(self, first_vec, second_vec):
        """
        Returns the angle in degrees between the first and second vector.
        A left turn as positive angles whereas right turns have negatives.
        """
        a1, a2 = first_vec[0], first_vec[1]
        b1, b2 = second_vec[0], second_vec[1]

        angle_in_radians = math.atan2(b2,b1) - math.atan2(a2,a1)
        angle_in_degrees = math.degrees(angle_in_radians)

        return angle_in_degrees

    def get_distance_between(self, first_point: tuple, second_point: tuple) -> float:
        a1, a2 = first_point
        b1, b2 = second_point
        c1, c2 = (b1-a1, b2-a2)
        distance = math.sqrt(c1**2 + c2**2)
        return distance
        
    def get_direction(self, first_point, second_point):
        """
        Return the difference vector (second_point-first_point)
        """
        return (second_point[0]-first_point[0], second_point[1]-first_point[1])

    def get_road_length(self, road_points):
        nr_of_road_points = len(road_points)

        road_length = 0
        for i in range(1, nr_of_road_points):
            a1, a2 = road_points[i-1]
            b1, b2 = road_points[i]

            c1, c2 = (b1-a1, b2-a2)

            road_length += math.sqrt(c1**2+c2**2)
        
        return road_length


if __name__ == "__main__":
    import unittest

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


    unittest.main()