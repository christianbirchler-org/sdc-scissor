import math
import statistics
from equi_distance_strategy import EquiDistanceStrategy
from road_geometry_calculator import RoadGeometryCalculator

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
    def __init__(self, road_points, segmentation_strategy):
        self.__road_features = RoadFeatures()
        self.__road_points = road_points
        self.__segments = []
        self.__road_geometry_calculator = RoadGeometryCalculator()

        # TODO: find a more usable way to instantiate the desired strategy
        self.__segmentation_strategy = segmentation_strategy

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

    def __get_full_road_features_from(self, segments: list[RoadSegment]) -> RoadFeatures:
        road_features = RoadFeatures()

        raw_feature_data = {
            "angles": [],
            "pivots": []
        }

        for segment in segments:
            if segment.type == SegmentType.l_turn: road_features.num_l_turns += 1
            elif segment.type == SegmentType.r_turn: road_features.num_r_turns += 1
            elif segment.type == SegmentType.straight: road_features.num_straights += 1
            road_features.total_angle += segment.angle

            # these lists allows a simpler calculation of the statistics
            raw_feature_data["angles"].append(segment.angle)
            raw_feature_data["pivots"].append(segment.radius)

        road_features.mean_angle = statistics.mean(raw_feature_data["angles"])
        road_features.median_angle = statistics.median(raw_feature_data["angles"])
        road_features.max_angle = max(raw_feature_data["angles"])
        road_features.min_angle = min(raw_feature_data["angles"])
        road_features.std_angle = statistics.stdev(raw_feature_data["angles"])

        road_features.mean_pivot_off = statistics.mean(raw_feature_data["pivots"])
        road_features.median_pivot_off = statistics.median(raw_feature_data["pivots"])
        road_features.max_pivot_off = max(raw_feature_data["pivots"])
        road_features.min_pivot_off = min(raw_feature_data["pivots"])
        road_features.std_pivot_off = statistics.stdev(raw_feature_data["pivots"])

        road_features.direct_distance = self.__road_geometry_calculator.get_distance_between(self.__road_points[0], self.__road_points[-1])
        road_features.road_distance = self.__road_geometry_calculator.get_road_length(self.__road_points)

        return road_features


    def __get_segment_type(self, road_segment):
        """
        Return the type of segment (straight, left turn, right turn). The segment
        is defined by its start and end index that are already specified.
        """
        start_index = road_segment.start_index
        end_index = road_segment.end_index

        segment_road_points = self.__road_points[start_index:end_index+1]

        angles_lst = self.__road_geometry_calculator.extract_turn_angles(segment_road_points)

        angles_sum = sum(angles_lst)

        if angles_sum < 5 and angles_sum > -5: return SegmentType.straight
        if angles_sum >= 5: return SegmentType.l_turn
        if angles_sum <= 5: return SegmentType.r_turn


        pass


    def __get_segment_angle(self, road_segment):
        start_index = road_segment.start_index
        end_index = road_segment.end_index

        segment_road_points = self.__road_points[start_index:end_index+1]

        angles_lst = self.__road_geometry_calculator.extract_turn_angles(segment_road_points)

        angles_sum = sum(angles_lst)

        return angles_sum


    def __get_segment_radius(self, road_segment):
        if road_segment.type == SegmentType.straight: return 0

        start_index = road_segment.start_index
        end_index = road_segment.end_index

        segment_road_points = self.__road_points[start_index:end_index+1]

        angles_lst = self.__road_geometry_calculator.extract_turn_angles(segment_road_points)
        segment_length = self.__road_geometry_calculator.get_road_length(segment_road_points)

        angles_sum = sum(angles_lst)

        unsigned_angle = abs(angles_sum)

        
        # C=2*pi*r
        proportion = unsigned_angle / 360
        circle_length = segment_length / proportion
        radius = circle_length /(2 * math.pi)

        return radius


    
    
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
    import unittest

    class FeatureExtractionTest(unittest.TestCase):
        def setUp(self):
            pass

        def test_straight_road(self):
            pass

    unittest.main()
