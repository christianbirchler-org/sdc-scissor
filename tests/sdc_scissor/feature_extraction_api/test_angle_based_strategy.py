import logging
import math

from pytest import approx

from sdc_scissor.feature_extraction_api.angle_based_strategy import AngleBasedStrategy


class TestAngleBasedSegmentation:
    def test_90_degree_right_turn_only(self):
        road_points = []
        radius = 50
        center_of_turn = (50, 0)

        for i in range(0, 91, 1):
            x = -1 * radius * math.cos(math.radians(i))  # minus for right turn
            y = radius * math.sin(math.radians(i))

            # translation of coordinates
            x = x + center_of_turn[0]

            road_points.append((x, y))

        strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=10)

        segment_indexes = strategy.extract_segments(road_points)

        assert 0 == segment_indexes[0][0]
        assert (len(road_points) - 1) == segment_indexes[0][1]

    def test_90_degree_left_and_right_turn_each(self):
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

            road_points.append((x, y))

        # right turn
        center_of_turn = (x, y + radius)
        for i in range(1, angle + 1, 1):
            x = -radius * math.sin(math.radians(i))  # minus for right turn
            y = -radius * math.cos(math.radians(i))

            # translation of coordinates
            x = x + center_of_turn[0]
            y = y + center_of_turn[1]

            road_points.append((x, y))

        strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=6)

        segment_indexes = strategy.extract_segments(road_points)

        assert 2 == len(segment_indexes)

        end_index_of_first_segment = segment_indexes[0][1]
        start_index_of_second_segment = segment_indexes[1][0]
        expected_mid_point_index = len(road_points) // 2

        assert end_index_of_first_segment == approx(start_index_of_second_segment, abs=5)
        assert end_index_of_first_segment == approx(expected_mid_point_index, abs=5)
        assert start_index_of_second_segment == approx(expected_mid_point_index, abs=5)

    def test_straight_segment_only(self):
        road_points = [(x, 10) for x in range(10, 200, 5)]

        strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=10)

        segment_indexes = strategy.extract_segments(road_points)

        assert 1 == len(segment_indexes)
        assert 0 == segment_indexes[0][0]
        assert (len(road_points) - 1) == segment_indexes[0][1]

    def test_left_turn_then_straight(self):
        strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=10)

        road_points = []
        radius = 50
        angle = 90
        center_of_turn = (100, 0)

        # left turn
        for i in range(0, angle + 1, 1):
            x = radius * math.cos(math.radians(i))  # minus for right turn
            y = radius * math.sin(math.radians(i))

            # translation of coordinates
            x = x + center_of_turn[0]
            y = y + center_of_turn[1]

            road_points.append((x, y))

        straight_road_points = [(x, 50) for x in range(99, -1, -3)]

        road_points = road_points + straight_road_points

        segment_indexes = strategy.extract_segments(road_points)

        assert 2 == len(segment_indexes)

        first_segment_start_index = segment_indexes[0][0]
        first_segment_end_index = segment_indexes[0][1]
        second_segment_start_index = segment_indexes[1][0]
        second_segment_end_index = segment_indexes[1][1]

        assert 0 == first_segment_start_index
        assert (len(road_points) - 1) == second_segment_end_index
        assert first_segment_end_index == approx(90, abs=5)
        assert second_segment_start_index == approx(91, abs=5)

    @staticmethod
    def test_frenetic_generated_road():
        road_points = [
            (66.38752953287502, 78.01492758476358),
            (66.39549279998235, 88.01492441408193),
            (63.41488386330962, 97.56039299171744),
            (59.39849432596085, 106.71837394192012),
            (53.717347876135484, 114.94786815576077),
            (45.71861092315158, 120.94955184927294),
            (35.923362286475445, 122.96278411249901),
            (26.205075299578844, 120.60590099271641),
            (17.811834039492837, 115.1695877980973),
            (12.078084922014867, 106.97665663411084),
            (10.0, 97.19496132824005),
            (13.48150774832019, 87.82057581246428),
            (20.764260856833666, 80.96772916596494),
            (29.79153825268792, 76.66560610655593),
            (39.428935001131215, 73.99716388063186),
            (48.20671802392773, 69.20649323815337),
            (55.656007423636034, 62.53505505441866),
            (62.62894703718282, 55.3672022974328),
            (69.3230484201203, 47.93827191177469),
            (74.39518316897082, 39.320067395200304),
            (75.92736990007486, 29.438144312063663),
            (74.25081132886308, 19.579688481798136),
            (71.38208886203154, 10.0),
        ]

        strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=10)

        segment_indexes = strategy.extract_segments(road_points)

        logging.info(segment_indexes)

    def test_angle_based_segmentation(self):
        road_points = [
            (20, 20),
            (50, 30),
            (70, 50),
            (80, 80),
            (70, 110),
            (50, 130),
            (50, 150),
            (60, 160),
            (80, 170),
            (100, 170),
            (120, 160),
            (140, 120),
            (150, 80),
            (150, 50),
            (150, 30),
            (150, 20),
        ]

        segmentation_strategy = AngleBasedStrategy(angle_threshold=10, decision_distance=10)
        segmentation_strategy.extract_segments(road_points)

        # TODO: Add assertions
        # assert False
