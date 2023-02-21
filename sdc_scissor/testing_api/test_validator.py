import abc

from shapely.geometry import LineString, MultiLineString

from sdc_scissor.feature_extraction_api.road_geometry_calculator import RoadGeometryCalculator
from sdc_scissor.testing_api.test import Test


class TestIsNotValidException(Exception):
    pass


class TestValidator(abc.ABC):
    @abc.abstractmethod
    def validate(self, test: Test) -> bool:
        pass


class SimpleTestValidator(TestValidator):
    def validate(self, test: Test) -> bool:
        test.is_valid = True
        return True


class TestValidatorDecorator(TestValidator):
    def __init__(self, wrappee: TestValidator):
        self.wrappee: TestValidator = wrappee

    def validate(self, test: Test) -> bool:
        return self.wrappee.validate(test)


class MakeTestInvalidValidator(TestValidatorDecorator):
    def __init__(self, wrappee: TestValidator):
        super().__init__(wrappee)

    def validate(self, test: Test) -> bool:
        self.wrappee.validate(test)
        test.is_valid = False
        return False


class NoIntersectionValidator(TestValidatorDecorator):
    def __init__(self, wrappee: TestValidator):
        super().__init__(wrappee)

    def validate(self, test: Test) -> bool:
        self.wrappee.validate(test)
        if not test.is_valid:
            return False

        road_points_line_string: LineString = LineString(
            coordinates=[(node[0], node[1]) for node in test.interpolated_road_points]
        )
        left_bound_line_string = road_points_line_string.parallel_offset(distance=5, side="left")
        right_bound_line_string = road_points_line_string.parallel_offset(distance=5, side="right")

        if left_bound_line_string.geom_type != "LineString" or right_bound_line_string.geom_type != "LineString":
            test.is_valid = False
            return test.is_valid

        road_lines: MultiLineString = MultiLineString(
            (left_bound_line_string, road_points_line_string, right_bound_line_string)
        )

        test.is_valid = True if road_lines.is_simple else False
        return test.is_valid


class NoTooSharpTurnsValidator(TestValidatorDecorator):
    def __init__(self, wrappee, angle_threshold=1.0):
        super().__init__(wrappee)
        self.__road_geometry_calculator = RoadGeometryCalculator()
        self.angle_threshold = angle_threshold

    def validate(self, test: Test) -> bool:
        self.wrappee.validate(test)

        p0 = test.interpolated_road_points[0][0], test.interpolated_road_points[0][1]
        p1 = test.interpolated_road_points[1][0], test.interpolated_road_points[1][1]
        previous_direction = self.__road_geometry_calculator.get_direction(p0, p1)
        previous_point = p1

        for current_point in test.interpolated_road_points[2:]:
            current_direction = self.__road_geometry_calculator.get_direction(previous_point, current_point)
            angle = self.__road_geometry_calculator.get_angle(previous_direction, current_direction)
            if angle > self.angle_threshold:
                return False
            previous_point, previous_direction = current_point, current_direction

        return True
