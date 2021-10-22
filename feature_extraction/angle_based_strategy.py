from feature_extraction.segmentation_strategy import SegmentationStrategy
from feature_extraction.road_geometry_calculator import RoadGeometryCalculator

class AngleBasedStrategy(SegmentationStrategy):
    """
    Define segments based on identified turns. The center of a turn where the
    angles possibly reaches the maximum will also be the center of the segment.
    Straight segments are identified where no significant turn angles are present.
    """

    def __init__(self, angle_threshold=5, decision_distance=10):
        self.__road_geometry_calculator = RoadGeometryCalculator()
        self.__angle_threshold = angle_threshold
        self.__decision_distance = decision_distance

    def extract_segments(self, road_points) -> list[tuple[int, int]]:
        # iterate according to the decision distance
        segment_indexes = []
        segment_start_index = 0
        segment_end_index = 0
        current_road_piece_start_index = 0
        current_road_piece_end_index = 0
        current_distance = 0
        current_angle = 0
        previous_angle = 0
        is_first_piece = True
        is_last_iteration = False

        for i in range(len(road_points)):

            # check if it is the last iteration
            if i == len(road_points)-1: is_last_iteration = True

            # the start of a new piece has to be 2 indexes ahead of the current i
            if current_road_piece_start_index == i+1:
                current_road_piece_end_index = i+2
            else:
                current_road_piece_end_index = i + 1

            # define the current road piece to calculate the turn angle and distane
            current_road_piece = road_points[current_road_piece_start_index:current_road_piece_end_index+1]
            
            # calculate the road piece distance defined above
            current_distance = self.__road_geometry_calculator.get_road_length(current_road_piece)
            
            # check if the distance of the current road piece is long enough or it is the last iteration
            if (current_distance >= self.__decision_distance) or is_last_iteration:
                previous_angle = current_angle

                # calculate the angle of the current road piece
                # TODO: ensure that the road piece to calculate the angle has enough points!!! (e.g., use temporarily a longer road piece)
                if len(current_road_piece) == 2 and current_road_piece_start_index > 0:
                    tmp_current_road_piece = road_points[current_road_piece_start_index-1:current_road_piece_end_index+1]
                else:
                    tmp_current_road_piece = current_road_piece
                current_angle = sum(self.__road_geometry_calculator.extract_turn_angles(tmp_current_road_piece))
            
                # define start and end index of segment iff the angle of the current road piece is different
                if (self.__has_current_angle_changed(previous_angle, current_angle) and not is_first_piece) or is_last_iteration:
                    segment_end_index = i
                    segment_indexes.append((segment_start_index, segment_end_index))
                    segment_start_index = segment_end_index + 1
                    current_road_piece_start_index = segment_start_index
                else:
                    current_road_piece_start_index = current_road_piece_end_index + 1
                    is_first_piece = False

        return segment_indexes

        # decide type of segment based on angle and its threshold
        # define segment when the type of segment will change
    

    def __has_current_angle_changed(self, previous_angle, current_angle):
        angle_threshold = self.__angle_threshold
        if current_angle <= previous_angle+angle_threshold and current_angle >= previous_angle-angle_threshold:
            return False
        else:
            return True


if __name__ == '__main__':
    import unittest
    import math

    class AngleBasedSegmentationTest(unittest.TestCase):
        def test_90_degree_right_turn_only(self):
            road_points = []
            radius = 50
            center_of_turn = (50, 0)

            for i in range(0, 91, 1):
                x = -1 * radius * math.cos(math.radians(i)) # minus for right turn
                y = radius * math.sin(math.radians(i))

                # translation of coordinates
                x = x + center_of_turn[0]

                road_points.append((x, y))


            strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=10)

            segment_indexes = strategy.extract_segments(road_points)

            self.assertEqual(0, segment_indexes[0][0], 'wrong start index!')
            self.assertEqual(len(road_points)-1, segment_indexes[0][1], 'wrong end index!')

        def test_90_degree_left_and_right_turn_each(self):
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

            strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=6)

            segment_indexes = strategy.extract_segments(road_points)

            self.assertEqual(2, len(segment_indexes), 'There must be two segments!')

            end_index_of_first_segment = segment_indexes[0][1]
            start_index_of_second_segment = segment_indexes[1][0]
            expected_mid_point_index = len(road_points)//2

            self.assertAlmostEqual(end_index_of_first_segment, start_index_of_second_segment, places=None, delta=5)
            self.assertAlmostEqual(end_index_of_first_segment, expected_mid_point_index, places=None, delta=5)
            self.assertAlmostEqual(start_index_of_second_segment, expected_mid_point_index, places=None, delta=5)

        def test_straight_segment_only(self):

            road_points = [(x, 10) for x in range(10, 200, 5)]

            strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=10)

            segment_indexes = strategy.extract_segments(road_points)

            self.assertEqual(1, len(segment_indexes), 'Straight road must result in only one segment!')
            self.assertEqual(0, segment_indexes[0][0], 'wrong start index!')
            self.assertEqual(len(road_points)-1, segment_indexes[0][1], 'wrong end index!')

        def test_left_turn_then_straight(self):

            strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=10)

            road_points = []
            radius = 50
            angle = 90
            center_of_turn = (100, 0)

            # left turn
            for i in range(0, angle+1, 1):
                x = radius * math.cos(math.radians(i)) # minus for right turn
                y = radius * math.sin(math.radians(i))

                # translation of coordinates
                x = x + center_of_turn[0]
                y = y + center_of_turn[1]

                road_points.append((x, y))

            straight_road_points = [(x, 50) for x in range(99, -1, -3)]

            road_points = road_points + straight_road_points

            segment_indexes = strategy.extract_segments(road_points)

            self.assertEqual(2, len(segment_indexes), 'there must be two segments!')

            first_segment_start_index = segment_indexes[0][0]
            first_segment_end_index = segment_indexes[0][1]
            second_segment_start_index = segment_indexes[1][0]
            second_segment_end_index = segment_indexes[1][1]

            self.assertEqual(0, first_segment_start_index)
            self.assertEqual(len(road_points)-1, second_segment_end_index)
            self.assertAlmostEqual(first_segment_end_index, 90, places=None, delta=5)
            self.assertAlmostEqual(second_segment_start_index, 91, places=None, delta=5)




        def test_frenetic_generated_road(self):

            road_points = [(66.38752953287502, 78.01492758476358), (66.39549279998235, 88.01492441408193), (63.41488386330962, 97.56039299171744), (59.39849432596085, 106.71837394192012), (53.717347876135484, 114.94786815576077), (45.71861092315158, 120.94955184927294), (35.923362286475445, 122.96278411249901), (26.205075299578844, 120.60590099271641), (17.811834039492837, 115.1695877980973), (12.078084922014867, 106.97665663411084), (10.0, 97.19496132824005), (13.48150774832019, 87.82057581246428), (20.764260856833666, 80.96772916596494), (29.79153825268792, 76.66560610655593), (39.428935001131215, 73.99716388063186), (48.20671802392773, 69.20649323815337), (55.656007423636034, 62.53505505441866), (62.62894703718282, 55.3672022974328), (69.3230484201203, 47.93827191177469), (74.39518316897082, 39.320067395200304), (75.92736990007486, 29.438144312063663), (74.25081132886308, 19.579688481798136), (71.38208886203154, 10.0)]

            strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=10)

            segment_indexes = strategy.extract_segments(road_points)

            print(segment_indexes)

        def test_angle_based_segmentation(self):

            road_points = [(20,20), (50,30), (70,50), (80,80), (70,110), (50,130), (50,150), (60,160), (80,170), (100,170), (120,160), (140,120), (150,80), (150,50), (150,30), (150,20)]

            segmentation_strategy = AngleBasedStrategy(angle_threshold=10, decision_distance=10)
            segments = segmentation_strategy.extract_segments(road_points)
            
            self.assertTrue(False)



    unittest.main()
