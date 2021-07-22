import math
import statistics
from feature_extraction.equi_distance_strategy import EquiDistanceStrategy
from feature_extraction.angle_based_strategy import AngleBasedStrategy
from feature_extraction.road_geometry_calculator import RoadGeometryCalculator

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
        for indexes in segment_indexes_list:
            segment = self.__get_road_segment_with_features(indexes)
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
        
        # more than 1 data point is required to calculate the standard deviation
        if len(raw_feature_data['angles']) > 1:
            road_features.std_angle = statistics.stdev(raw_feature_data["angles"])
        else:
            road_features.std_angle = 0

        road_features.mean_pivot_off = statistics.mean(raw_feature_data["pivots"])
        road_features.median_pivot_off = statistics.median(raw_feature_data["pivots"])
        road_features.max_pivot_off = max(raw_feature_data["pivots"])
        road_features.min_pivot_off = min(raw_feature_data["pivots"])
        
        if len(raw_feature_data['pivots']) > 1:
            road_features.std_pivot_off = statistics.stdev(raw_feature_data["pivots"])
        else:
            road_features.std_pivot_off = 0

        road_features.direct_distance = self.__road_geometry_calculator.get_distance_between(self.__road_points[0], self.__road_points[-1])
        road_features.road_distance = self.__road_geometry_calculator.get_road_length(self.__road_points)

        return road_features


    def __get_segment_type(self, road_segment, angle_threshold):
        """
        Return the type of segment (straight, left turn, right turn). The segment
        is defined by its start and end index that are already specified.
        """
        start_index = road_segment.start_index
        end_index = road_segment.end_index

        segment_road_points = self.__road_points[start_index:end_index+1]

        angles_lst = self.__road_geometry_calculator.extract_turn_angles(segment_road_points)

        angles_sum = sum(angles_lst)

        if angles_sum < angle_threshold and angles_sum > -angle_threshold: return SegmentType.straight
        if angles_sum >= angle_threshold: return SegmentType.l_turn
        if angles_sum <= angle_threshold: return SegmentType.r_turn



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


    
    
    def __get_road_segment_with_features(self, indexes):
        road_segment = RoadSegment()
        road_segment.start_index = indexes[0]
        road_segment.end_index = indexes[1]

        # classify segment type
        road_segment.type = self.__get_segment_type(road_segment, angle_threshold=5)

        # update angle
        road_segment.angle = self.__get_segment_angle(road_segment)

        # calculate radius
        road_segment.radius = self.__get_segment_radius(road_segment)

        return road_segment
        


if __name__ == "__main__":
    import unittest
    from parameterized import parameterized

    class FeatureExtractionTest(unittest.TestCase):
        def setUp(self):
            pass

        @parameterized.expand([
            (999,20),
            (200,12)
            ])
        def test_straight_road_equi_distance_strategy(self, distance, nr_segments):
            road_points = [(x,0) for x in range(distance+1)]
            segmentation_strategy = EquiDistanceStrategy(nr_segments)

            feature_extractor = FeatureExtractor(road_points, segmentation_strategy)

            road_features = feature_extractor.extract_features()

            self.assertEqual(road_features.direct_distance, distance)
            self.assertEqual(road_features.road_distance, distance)
            self.assertEqual(road_features.num_l_turns, 0)
            self.assertEqual(road_features.num_r_turns, 0)
            self.assertEqual(road_features.num_straights, nr_segments)
            self.assertEqual(road_features.median_angle, 0)
            self.assertEqual(road_features.total_angle, 0)
            self.assertEqual(road_features.mean_angle, 0)
            self.assertEqual(road_features.std_angle, 0)
            self.assertEqual(road_features.max_angle, 0)
            self.assertEqual(road_features.min_angle, 0)
            self.assertEqual(road_features.median_pivot_off, 0)
            self.assertEqual(road_features.mean_pivot_off, 0)
            self.assertEqual(road_features.std_pivot_off, 0)
            self.assertEqual(road_features.max_pivot_off, 0)
            self.assertEqual(road_features.min_pivot_off, 0)


        def test_90_degree_right_turn_only(self):
            nr_segments = 2
            road_points = []
            radius = 50
            angle = 90
            center_of_turn = (50, 0)

            for i in range(0, angle+1, 1):
                x = -1 * radius * math.cos(math.radians(i)) # minus for right turn
                y = radius * math.sin(math.radians(i))

                # translation of coordinates
                x = x + center_of_turn[0]

                road_points.append((x, y))

           

            segmentation_strategy = EquiDistanceStrategy(nr_segments)

            feature_extractor = FeatureExtractor(road_points, segmentation_strategy)

            road_features = feature_extractor.extract_features()

            # self.assertEqual(road_features.direct_distance, distance)
            # self.assertEqual(road_features.road_distance, distance)
            self.assertEqual(road_features.num_l_turns, 0)
            self.assertEqual(road_features.num_r_turns, nr_segments)
            self.assertEqual(road_features.num_straights, 0)
            self.assertAlmostEqual(road_features.median_angle, -angle/nr_segments, places=None, delta=2)
            self.assertAlmostEqual(road_features.total_angle, -angle, places=None, delta=2)
            self.assertAlmostEqual(road_features.mean_angle, -angle/nr_segments, places=None, delta=2)
            # self.assertEqual(road_features.std_angle, 0)
            self.assertAlmostEqual(road_features.max_angle, -angle/nr_segments, places=None, delta=2)
            self.assertAlmostEqual(road_features.min_angle, -angle/nr_segments, places=None, delta=2)
            self.assertAlmostEqual(road_features.median_pivot_off, radius, places=None, delta=2)
            self.assertAlmostEqual(road_features.mean_pivot_off, radius, places=None, delta=2)
            self.assertAlmostEqual(road_features.max_pivot_off, radius, places=None, delta=2)
            self.assertAlmostEqual(road_features.min_pivot_off, radius, places=None, delta=2)
            # self.assertEqual(road_features.std_pivot_off, 0)


        def test_90_degree_left_turn_only(self):
            nr_segments = 1
            # nr_segments = 2
            # segmentation_strategy = EquiDistanceStrategy(nr_segments)
            segmentation_strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=10)

            road_points = []
            radius = 50
            angle = 90
            center_of_turn = (0, 0)

            for i in range(0, angle+1, 1):
                x = radius * math.cos(math.radians(i)) # minus for right turn
                y = radius * math.sin(math.radians(i))

                # translation of coordinates
                x = x + center_of_turn[0]

                road_points.append((x, y))

           

            
            feature_extractor = FeatureExtractor(road_points, segmentation_strategy)

            road_features = feature_extractor.extract_features()

            # self.assertEqual(road_features.direct_distance, distance)
            # self.assertEqual(road_features.road_distance, distance)
            self.assertEqual(road_features.num_l_turns, nr_segments)
            self.assertEqual(road_features.num_r_turns, 0)
            self.assertEqual(road_features.num_straights, 0)
            self.assertAlmostEqual(road_features.median_angle, angle/nr_segments, places=None, delta=2)
            self.assertAlmostEqual(road_features.total_angle, angle, places=None, delta=2)
            self.assertAlmostEqual(road_features.mean_angle, angle/nr_segments, places=None, delta=2)
            # self.assertEqual(road_features.std_angle, 0)
            self.assertAlmostEqual(road_features.max_angle, angle/nr_segments, places=None, delta=2)
            self.assertAlmostEqual(road_features.min_angle, angle/nr_segments, places=None, delta=2)
            self.assertAlmostEqual(road_features.median_pivot_off, radius, places=None, delta=2)
            self.assertAlmostEqual(road_features.mean_pivot_off, radius, places=None, delta=2)
            self.assertAlmostEqual(road_features.max_pivot_off, radius, places=None, delta=2)
            self.assertAlmostEqual(road_features.min_pivot_off, radius, places=None, delta=2)
            # self.assertEqual(road_features.std_pivot_off, 0)


        def test_left_then_right_turn_segments_90_degrees_each(self):
            nr_segments = 2
            road_points = []
            radius = 50
            angle = 90
            center_of_turn = (0, 0)

            # left turn
            for i in range(0, angle+1, 1):
                x = radius * math.cos(math.radians(i)) # minus for right turn
                y = radius * math.sin(math.radians(i))

                # translation of coordinates
                x = x + center_of_turn[0]
                y = y + center_of_turn[1]

                road_points.append((x, y))


            # right turn
            center_of_turn = (x, y+radius)
            for i in range(1, angle+1, 1):
                x = -radius * math.sin(math.radians(i)) # minus for right turn
                y = -radius * math.cos(math.radians(i))

                # translation of coordinates
                x = x + center_of_turn[0]
                y = y + center_of_turn[1]

                road_points.append((x, y))

           

            segmentation_strategy = EquiDistanceStrategy(nr_segments)

            feature_extractor = FeatureExtractor(road_points, segmentation_strategy)

            road_features = feature_extractor.extract_features()

            # pythagoras
            self.assertAlmostEqual(road_features.direct_distance, math.sqrt(2*((2*radius)**2)), places=None, delta=2)
            
            # half of a circle
            self.assertAlmostEqual(road_features.road_distance, math.pi*radius, places=None, delta=2)
            self.assertEqual(road_features.num_l_turns, 1)
            self.assertEqual(road_features.num_r_turns, 1)
            self.assertEqual(road_features.num_straights, 0)
            self.assertAlmostEqual(road_features.median_angle, 0, places=None, delta=2)
            self.assertAlmostEqual(road_features.total_angle, 0, places=None, delta=2)
            self.assertAlmostEqual(road_features.mean_angle, 0, places=None, delta=2)
            self.assertGreater(road_features.std_angle, 0)
            self.assertAlmostEqual(road_features.max_angle, angle, places=None, delta=2)
            self.assertAlmostEqual(road_features.min_angle, -angle, places=None, delta=2)
            self.assertAlmostEqual(road_features.median_pivot_off, radius, places=None, delta=2)
            self.assertAlmostEqual(road_features.mean_pivot_off, radius, places=None, delta=2)
            self.assertAlmostEqual(road_features.max_pivot_off, radius, places=None, delta=2)
            self.assertAlmostEqual(road_features.min_pivot_off, radius, places=None, delta=2)
            #self.assertGreater(road_features.std_pivot_off, 0)


    unittest.main()
