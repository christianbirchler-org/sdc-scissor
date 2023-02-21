from sdc_scissor.feature_extraction_api.segmentation_strategy import SegmentationStrategy


class EquiDistanceStrategy(SegmentationStrategy):
    """
    Define segments with equal lengts. The last segment might be different to
    the others since there might be a remainder while dividing the road into
    predefined number of segments.
    """

    def __init__(self, number_of_segments):
        """
        Initialize the strategy by providing the number of segments that should be generated

        :param number_of_segments: The number of segments with equal distances that should be generated
        """
        super().__init__()
        self.__number_of_segments = number_of_segments

    def extract_segments(self, road_points):
        """
        Extract the segments of the road specified by the road points

        :param road_points: Road points defining the road
        :return: List of indexes representing the start and end point of segments
        """
        segments = []

        # only two road points for a segment
        max_number_of_possible_segments = len(road_points) - 1

        number_of_road_points = len(road_points)

        if number_of_road_points < self.__number_of_segments:
            raise Exception("Not enough road points.")

        # TODO: Verify if this calculation is correct. I am not sure!
        road_points_per_segment = 1 + round(max_number_of_possible_segments / self.__number_of_segments)

        # calculate for each segments its start/end road point indeces
        end = 0
        for i in range(self.__number_of_segments):
            start = end

            # check if last segment because last segment might have more/less points
            if i == self.__number_of_segments - 1:
                end = len(road_points) - 1
            else:
                end = start + road_points_per_segment - 1

            current_segment = (start, end)
            segments.append(current_segment)

        return segments


if __name__ == "__main__":
    import unittest

    class EquiDistanceSegmentationTest(unittest.TestCase):
        def setUp(self):
            pass

        def test_n5_6_straight_points(self):
            nr_of_segments = 5
            strategy = EquiDistanceStrategy(nr_of_segments)

            road_points = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)]

            segments = strategy.extract_segments(road_points)

            self.assertEqual(len(segments), 5, "There must be {} segments.".format(nr_of_segments))

            expected_segments = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
            self.assertEqual(segments, expected_segments, "Segments are not correctly calculated.")

        def test_too_few_road_points_should_raise_exception(self):
            nr_of_segments = 4
            strategy = EquiDistanceStrategy(nr_of_segments)

            # 6 road points
            road_points = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)]

            self.assertRaises(Exception, strategy.extract_segments(road_points))

        def test_last_segment_has_more_road_points_than_others(self):
            nr_of_segments = 4
            strategy = EquiDistanceStrategy(nr_of_segments)

            road_points = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)]

            segments = strategy.extract_segments(road_points)

            expected_segments = [(0, 1), (1, 2), (2, 3), (3, 5)]
            self.assertEqual(segments, expected_segments, "Segments are not correctly calculated.")

        def test_last_segment_has_less_road_points_than_others(self):
            nr_of_segments = 3
            strategy = EquiDistanceStrategy(nr_of_segments)

            road_points = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)]

            segments = strategy.extract_segments(road_points)

            expected_segments = [(0, 2), (2, 4), (4, 5)]
            self.assertEqual(segments, expected_segments, "Segments are not correctly calculated.")

    unittest.main()
