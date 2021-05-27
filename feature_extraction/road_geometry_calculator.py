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

            prev_direction = self.__get_direction(point_before, mid_point)
            current_direction = self.__get_direction(point_after, mid_point)

            turn_angle = self.__get_angle(prev_direction, current_direction)
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

        angle_in_radians = math.atan2(b2,b1)-math.atan2(a2,a1)
        angle_in_degrees = math.degrees(angle_in_radians)

        return angle_in_degrees

    def get_direction(self, first_point, second_point):
        """
        Return the difference vector (second_point-first_point)
        """
        return (second_point[0]-first_point[0], second_point[1]-second_point[1])

