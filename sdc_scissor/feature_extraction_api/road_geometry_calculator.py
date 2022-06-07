import logging
import math


class RoadGeometryCalculator:
    def extract_turn_angles(self, road_points):
        """
        Extract angles of raod points and ad them to the instance variable.

        :param road_points: Points that define the road in the test scenario.
        :return: Angles in degrees of road's turns defined by the road points.
        """
        angles = []
        # iterate over "all" road points
        for i in range(2, len(road_points)):
            # calculate angle between previous direction and vector from
            # previous point to the current one

            point_before = road_points[i - 2]
            mid_point = road_points[i - 1]
            point_after = road_points[i]

            prev_direction = self.get_direction(point_before, mid_point)
            current_direction = self.get_direction(mid_point, point_after)

            turn_angle = self.get_angle(prev_direction, current_direction)
            angles.append(turn_angle)

        return angles

    @staticmethod
    def get_angle(first_vec, second_vec):
        """
        Returns the angle in degrees between the first and second vector.
        A left turn as positive angles whereas right turns have negatives.

        :param first_vec: First 2D vector
        :param second_vec: Second 3D vector
        :return: Angle between the vectors in degrees
        """
        a1, a2 = first_vec[0], first_vec[1]
        b1, b2 = second_vec[0], second_vec[1]

        angle_in_radians = math.atan2(b2, b1) - math.atan2(a2, a1)
        angle_in_degrees = math.degrees(angle_in_radians)

        return angle_in_degrees

    @staticmethod
    def get_distance_between(first_point, second_point) -> float:
        """
        Calculate Euclidean distance between two points.

        :param first_point: (x,y) coordinates of first point
        :param second_point: (x,y) coordinates of second point
        :return: Euclidean distance between the points
        """
        a1, a2 = first_point[0], first_point[1]
        b1, b2 = second_point[0], second_point[1]
        c1, c2 = (b1 - a1, b2 - a2)
        distance = math.sqrt(c1**2 + c2**2)
        return distance

    @staticmethod
    def get_direction(first_point, second_point):
        """
        Get the direction vector from the first point to the second point.

        :param first_point: (x,y) coordinates of first point
        :param second_point: (x,y) coordinates of second point
        :return: Return the difference 2D vector (second_point-first_point)
        """
        return second_point[0] - first_point[0], second_point[1] - first_point[1]

    @staticmethod
    def get_road_length(road_points):
        """
        Compute the length of the road.

        :param road_points: List of road points defining the road
        :return: Length of the road
        """
        nr_of_road_points = len(road_points)

        road_length = 0
        for i in range(1, nr_of_road_points):
            a1, a2 = road_points[i - 1][0], road_points[i - 1][1]
            b1, b2 = road_points[i][0], road_points[i][1]

            c1, c2 = (b1 - a1, b2 - a2)

            road_length += math.sqrt(c1**2 + c2**2)

        return road_length


if __name__ == "__main__":
    logging.info("road_geometry_calculator.py")
