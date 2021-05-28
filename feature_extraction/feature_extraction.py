from feature_extraction.segmentation_strategies.equi_distance_strategy import EquiDistanceStrategy

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

  
class RoadSegment:
    def __init__(self):
        self.start_index = None
        self.end_index = None
        self.type = None
        self.angle = None
        self.radius = None


class SegmentType:
    l_turn = "left_turn"
    r_turn = "right_turn"
    straight = "straight"


class FeatureExtractor:
    def __init__(self, road_points):
        self.__road_features = RoadFeatures()
        self.__road_points = road_points
        self.__segments = []

        # TODO: find a more usable way to instantiate the desired strategy
        self.__segmentation_strategy = EquiDistanceStrategy()

    def extract_features(self):
        """
        Input is a list of (x,y) tuples which defines the road.
        This function extract the angles and radius of segments.
        Futhermore, the statistics of angles and radius are calculated.
        """
        
        # get turn angles
        #self.__angles = self.__extract_turn_angles(self.__road_points)

        # define segments (allow different strategies)
        segment_indexes_list = self.__segmentation_strategy.extract_segments(self.__road_points)

        # calculate segment features
        for segment_indexes in range(len(segment_indexes_list)):
            segment = self.__get_road_segment_with_features(segment_indexes)
            self.__segments.append(segment)

        self.__road_features = self.__get_full_road_features_from(self.__segments)

        return self.__road_features
            
    

    ############################################################################
    #       IMPLEMENTATION DETAILS BELOW
    ############################################################################

    def __get_full_road_features_from(segments):
        pass


    def __get_segment_type(self, road_segment):
        pass


    def __get_segment_angle(self, road_segment):
        pass


    def __get_segment_radius(self, road_segment):
        pass
    
    
    def __get_road_segment_with_features(self, i):
        road_segment = RoadSegment()
        road_segment.start_index = self.__road_points[i][0]
        road_segment.end_index = self.__road_points[i][1]

        # classify segment type
        road_segment.type = self.__get_segment_type(road_segment)

        # update angle
        road_segment.angle = self.__get_segment_angle(road_segment)

        # calculate radius
        road_segment.radius = self.__get_segment_radius(road_segment)

        return road_segment
        


if __name__ == "__main__":
    print("Do some testing here")
