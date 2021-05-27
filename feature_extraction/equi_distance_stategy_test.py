import unittest
from feature_extraction.equi_distance_strategy import EquiDistanceStrategy

class EquiDistanceSegmentationTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_n5_6_straight_points(self):
        nr_of_segments = 5
        strategy = EquiDistanceStrategy(nr_of_segments)

        road_points = [(1,1),(2,1),(3,1),(4,1),(5,1),(6,1)]

        segments = strategy.extract_segments(road_points)

        self.assertEqual(len(segments), 5, "There must be {} segments.".format(nr_of_segments))

        expected_segments = [(0,1),(1,2),(2,3),(3,4),(4,5)]
        self.assertEqual(segments, expected_segments, "Segments are not correctly calculated.")

    def test_too_few_road_points_should_raise_exception(self):
        nr_of_segments = 4
        strategy = EquiDistanceStrategy(nr_of_segments)

        # 6 road points
        road_points = [(1,1),(2,1),(3,1),(4,1),(5,1),(6,1)]

        self.assertRaises(Exception, strategy.extract_segments(road_points))

    def test_last_segment_has_more_road_points_than_others(self):
        nr_of_segments = 4
        strategy = EquiDistanceStrategy(nr_of_segments)

        road_points = [(1,1),(2,1),(3,1),(4,1),(5,1),(6,1)]

        segments = strategy.extract_segments(road_points)

        expected_segments = [(0,1),(1,2),(2,3),(3,5)]
        self.assertEqual(segments, expected_segments, "Segments are not correctly calculated.")


    def test_last_segment_has_less_road_points_than_others(self):
        nr_of_segments = 3
        strategy = EquiDistanceStrategy(nr_of_segments)

        road_points = [(1,1),(2,1),(3,1),(4,1),(5,1),(6,1)]

        segments = strategy.extract_segments(road_points)

        expected_segments = [(0,2),(2,4),(4,5)]
        self.assertEqual(segments, expected_segments, "Segments are not correctly calculated.")


def run_tests():
    unittest.main()


if __name__ == "__main__":
    run_tests()