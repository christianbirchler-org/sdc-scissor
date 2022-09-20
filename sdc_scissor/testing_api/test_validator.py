from shapely.geometry import LineString, MultiLineString
from sdc_scissor.testing_api.test import Test


class TestIsNotValidException(Exception):
    pass


class TestValidator:
    def validate(self, test: Test) -> bool:
        road_points_line_string: LineString = LineString(
            coordinates=[(node[0], node[1]) for node in test.interpolated_road_points]
        )
        left_bound_line_string = road_points_line_string.parallel_offset(distance=5, side='left')
        right_bound_line_string = road_points_line_string.parallel_offset(distance=5, side='right')

        if left_bound_line_string.geom_type != 'LineString' or right_bound_line_string.geom_type != 'LineString':
            test.is_valid = False
            return test.is_valid

        road_lines: MultiLineString = MultiLineString((left_bound_line_string, road_points_line_string, right_bound_line_string))

        test.is_valid = True if road_lines.is_simple else False
        return test.is_valid
