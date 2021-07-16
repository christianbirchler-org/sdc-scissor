from segmentation_strategy import SegmentationStrategy
from road_geometry_calculator import RoadGeometryCalculator

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
                current_angle = sum(self.__road_geometry_calculator.extract_turn_angles(current_road_piece))
            
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


    unittest.main()
