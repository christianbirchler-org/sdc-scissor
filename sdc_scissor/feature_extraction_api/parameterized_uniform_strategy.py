from .segmentation_strategy import SegmentationStrategy
from .road_geometry_calculator import RoadGeometryCalculator

seg_lengths_dict = {"1": 50, "1.5": 30, "2": 10}


class ParameterizedUniformStrategy(SegmentationStrategy):
    """
    This class segments the road based on parameters like risk factor and
    fullroad length.
    """

    def __init__(self, risk_factor: str, max_seg_length_to_full_road):
        """

        :param risk_factor: Risk factor of the driving AI.
        :param max_seg_length_to_full_road: Relative size of the longest allowed segment compared to the full road length.
        """
        # dependend on the risk factor
        self.__seg_length_in_meters = seg_lengths_dict[risk_factor]
        # dependend on the length of the full road
        self.__max_seg_length_in_meters = None

        self.__max_seg_length_to_full_road = max_seg_length_to_full_road

        self.__road_geometry_calculator = RoadGeometryCalculator()

    # TODO: formalize the clear segmentaion process
    def extract_segments(self, road_points):
        """
        Returns a list of tuples that contain start end end indexes of road
        segments.

        :param road_points: List of coordinates specifying the road.
        :return: List of start and end indexes defining the start and end  road points of segments.
        """
        road_length = self.__road_geometry_calculator.get_road_length(road_points)

        self.__max_seg_length_in_meters = road_length * self.__max_seg_length_to_full_road

        if self.__seg_length_in_meters > self.__max_seg_length_in_meters:
            raise Exception("Road is too short for the required segment length.")

        # iterate over road points until we reach the desired segment length
        end = 0
        start = 0
        current_segment_length = 0
        segment_indexes = []
        for i in range(1, len(road_points)):
            current_elementary_segment = road_points[i - 1 : i + 1]
            current_segment_length += self.__road_geometry_calculator.get_road_length(current_elementary_segment)

            if current_segment_length > self.__max_seg_length_in_meters:
                raise Exception("Max segment reached.")

            # segment reached its required length
            if (current_segment_length >= self.__seg_length_in_meters) or (i == len(road_points) - 1):
                current_segment_length = 0
                end = i
                segment_indexes.append((start, end))
                start = i  # set start index for the next segment

        return segment_indexes


if __name__ == "__main__":
    import unittest

    class ParameterizedUniformStrategyTest(unittest.TestCase):
        def test_straight_only(self):
            strategy = ParameterizedUniformStrategy("2", 0.05)

            road_points = [(x, 0) for x in range(1000)]

            segments = strategy.extract_segments(road_points)

            expected_segments = [(x * 10, x * 10 + 10) for x in range(99)]
            expected_segments.append((990, 999))
            self.assertEqual(segments, expected_segments, "Segment indexes are wrong.")

        def test_road_is_too_short(self):
            strategy = ParameterizedUniformStrategy("2", 0.0005)

            road_points = [(x, 0) for x in range(1000)]

            with self.assertRaises(Exception):
                strategy.extract_segments(road_points)

    unittest.main()
