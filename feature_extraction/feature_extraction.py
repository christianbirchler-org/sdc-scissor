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


class FeatureExtractor:
    def __init__(self, road_points):
        self.__road_features = RoadFeatures()

        self.__road_points = road_points
        # store all angles (change of direction for the next road point)
        self.__angles = None
        self.__segments = None

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
        self.__segments = self.__segmentation_strategy.extract_segments(self.__road_points)

        # calculate segment features

        # calculate fullroad features
        


if __name__ == "__main__":
    print("Do some testing here")
