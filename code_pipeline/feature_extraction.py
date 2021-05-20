
class RoadFeatures:
    
    def __init__(self):
        self.direct_distance = 0
        self.road_distance = 0
        self.num_l_turns = 0
        self.num_r_turns = 0
        self.num_straights = 0
        self.median_angle = 0
        self.total_angle = 0
        self.mean_angle = 0
        self.std_angle = 0
        self.max_angle = 0
        self.min_angle = 0
        self.median_pivot_off = 0
        self.mean_pivot_off = 0
        self.std_pivot_off = 0
        self.max_pivot_off = 0
        self.min_pivot_off = 0
        self.start_time = 0
        self.end_time = 0
        self.duration_seconds = 0
        self.safety = 0
    


class FeatureExtractor:
    def __init__(self):
        self.__road_features = RoadFeatures()


    def extract_features(self, road_points):
        """
        Input is a list of (x,y) tuples which defines the road.
        This function extract the angles of segments.
        """
        
        # iterate over all road points
        for i in range(2, len(road_points)):
            # calculate angle between previous direction and vector from
            # previous point to the current one
            
            point_before = road_points[i-2]
            mid_point = road_points[i-1]
            point_after = road_points[i]

            prev_direction = self.__get_direction(point_before, mid_point)
            current_direction = self.__get_direction(point_after, mid_point)

            turn_angle = self.__get_angle(prev_direction, current_direction)

    

    
    ############################################################################
    # IMPLEMENTATION DETAILS
    ############################################################################
    def __get_angle(self, first_vec, second_vec):
        """
        Returns the angle in degrees between the first and second vector.
        A left turn as positive angles whereas right turns have negatives.
        """
        a1, a2 = first_vec[0], first_vec[1]
        b1, b2 = second_vec[0], second_vec[1]

        angle_in_radians = math.atan2(b2,b1)-math.atan2(a2,a1)
        angle_in_degrees = math.degrees(angle_in_radians)

        return angle_in_degrees

    def __get_direction(self, first_point, second_point):
        """
        Return the difference vector (second_point-first_point)
        """
        return (second_point[0]-first_point[0], second_point[1]-second_point[1])
