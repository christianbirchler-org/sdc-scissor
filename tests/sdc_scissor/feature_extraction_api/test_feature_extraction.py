import math
import shutil
from pathlib import Path

import pytest
from parameterized import parameterized
from pytest import approx

from sdc_scissor.feature_extraction_api.angle_based_strategy import AngleBasedStrategy
from sdc_scissor.feature_extraction_api.equi_distance_strategy import EquiDistanceStrategy
from sdc_scissor.feature_extraction_api.feature_extraction import FeatureExtractor, RoadFeatures
from sdc_scissor.testing_api.test import Test


@pytest.fixture
def tmp_dir():
    file_dir_str = "tmp-dir"
    file_dir = Path(file_dir_str)
    file_dir.mkdir(parents=True)
    yield file_dir
    shutil.rmtree(file_dir)


class TestFeatureExtraction:
    @parameterized.expand([[999, 20], [200, 12]])
    def test_straight_road_equi_distance_strategy(self, distance, nr_segments):
        road_points = [[x, 0] for x in range(distance + 1)]
        test = Test(0, road_points, "NOT_EXECUTED")
        segmentation_strategy = EquiDistanceStrategy(nr_segments)

        feature_extractor = FeatureExtractor(segmentation_strategy)

        road_features = feature_extractor.extract_features(test)

        assert road_features.direct_distance == distance
        assert road_features.road_distance == distance
        assert road_features.num_l_turns == 0
        assert road_features.num_r_turns == 0
        assert road_features.num_straights == nr_segments
        assert road_features.median_angle == 0
        assert road_features.total_angle == 0
        assert road_features.mean_angle == 0
        assert road_features.std_angle == 0
        assert road_features.max_angle == 0
        assert road_features.min_angle == 0
        assert road_features.median_pivot_off == 0
        assert road_features.mean_pivot_off == 0
        assert road_features.std_pivot_off == 0
        assert road_features.max_pivot_off == 0
        assert road_features.min_pivot_off == 0

    @parameterized.expand([(20, 1), (33, 1), (68, 1), (200, 1), (287, 1)])
    def test_straight_road_angle_based_strategy(self, distance, nr_segments):
        road_points = [[x, 0] for x in range(distance + 1)]
        test = Test(0, road_points, "NOT_EXECUTED")
        segmentation_strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=10)

        feature_extractor = FeatureExtractor(segmentation_strategy)

        road_features = feature_extractor.extract_features(test)

        assert road_features.direct_distance == distance
        assert road_features.road_distance == distance
        assert road_features.num_l_turns == 0
        assert road_features.num_r_turns == 0
        assert road_features.num_straights == nr_segments
        assert road_features.median_angle == 0
        assert road_features.total_angle == 0
        assert road_features.mean_angle == 0
        assert road_features.std_angle == 0
        assert road_features.max_angle == 0
        assert road_features.min_angle == 0
        assert road_features.median_pivot_off == 0
        assert road_features.mean_pivot_off == 0
        assert road_features.std_pivot_off == 0
        assert road_features.max_pivot_off == 0
        assert road_features.min_pivot_off == 0

    def test_90_degree_right_turn_only(self):
        nr_segments = 2
        road_points = []
        radius = 50
        angle = 90
        center_of_turn = (50, 0)

        for i in range(0, angle + 1, 1):
            x = -1 * radius * math.cos(math.radians(i))  # minus for right turn
            y = radius * math.sin(math.radians(i))

            # translation of coordinates
            x = x + center_of_turn[0]

            road_points.append([x, y])

        segmentation_strategy = EquiDistanceStrategy(nr_segments)

        feature_extractor = FeatureExtractor(segmentation_strategy)

        test = Test(0, road_points, "NOT_EXECUTED")
        road_features = feature_extractor.extract_features(test)
        assert road_features.num_l_turns == 0
        assert road_features.num_r_turns == nr_segments
        assert road_features.num_straights == 0
        assert road_features.median_angle == approx(-angle / nr_segments, abs=2)
        assert road_features.total_angle == approx(-angle, abs=2)
        assert road_features.mean_angle == approx(-angle / nr_segments, abs=2)
        assert road_features.max_angle == approx(-angle / nr_segments, abs=2)
        assert road_features.min_angle == approx(-angle / nr_segments, abs=2)
        assert road_features.median_pivot_off == approx(radius, abs=2)
        assert road_features.mean_pivot_off == approx(radius, abs=2)
        assert road_features.max_pivot_off == approx(radius, abs=2)
        assert road_features.min_pivot_off == approx(radius, abs=2)

    def test_90_degree_left_turn_only_angle_based(self):
        nr_segments = 1
        segmentation_strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=10)
        road_points = []
        radius = 50
        angle = 90
        center_of_turn = (0, 0)

        for i in range(0, angle + 1, 1):
            x = radius * math.cos(math.radians(i))  # minus for right turn
            y = radius * math.sin(math.radians(i))

            x = x + center_of_turn[0]

            road_points.append([x, y])

        test = Test(0, road_points, "NOT_EXECUTED")
        feature_extractor = FeatureExtractor(segmentation_strategy)

        road_features = feature_extractor.extract_features(test)

        assert road_features.num_l_turns == nr_segments
        assert road_features.num_r_turns == 0
        assert road_features.num_straights == 0
        assert road_features.median_angle == approx(angle / nr_segments, abs=2)
        assert road_features.total_angle == approx(angle, abs=2)
        assert road_features.mean_angle == approx(angle / nr_segments, abs=2)
        assert road_features.max_angle == approx(angle / nr_segments, abs=2)
        assert road_features.min_angle == approx(angle / nr_segments, abs=2)
        assert road_features.median_pivot_off == approx(radius, abs=2)
        assert road_features.mean_pivot_off == approx(radius, abs=2)
        assert road_features.max_pivot_off == approx(radius, abs=2)
        assert road_features.min_pivot_off == approx(radius, abs=2)

    def test_90_degree_right_turn_only_angle_based(self):
        nr_segments = 1
        segmentation_strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=10)
        road_points = []
        radius = 50
        angle = 90
        center_of_turn = (0, 0)

        for i in range(0, angle + 1, 1):
            x = -radius * math.cos(math.radians(i))  # minus for right turn
            y = radius * math.sin(math.radians(i))

            x = x + center_of_turn[0]

            road_points.append([x, y])

        test = Test(0, road_points, "NOT_EXECUTED")
        feature_extractor = FeatureExtractor(segmentation_strategy)

        road_features = feature_extractor.extract_features(test)

        assert road_features.num_l_turns == 0
        assert road_features.num_r_turns == nr_segments
        assert road_features.num_straights == 0
        assert road_features.median_angle == approx(-angle / nr_segments, abs=2)
        assert road_features.total_angle == approx(-angle, abs=2)
        assert road_features.mean_angle == approx(-angle / nr_segments, abs=2)
        assert road_features.max_angle == approx(-angle / nr_segments, abs=2)
        assert road_features.min_angle == approx(-angle / nr_segments, abs=2)
        assert road_features.median_pivot_off == approx(radius, abs=2)
        assert road_features.mean_pivot_off == approx(radius, abs=2)
        assert road_features.max_pivot_off == approx(radius, abs=2)
        assert road_features.min_pivot_off == approx(radius, abs=2)

    def test_left_then_right_turn_segments_90_degrees_each(self):
        nr_segments = 2
        road_points = []
        radius = 50
        angle = 90
        center_of_turn = (0, 0)

        # left turn
        for i in range(0, angle + 1, 1):
            x = radius * math.cos(math.radians(i))  # minus for right turn
            y = radius * math.sin(math.radians(i))

            # translation of coordinates
            x = x + center_of_turn[0]
            y = y + center_of_turn[1]

            road_points.append([x, y])

        # right turn
        center_of_turn = (x, y + radius)
        for i in range(1, angle + 1, 1):
            x = -radius * math.sin(math.radians(i))  # minus for right turn
            y = -radius * math.cos(math.radians(i))

            # translation of coordinates
            x = x + center_of_turn[0]
            y = y + center_of_turn[1]

            road_points.append([x, y])

        segmentation_strategy = EquiDistanceStrategy(nr_segments)
        feature_extractor = FeatureExtractor(segmentation_strategy)
        test = Test(0, road_points, "NOT_EXECUTED")

        road_features = feature_extractor.extract_features(test)

        # pythagoras
        assert road_features.direct_distance == approx(math.sqrt(2 * ((2 * radius) ** 2)), abs=2)

        # half of a circle
        assert road_features.road_distance == approx(math.pi * radius, abs=2)
        assert road_features.num_l_turns == 1
        assert road_features.num_r_turns == 1
        assert road_features.num_straights == 0
        assert road_features.median_angle == approx(0, abs=2)
        assert road_features.total_angle == approx(0, abs=2)
        assert road_features.mean_angle == approx(0, abs=2)
        assert road_features.max_angle == approx(angle, abs=2)
        assert road_features.min_angle == approx(-angle, abs=2)
        assert road_features.median_pivot_off == approx(radius, abs=2)
        assert road_features.mean_pivot_off == approx(radius, abs=2)
        assert road_features.max_pivot_off == approx(radius, abs=2)
        assert road_features.min_pivot_off == approx(radius, abs=2)

    def test_no_diversity(self, mocker):
        angle_based_strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=10)
        feature_extractor = FeatureExtractor(segmentation_strategy=angle_based_strategy)

        mock_test = mocker.patch("sdc_scissor.testing_api.test.Test")
        mock_test.road_points = [[x, 0] for x in range(100)]

        road_features = feature_extractor.extract_features(mock_test)

        expected = 0
        actual = road_features.mean_road_diversity
        assert actual == expected

    def test_with_small_diversity(self, mocker):
        angle_based_strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=10)
        feature_extractor = FeatureExtractor(segmentation_strategy=angle_based_strategy)

        mock_test = mocker.patch("sdc_scissor.testing_api.test.Test")
        mock_test.road_points = [[x, 0] for x in range(100)]
        mock_test.road_points.append([101, 1])

        road_features = feature_extractor.extract_features(mock_test)

        expected = 0
        actual = road_features.mean_road_diversity
        assert actual != expected

    def test_with_no_full_road_diversity(self, mocker):
        angle_based_strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=10)
        feature_extractor = FeatureExtractor(segmentation_strategy=angle_based_strategy)

        mock_test = mocker.patch("sdc_scissor.testing_api.test.Test")
        mock_test.road_points = [[x, 0] for x in range(100)]

        road_features = feature_extractor.extract_features(mock_test)

        expected = 0
        actual = road_features.full_road_diversity
        assert actual == expected

    def test_with_small_full_road_diversity(self, mocker):
        angle_based_strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=10)
        feature_extractor = FeatureExtractor(segmentation_strategy=angle_based_strategy)

        mock_test = mocker.patch("sdc_scissor.testing_api.test.Test")
        mock_test.road_points = [[x, 0] for x in range(100)]
        mock_test.road_points.append([101, 1])

        road_features = feature_extractor.extract_features(mock_test)

        expected = 0
        actual = road_features.full_road_diversity
        assert actual != expected

    def test_save_to_csv(self, tmp_dir):
        road_features = RoadFeatures()
        id_string = "id"
        file_dir = tmp_dir
        FeatureExtractor.save_to_csv(road_features=[(id_string, road_features)], out_dir=file_dir)
