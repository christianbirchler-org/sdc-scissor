import pytest

from sdc_scissor.feature_extraction_api.parameterized_uniform_strategy import (
    ParameterizedUniformStrategy,
)


class TestParameterizedUniformStrategyTest:
    def test_straight_only(self):
        strategy = ParameterizedUniformStrategy("2", 0.05)

        road_points = [(x, 0) for x in range(1000)]

        segments = strategy.extract_segments(road_points)

        expected_segments = [(x * 10, x * 10 + 10) for x in range(99)]
        expected_segments.append((990, 999))
        assert segments == expected_segments

    def test_road_is_too_short(self):
        strategy = ParameterizedUniformStrategy("2", 0.0005)

        road_points = [(x, 0) for x in range(1000)]

        with pytest.raises(Exception):
            strategy.extract_segments(road_points)
