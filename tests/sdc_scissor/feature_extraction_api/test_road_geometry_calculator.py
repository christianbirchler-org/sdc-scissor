import math

from pytest import approx

from sdc_scissor.feature_extraction_api.feature_extraction import RoadGeometryCalculator


class TestRoadGeometryCalculatorAngle:
    def setup_class(self):
        self.__road_geometry_calculator = RoadGeometryCalculator()

    def test_90_degree_right_turn_get_angles(self):
        road_points = []
        radius = 50
        center_of_turn = (50, 0)

        for i in range(0, 91, 1):
            x = -1 * radius * math.cos(math.radians(i))  # minus for right turn
            y = radius * math.sin(math.radians(i))

            # translation of coordinates
            x = x + center_of_turn[0]

            road_points.append((x, y))

        turn_angles = self.__road_geometry_calculator.extract_turn_angles(road_points)

        angle_retrieved = sum(turn_angles)

        # right turns have a negative sign, whereas left turns have positives
        angle_expected = -90
        assert angle_retrieved == approx(angle_expected, abs=1)

    def test_90_degree_left_turn_get_angles(self):
        road_points = []
        radius = 50
        center_of_turn = (0, 0)

        for i in range(0, 91, 1):
            x = radius * math.cos(math.radians(i))  # plus for left turn
            y = radius * math.sin(math.radians(i))

            # translation of coordinates
            x = x + center_of_turn[0]

            road_points.append((x, y))

        turn_angles = self.__road_geometry_calculator.extract_turn_angles(road_points)

        angle_retrieved = sum(turn_angles)

        # right turns have a negative sign, whereas left turns have positives
        angle_expected = 90
        assert angle_retrieved == approx(angle_expected, abs=1)

    def test_positive_angle(self):
        v1 = (1, 0)
        v2 = (0, 1)

        angle = self.__road_geometry_calculator.get_angle(v1, v2)

        assert angle > 0

    def test_negative_angle(self):
        v1 = (0, 1)
        v2 = (1, 0)

        angle = self.__road_geometry_calculator.get_angle(v1, v2)

        assert angle < 0

    def test_negative_angle_both_vectors_direct_down(self):
        v1 = (3, -1)
        v2 = (3, -2)

        angle = self.__road_geometry_calculator.get_angle(v1, v2)

        assert angle < 0

    def test_positive_angle_both_vectors_direct_down(self):
        v1 = (3, -2)
        v2 = (3, -1)

        angle = self.__road_geometry_calculator.get_angle(v1, v2)

        assert angle > 0

    def test_negative_angle_both_vectors_direct_down_with_negative_xs(self):
        v1 = (-3, -2)
        v2 = (-3, -1)

        angle = self.__road_geometry_calculator.get_angle(v1, v2)

        assert angle < 0

    def test_positive_angle_both_vectors_direct_down_with_negative_xs(self):
        v1 = (-3, -1)
        v2 = (-3, -2)

        angle = self.__road_geometry_calculator.get_angle(v1, v2)

        assert angle > 0

    def test_negative_angle_both_vectors_direct_up_with_negative_xs(self):
        v1 = (-3, 1)
        v2 = (-3, 2)

        angle = self.__road_geometry_calculator.get_angle(v1, v2)

        assert angle < 0

    def test_positive_angle_both_vectors_direct_up_with_negative_xs(self):
        v1 = (-3, 2)
        v2 = (-3, 1)

        angle = self.__road_geometry_calculator.get_angle(v1, v2)

        assert angle > 0


class TestRoadGeometryCalculatorRoadLength:
    def setup_class(self):
        self.__road_geometry_calculator = RoadGeometryCalculator()

    def test_straight_horizontal_road(self):
        road_points = [(1, 1), (2, 1), (3, 1), (4, 1)]

        length = self.__road_geometry_calculator.get_road_length(road_points)
        expected_length = 3

        assert length == expected_length
